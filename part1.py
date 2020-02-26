#!/usr/bin/python3
# File name: part1.py
# 
# Authors: Lakeman, G.
# Date: 05-02-20

import praw

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent')
