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
import threading
from part2 import CommentTreeDisplay


class ResponseCommentTreeDisplay(CommentTreeDisplay):
    def __init__(self, parent, reddit):
        CommentTreeDisplay.__init__(self, parent, reddit)
        print("Init complete")
        
    def attachTree(self):
        self.commentTree = self.newTree
        self.yscrollbarComment = ttk.Scrollbar(self, orient='vertical', command=self.commentTree.yview)
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.yscrollbarComment.grid(row=0, column=0, sticky='nse')
        self.commentTree.configure(yscrollcommand=self.yscrollbarComment.set)
        self.commentTree.bind("<Double-1>", self.addComment)
        print("Attached Event")
    
    def addComment(self, event):
        print("Double Click Detected")
        comment = reddit.comment(id = commentID)
        reply = simpledialog.askstring(title = "Add comment", prompt = "Type your comment below:")
        comment.reply(reply)
        
def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    ctd = ResponseCommentTreeDisplay(root, reddit)
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
