#!/usr/bin/env python
# coding=utf-8

from __future__ import division

import os, sys, glob
import random
import pprint
import time

import tumblpy

import markov
import tumblr_auth_tokens
from utils import *

#-------------------------------------------------------------------------------------------
#--- COMMAND LINE

HELP = """
tumblr-queue-entire-file.py file.txt

Sends the entire file to Tumblr, making one text post in the queue for each line in the file.
Leaves the original file unchanged.
"""

ARGS = sys.argv[1:]

if '-h' in ARGS or len(ARGS) != 1:
    print
    print HELP
    print
    sys.exit(0)

FILENAME = ARGS[0]

#-------------------------------------------------------------------------------------------
#--- TUMBLR SETUP

t = tumblpy.Tumblpy(app_key = tumblr_auth_tokens.TUMBLR_CONSUMER_KEY,
                    app_secret = tumblr_auth_tokens.TUMBLR_CONSUMER_SECRET,
                    oauth_token = tumblr_auth_tokens.TUMBLR_OAUTH_TOKEN,
                    oauth_token_secret = tumblr_auth_tokens.TUMBLR_OAUTH_TOKEN_SECRET)

tumblrUrl = 'http://%s.tumblr.com'%(tumblr_auth_tokens.TUMBLR_USERNAME.replace('_','-'))

#-------------------------------------------------------------------------------------------
#--- MAIN

if __name__ == '__main__':

    print '---------------------------------------------------------------------------------\\'
    for ii,line in enumerate(file(FILENAME,'r').readlines()):
        line = line.strip()
        if not line:
            continue
        print 'posting %s: "%s"...'%(ii,line)
        post = t.post(  'post',
                        blog_url=tumblrUrl,
                        params=dict(type='text',
                                    state='queue',
                                    title=line,
                                    body='',
                                    source_url=tumblrUrl,
                                    source_title=tumblrUrl,
                                   )
                     )
    print '---------------------------------------------------------------------------------/'





#
