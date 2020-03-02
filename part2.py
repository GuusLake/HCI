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
        #self.entry = tk.Entry(self)
        #self.entry.pack(fill=tk.X, side="left", expand=True)
        #self.button = tk.Button(self,text = "Get Comments")
        #self.button.pack(side="right", fill=tk.X)
        
        self.botframe = tk.Frame(self)
        self.commentTree = ttk.Treeview(self.botframe)
        self.vsb = tk.Scrollbar(self.botframe, orient="vertical",command=self.commentTree.yview)
        self.vsb.pack(side="right", fill="y")
        self.commentTree.pack(side="left", fill="both", expand=True)
        self.botframe.pack() 
        
    def showComments(self, url):
        
        

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
    ctd.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
