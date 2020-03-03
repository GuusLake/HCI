#!/usr/bin/python3
# File name: part2.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N (s3133125)
# Date: 26-02-20

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
    def __init__(self, reddit, update_queue):
        self.reddit = reddit
        self.update_queue = update_queue
        threading.Thread(target=self.updateLoop).start()
        
    def changeSubmission(self, old_comments, url):
        self.old_comments = old_comments
        self.url = url
    
    def updateLoop(self):
        while True:
            try:
                submission = self.reddit.submission(url=self.url)
                new_comments = submission.num_comments
                print("Old Comments:")
                print(self.old_comments)
                print("New Comments:")
                print(new_comments)
                if self.old_comments < new_comments:
                    self.update_queue.sendItem(True)
                    print("Send queue")
            except: pass
            time.sleep(1)


class MyQueue:
    def __init__(self, maxsize, sendBlock, getBlock):
        self.myqueue=queue.Queue(maxsize)
        self.sendBlock = sendBlock
        self.getBlock = getBlock

    def sendItem(self,item):
        self.myqueue.put(item, block=self.sendBlock)

    def getNextItem(self):
        message=self.myqueue.get(block=self.getBlock)
        return message


class UpdatedTreeDisplay(ResponseCommentTreeDisplay):
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
        self.submisUrl = self.urlEntry.get()
        try:
            self.submission = self.reddit.submission(url=self.submisUrl)
            threading.Thread(target=self.showComments).start()
            threading.Thread(target=self.updater.changeSubmission(self.submission.num_comments,self.submisUrl))
        except:
            messagebox.showerror('Error', 'The URL was invalid')
        self.win.destroy()
    
    def checkUpdate(self):
        try:
            self.update = self.queue.getNextItem()
            if self.update:
                print("Found update!")
                self.submission = self.reddit.submission(url=self.submisUrl)
                threading.Thread(target=self.showComments).start()
                threading.Thread(target=self.updater.changeSubmission(self.submission.num_comments,self.submisUrl))
                print("Asked to load comments")
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
    update_queue = MyQueue(1, False, False)
    updater = UpdateChecker(reddit, update_queue)
    ctd = UpdatedTreeDisplay(root, reddit, update_queue, updater)
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
