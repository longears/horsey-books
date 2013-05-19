#!/usr/bin/env python
# coding=utf-8

from __future__ import division

import os, sys, glob
import random
import pprint
import time
import subprocess

import markov
import config
from utils import *


#-------------------------------------------------------------------------------------------
#--- COMMAND LINE

HELP = """
generate.py
  choose exactly one of these modes:
    --interactive       # (default) approve or reject each message and save good ones to queue.txt
    --unattended        # generate one message every UPDATE_FREQ seconds and print it
    --say               # same as --unattended, but speak them and wait SAY_PAUSE between each one
    --many [how_many]   # generate a bunch at once with no delay and print them, so you can feed them to grep
"""

def helpAndQuit():
    print
    print HELP
    print
    sys.exit(0)

ARGS = sys.argv[1:]
N_TWEETS = 5
for arg in ARGS:
    try:
        N_TWEETS = int(arg)
    except:
        if not arg.startswith('--'):
            print 'Error: unknown command line'
            helpAndQuit()

if '-h' in ARGS or '--help' in ARGS:
    helpAndQuit()

if len(ARGS) == 0:
    ARGS = ['--interactive']

if not '--unattended' in ARGS and not '--interactive' in ARGS and not '--many' in ARGS and not '--say' in ARGS:
    helpAndQuit()


#-------------------------------------------------------------------------------------------
#--- HELPERS

def runCmd(parts):
    """Run a command.  Parts is a list of strings / arguments.
    Ignore the output.
    Example: runCmd(['ls','-la'])
    """
    return subprocess.call(parts)


#-------------------------------------------------------------------------------------------
#--- MAIN

print '---------------------------------------------------------------------------------\\'
print

if __name__ == '__main__':

    if '--interactive'  in ARGS:
        print 'usage:'
        print '    y / yes                      save to the queue'
        print '    some long message            queue your own message instead'
        print '    n / no / blank response      ignore and discard'
        print '    q / quit                     quit'
        print

    # set up markov object
    mymarkov = markov.Markov(n=config.MARKOV_N)

    # learn from text files
    inputFNs = glob.glob(config.INPUT_GLOB)
    if len(inputFNs) == 0:
        print 'ERROR: no input files found in %s'%config.INPUT_GLOB
        sys.exit(0)
    for inputFN in inputFNs:
        mymarkov.learn(markov.tokenize(fn=inputFN))

    ii = 0
    while True:

        # generate a phrase
        phrase = mymarkov.speak(mintokens=random.randint(config.MINTOKENS1,config.MINTOKENS2),maxtokens=config.MAXTOKENS)
        if config.TWITTERIZE:
            phrase = markov.twitterize(phrase)

        print phrase

        # get user input
        if '--interactive'  in ARGS:
            accept = raw_input('> ')
            if accept in ('q','quit','exit','\q',':q'):
                sys.exit(0)
            elif accept in ('y','yes'):
                print '    ok.  queueing...'
                appendFile(config.QUEUE_FN,phrase+'\n')
            elif len(accept) > 4:
                phrase = accept
                print '    queueing custom phrase...'
                appendFile(config.QUEUE_FN,phrase+'\n')
            else:
                pass

        print

        if '--say' in ARGS:
            runCmd(['say','-v',config.SAY_VOICE,phrase])
            time.sleep(conifg.SAY_PAUSE)

        if '--unattended' in ARGS:
            print '...'
            time.sleep(config.UPDATE_FREQ)

        if '--many' in ARGS:
            ii += 1
            if ii >= N_TWEETS:
                break


print '---------------------------------------------------------------------------------/'





#
