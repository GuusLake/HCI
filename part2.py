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
    def __init__(self, parent, reddit, queue):
        tk.Frame.__init__(self, parent)
        self.reddit = reddit
        self.queue = queue
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load comments", command=self.loadCommentsPopup)
        self.filemenu.add_command(label="exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        parent.config(menu=self.menubar)
        
        self.botframe = tk.Frame(self)
        self.commentTree = ttk.Treeview(self.botframe)
        self.vsb = tk.Scrollbar(self.botframe, orient="vertical",command=self.commentTree.yview)
        self.vsb.pack(side="right", fill="y")
        self.commentTree.pack(side="left", fill="both", expand=True)
        self.botframe.pack() 
        
    def loadCommentsPopup(self):
        self.win= tk.Toplevel(self)
        self.label=tk.Label(self.win, text="Enter an URL")
        self.label.pack()
        self.submisUrl=tk.Entry(self.win)
        self.submisUrl.pack()
        self.btn=tk.Button(self.win,text='Load comments',command=self.loadComments)
        self.btn.pack()
    
    def loadComments(self):
        # ADD URL VARIABLE HERE INSTEAD OF VALUE
        self.value=self.submisUrl.get()
        # ADD OLD COMMENT TREE CLEANUP HERE
        # ADD LOADING PROCEDURE HERE
        self.win.destroy()
        
        

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
