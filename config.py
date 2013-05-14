#!/usr/bin/env python
# coding=utf-8

#-------------------------------------------------------------------------------------------
#--- for generate.py

QUEUE_FN = 'queue.txt'
POSTED_FN = 'posted.txt'
INPUT_GLOB = 'text/*.txt'

UPDATE_FREQ = 10    # when --unattended, wait this long between phrases
SAY_PAUSE = 1.4     # wait this long when speaking
SAY_VOICE = 'alex'  # OSX voices: vicki, alex, bruce, fred

MARKOV_N = 2     # use Markov chains of length N

MINTOKENS1 = 5   # min tokens in a phrase will be randomly between MINTOKENS1 and MINTOKENS2
MINTOKENS2 = 20  
MAXTOKENS = 200  # max tokens in a phrase

TWITTERIZE = True   # shorten to fit in a tweet and sometimes make it all caps

#-------------------------------------------------------------------------------------------
#--- for markov.py

# twitterizing
TWEET_LENGTH = 140
TRUNCATION_PROBABILITY = 0.3
TRUNCATION_FRACTION = 0.3 # remove this % of the end of the message
ALLCAPS_PROBABILITY = 0.1
ALLCAPS_ONEWORD_PROBABILITY = 0.15
ALLCAPS_ONEWORD_MIN_WORD_LENGTH = 4 # only apply to words at least this long

NEWLINE = '\n'

# these are part of a token
# this variable is actually ignored but is just here for humans to look at
IN_WORD_CHARS = "'@$&/"

# preserve smileys or other sequences of characters.  put longer ones first.
SMILEYS = '>:3 <_< >_> ... <3 :3 :) :/ :] --'.split()

# replace each key with the corresponding value
REPLACEMENTS = {
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
    }

# these should count as a whole word.
# in text they do not have spaces in front of them.
TOKEN_CHARS = '.?!,;:'

# these should be removed and replaced with a space
REMOVE_CHARS = '"<>[]{}()\\|+-_=#%^*'

# chars that end a sentence
SENTENCE_END_CHARS = '.!?'

