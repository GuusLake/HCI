#!/usr/bin/python3
# File name: part1.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N ()
# Date: 26-02-20

import praw
import tkinter as tk
import time

def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    subreddit = reddit.subreddit('all')
    seen_submissions = set()
    
    # https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html
    while True:
        for submission in subreddit.new(limit=10):
            if submission.fullname not in seen_submissions:
                seen_submissions.add(submission.fullname)
                print('{} {}\n'.format(submission.title, submission.url))
        time.sleep(60)

if __name__ == "__main__":
    main()
