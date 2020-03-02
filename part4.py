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
    def __init__(self, reddit, comment_queue, update_queue):
        self.reddit = reddit
        self.comment_queue = comment_queue
        self.update_queue = update_queue
        self.old_comments = 0
        threading.Thread(target=self.updateLoop).start()
    
    def updateLoop(self):
        while True:
            try:
                self.old_comments = comment_queue.getNextItem()
            except: pass
            
            submission = self.reddit.submission(url=self.submisUrl)
            new_comments = submission.num_comments
            if self.old_comments < new_comments:
                update_queue.sendItem(True)
            time.sleep(0.100)


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
    def __init__(self, parent, reddit, comment_queue, update_queue):
        ResponseCommentTreeDisplay.__init__(self, parent, reddit)
        self.reddit = reddit
        self.comment_queue = comment_queue
        self.update_queue = update_queue
        self.after(100, self.checkUpdate)
        
    def loadComments(self):
        self.submisUrl = self.urlEntry.get()
        try:
            self.submission = self.reddit.submission(url=self.submisUrl)
            self.comment_queue.sendItem(self.submission.num_comments)
            threading.Thread(target=self.showComments).start()
        except:
            messagebox.showerror('Error', 'THe URL was invalid')
        self.win.destroy()
    
    def checkUpdate(self):
        try:
            if self.update_queue.getNextItem() == True:
                self.loadComments()
                print("Updating!")
        except: pass
        self.after(100, self.checkUpdate)
        
def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    comment_queue = MyQueue(1, False, False)
    update_queue = MyQueue(1, False, False)
    checker = UpdateChecker(reddit, comment_queue, update_queue)
    ctd = UpdatedTreeDisplay(root, reddit, comment_queue, update_queue)
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
