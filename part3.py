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


class ResponseCommentTreeDisplay(CommentTreeDisplay):
    ''' Subclass of CommentTreeDisplay able to respond to comments '''
    def __init__(self, parent, reddit):
        CommentTreeDisplay.__init__(self, parent, reddit)
        self.reddit = reddit

    def attachTree(self):
        ''' After a new tree is built, replaces the old comment tree with the new one '''
        self.commentTree = self.newTree
        self.yscrollbarComment = ttk.Scrollbar(self, orient='vertical', command=self.commentTree.yview)
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.yscrollbarComment.grid(row=0, column=0, sticky='nse')
        self.commentTree.configure(yscrollcommand=self.yscrollbarComment.set)

        # Attach Double click event to new tree
        self.commentTree.bind("<Double-1>", self.addComment)

    def addComment(self, event):
        ''' Ask user for a reply to double clicked comment '''
        # Get comment ID based on its ID in the tree
        item = self.commentTree.selection()[0]
        comment = self.reddit.comment(id = item)
        try:
            reply = simpledialog.askstring(title = "Add comment", prompt = "Type your comment below:")
            comment.reply(reply)
        except:
            print("Empty string detected!")


def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )

    root = tk.Tk()
    root.geometry('1280x720')
    ctd = ResponseCommentTreeDisplay(root, reddit)
    ctd.pack(fill=tk.BOTH, expand = True)

    root.mainloop()

if __name__ == "__main__":
    main()
