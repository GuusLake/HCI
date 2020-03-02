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
        self.columnconfigure(0, weight=1)
        self.queue = queue
        
        # Make menubar
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load comments", command=self.loadCommentsPopup)
        self.filemenu.add_command(label="exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        parent.config(menu=self.menubar)
        
        # Create comment tree
        self.commentTree = ttk.Treeview(self)
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.yscrollbarComment = ttk.Scrollbar(self, orient='vertical', command=self.commentTree.yview)
        self.commentTree.configure(yscrollcommand=self.yscrollbarComment.set)
        self.yscrollbarComment.grid(row=0, column=0, sticky='nse')
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
        for node in self.commentTree.get_children():
            self.commentTree.delete(node)
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
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
