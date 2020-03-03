#!/usr/bin/python3
# File name: part2.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N (s3133125)
# Date: 03-03-20

import praw
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import time
import queue
import threading
from part2 import CommentTreeDisplay
from part3 import ResponseCommentTreeDisplay


class UpdateChecker:
    ''' Threading class to check for new comments '''
    def __init__(self, reddit, update_queue):
        self.reddit = reddit
        self.update_queue = update_queue
        threading.Thread(target=self.updateLoop).start()

    def changeSubmission(self, old_comments, url):
        ''' Change url and old comment count of submission to monitor '''
        self.old_comments = old_comments
        self.url = url

    def updateLoop(self):
        ''' Loop which check the comment count and 
            compares it to last known comment count '''
        while True:
            try:
                submission = self.reddit.submission(url=self.url)
                new_comments = submission.num_comments
                if self.old_comments < new_comments:
                    self.update_queue.sendItem(True)
                    print("Send queue")
            except: pass
            time.sleep(1)


class MyQueue:
    ''' Queue class to transfer new submission data between threads '''
    def __init__(self, maxsize, sendBlock, getBlock):
        self.myqueue=queue.Queue(maxsize)
        self.sendBlock = sendBlock
        self.getBlock = getBlock

    def sendItem(self,item):
        ''' Add item to queue '''
        self.myqueue.put(item, block=self.sendBlock)

    def getNextItem(self):
        ''' Get item from queue '''
        message=self.myqueue.get(block=self.getBlock)
        return message


class UpdatedTreeDisplay(ResponseCommentTreeDisplay):
    ''' Subclass of ResponseCommentTreeDisplay which periodically checks for new comments '''
    def __init__(self, parent, reddit, queue, updater):
        ResponseCommentTreeDisplay.__init__(self, parent, reddit)
        self.reddit = reddit
        self.queue = queue
        self.updater = updater
        self.time_slider = tk.Scale(self, from_=1, to=100, orient='horizontal', label='Select time between updates in seconds')
        self.time_slider.set(10)
        self.time_slider.grid(column=0, row=1, columnspan=2, sticky = tk.NSEW)
        self.after(self.time_slider.get()*1000, self.checkUpdate)

    def loadComments(self):
        ''' After url has been given, checks validity and closes the window '''
        self.submisUrl = self.urlEntry.get()
        try:
            # Check for valid reddit post
            self.submission = self.reddit.submission(url=self.submisUrl)
            # Build the tree for new post in seperate thread
            threading.Thread(target=self.showComments).start()
            # Update the submission being monitored
            threading.Thread(target=self.updater.changeSubmission(self.submission.num_comments,self.submisUrl))
        except:
            messagebox.showerror('Error', 'The URL was invalid')
        self.win.destroy()

    def checkUpdate(self):
        ''' Checks the queue to see if new comments have been found '''
        try:
            self.update = self.queue.getNextItem()
            # If new comments were found
            if self.update:
                self.submission = self.reddit.submission(url=self.submisUrl)
                # Build new tree including new comments
                threading.Thread(target=self.showComments).start()
                # Updates the number of old comments
                threading.Thread(target=self.updater.changeSubmission(self.submission.num_comments,self.submisUrl))
        except: pass
        self.after(self.time_slider.get()*1000, self.checkUpdate)


def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )

    root = tk.Tk()
    root.geometry('1280x720')
    update_queue = MyQueue(1, False, False)
    updater = UpdateChecker(reddit, update_queue)
    ctd = UpdatedTreeDisplay(root, reddit, update_queue, updater)
    ctd.pack(fill=tk.BOTH, expand = True)

    root.mainloop()


if __name__ == "__main__":
    main()
