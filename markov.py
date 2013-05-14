#!/usr/bin/env python
# coding=utf-8

from __future__ import division

import os, sys, glob
import random
import pprint
import time

import config
from utils import *

#-------------------------------------------------------------------------------------------
#--- HELPERS

def twitterize(phrase):
    """Given a string of any length, shorten it to a tweet.
    Do this by truncating at 140 chars, then chopping at the last SENTENCE_END_CHAR if possible.
    Sometimes, drop a few words, horse_ebooks style.
    """
    # shorten to a tweet
    phrase = phrase[:config.TWEET_LENGTH]

    # if possible, chop off at the last sentence ending character
    options = []
    for char in config.SENTENCE_END_CHARS:
        if char in phrase:
            chopped = phrase.rsplit(char,1)[0] + char
            options.append(chopped)
    if options:
        options.sort(key=lambda x: len(x))
        phrase = options[-1] # choose the longest one
    else:
        # couldn't find a sentence ending character.
        # let's just remove the last word becuase it's probably a partial word
        phrase = ' '.join(phrase.split(' ')[:-1])

    # truncate, horse_ebooks style
    if random.random() < config.TRUNCATION_PROBABILITY:
        words = phrase.split(' ')
        if len(words) > 4:
            words = words[:-int(len(words) * config.TRUNCATION_FRACTION)]
            phrase = ' '.join(words)

    # all caps
    if random.random() < config.ALLCAPS_PROBABILITY:
        phrase = phrase.upper()

    # one word caps
    if random.random() < config.ALLCAPS_ONEWORD_PROBABILITY:
        words = phrase.split(' ')
        # try to find a long word
        for tries in range(100):
            ii = random.randrange(0,len(words))
            if len(words[ii]) >= config.ALLCAPS_ONEWORD_MIN_WORD_LENGTH: break
        words[ii] = words[ii].upper()
        phrase = ' '.join(words)

    return phrase


def tokenize(fn=None, string=None, preserveSingleNewline=False, preserveMultipleNewline=False, doubleNewlineCreatesPeriod=True):
    """Given a filename, yield its contents as a series of parsed tokens, one at a time.
    Supply either a filename or a string, but not both.
    If preserveSingleNewline, newlines become '\n' tokens.  Otherwise they're removed.
    If preserveMultipleNewline, multiple newlines in a row come back as a '\n' token.  Otherwise they're removed.
    If doubleNewlineCreatesPeriod, two+ newlines in a row generate a '.' token (before a possible '\n' token)
    """
    assert (fn is None) + (string is None) == 1
    if fn is not None:
        generator = streamFileLines(fn)
    else:
        generator = [string]

    buffer = []
    lastToken = ''
    lastLineWasBlank = False

    for lineNum,line in enumerate(generator):
        line = line.strip()

        if not line:
            if not lastLineWasBlank and lastToken not in config.SENTENCE_END_CHARS:
                if doubleNewlineCreatesPeriod:
                    yield '.'
                    lastToken = '.'
            if preserveMultipleNewline:
                yield config.NEWLINE
                lastToken = config.NEWLINE
            lastLineWasBlank = True
            continue
        lastLineWasBlank = False

        for ii,smiley in enumerate(config.SMILEYS):
            line = line.replace(smiley,'zzzSMILEY%szzz'%ii)

        for k,v in config.REPLACEMENTS.items():
            line = line.replace(k,v)

        for char in config.TOKEN_CHARS:
            line = line.replace(char,' %s '%char)

        for char in config.REMOVE_CHARS:
            line = line.replace(char,' ')

        for ii,smiley in enumerate(config.SMILEYS):
            line = line.replace('zzzSMILEY%szzz'%ii,' %s '%config.SMILEYS[ii])

        tokens = line.split()
        if preserveSingleNewline and lineNum != 0:
            yield config.NEWLINE 
            lastToken = token
        for token in tokens:
            yield token.lower()
            lastToken = token

    if preserveSingleNewline:
        yield config.NEWLINE 


