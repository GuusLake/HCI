#!/usr/bin/python3
# File name: part2.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N (s3133125)
# Date: 26-02-20

import praw
import tkinter as tk
from tkinter import ttk
import time
import queue

class CommentsQueue:
    def __init__(self, maxsize =10):
        self.myqueue=queue.Queue(maxsize)

    def sendItem(self,item):
        self.myqueue.put(item, block=True)

    def getNextItem(self):
        message=self.myqueue.get(block=False)
        return message

class CommentTreeDisplay(tk.Frame):
    def __init__(self, parent, reddit, q):
        tk.Frame.__init__(self, parent)
        self.reddit = reddit
        self.queue = q
        
        self.columnconfigure(0, weight=1)
        #self.entry = tk.Entry(self)
        #self.entry.pack(fill=tk.X, side="left", expand=True)
        #self.button = tk.Button(self,text = "Get Comments")
        #self.button.pack(side="right", fill=tk.X)
        
        #self.botframe = tk.Frame(self)
        self.commentTree = ttk.Treeview(self)
        #self.vsb = tk.Scrollbar(self.botframe, orient="vertical",command=self.commentTree.yview)
        #self.vsb.pack(side="right", fill="y")
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        #self.botframe.pack() 
        self.showComments('https://www.reddit.com/r/AskReddit/comments/fca671/what_has_always_been_your_fun_fact_when_asked/', reddit)
    
    def showComments(self, url, reddit):
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            self.commentTree.insert('', 'end', comment.id, text=comment.body)
            self.recursiveTreeBuilder(comment, comment.id)
            
        
    def recursiveTreeBuilder(self, parent, parent_id):
        for child in parent.replies:
            self.commentTree.insert(parent_id, 'end', child.id, text=child.body)
            self.recursiveTreeBuilder(child, child.id)
        
        

def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    queue = CommentsQueue()
    ctd = CommentTreeDisplay(root, reddit, queue)
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