def untokenize(tokens):
    """Given an iterable of tokens, return a string with them mushed together properly.
    Correctly capitalize sentences, remove spaces before commas, etc.
    """

    # capitalize the first word of a sentence
    capitalizedTokens = []
    lastToken = '.'
    for token in tokens:
        if lastToken in config.SENTENCE_END_CHARS:
            token = token.capitalize()
        if token == 'i':
            token = token.capitalize()
        if token.startswith("i'"):
            token = token.capitalize()
        capitalizedTokens.append(token)
        lastToken = token

    tokensAndSpaces = []
    for token in capitalizedTokens:
        # insert spaces except in front of TOKEN_CHARS
        if token not in config.TOKEN_CHARS:
            tokensAndSpaces.append(' ')
        tokensAndSpaces.append(token)
        # insert extra space after SENTENCE_END_CHARS
        if token in config.SENTENCE_END_CHARS:
            tokensAndSpaces.append(' ')

    # remove leading space
    tokensAndSpaces.pop(0)

    # remove trailing space
    if tokensAndSpaces[-1] == ' ':
        tokensAndSpaces.pop()

    result = ''.join(tokensAndSpaces)

    return result.strip()

#-------------------------------------------------------------------------------------------
#--- MARKOV

def chooseRandomlyFromCountDict(d):
    """Given a dict mapping words to their frequencies:
        word: 23,
        anotherword: 49,
        someword: 103,
    Return one of the keys with probability proportional to its count.
    """
    total = sum(d.values())
    randVal = random.uniform(0,total)
    items = d.items()

    countSoFar = 0
    for word,count in d.items():
        countSoFar += count
        if countSoFar > randVal:
            return word
    return word


class Markov(object):
    def __init__(self,n=3):
        self.n = n
        self.db = {} # mapping (token1,token2,token3) -> {tokenA:countA, tokenB:countB}

    def learn(self,tokenizer):
        """Given a tokenizer, read the tokens and learn their patterns.
        """
        lastN = tuple([None] * self.n)
        for token in tokenizer:
            counts = self.db.get(lastN,{})
            counts[token] = counts.get(token,0)+1
            self.db[lastN] = counts

            lastN = list(lastN)
            lastN.pop(0)
            lastN.append(token)
            lastN = tuple(lastN)

    def _dbGet(self,lastN):
        """Look up a token sequence in the db and return a count dictionary.
        Nones in the token sequence act as wildcards.  In this case, multiple matching count dictionaries
         will be combined into one and returned.
        If not found, return None.
        """
        if None not in lastN:
            return self.db.get(lastN,None)

        combinedCounts = {}
        for key,counts in self.db.items():
            # check if wildcard matches
            fail = False
            for ii in range(len(lastN)):
                if lastN[ii] is not None and lastN[ii] != key[ii]: fail = True
            if fail: continue

            # combine dicts
            for token,count in counts.items():
                combinedCounts[token] = combinedCounts.get(token,0) + count

        return combinedCounts

    def speak(self,mintokens=50,maxtokens=100,startToken='.',stopTokens=config.SENTENCE_END_CHARS):
        """Return a string.
        It will be at least mintokens long.  After mintokens it will end as soon as it hits stopToken or
         if it gets longer than maxtokens.
        """
        lastN = tuple([None] * (self.n-1) + [startToken])
        result = []
        ii = 0
        while True:
            counts = self._dbGet(lastN)
            if counts is None:
                # got a sequence we haven't seen before.  let's start over.
                lastN = tuple([None] * (self.n-1) + [startToken])
                counts = self._dbGet(lastN)
            token = chooseRandomlyFromCountDict(counts)
            result.append( token )

            lastN = list(lastN)
            lastN.pop(0)
            lastN.append(token)
            lastN = tuple(lastN)

            ii += 1
            if ii >= mintokens:
                if token in stopTokens:
                    break
            if ii >= maxtokens:
                break
        return untokenize(result)

    def report(self):
        return '<Markov(%s) with %s entries in db>'%(self.n,len(self.db))


