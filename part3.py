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


class CommentTreeDisplay(tk.Frame):
    def __init__(self, parent, reddit):
        tk.Frame.__init__(self, parent)
        self.reddit = reddit
        self.columnconfigure(0, weight=1)
        
        # Make menubar
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load comments", command=self.loadCommentsPopup)
        self.filemenu.add_command(label="exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        parent.config(menu=self.menubar)
        
        # Create comment tree
        self.commentTree = ttk.Treeview(self)
        self.yscrollbarComment = ttk.Scrollbar(self, orient='vertical', command=self.commentTree.yview)
        self.commentTree.configure(yscrollcommand=self.yscrollbarComment.set)
        self.yscrollbarComment.grid(row=0, column=0, sticky='nse')
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.submisUrl = 'https://www.reddit.com/r/AskReddit/comments/fca671/what_has_always_been_your_fun_fact_when_asked/'
        threading.Thread(target=self.showComments).start()
    
    def showComments(self):
        self.newTree = ttk.Treeview(self)
            
        submission = self.reddit.submission(url=self.submisUrl)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            try:
                self.newTree.insert('', 'end', comment.id, text=comment.body)
            except:
                self.newTree.insert('', 'end', comment.id, text="CHARACTER ERROR")
            self.recursiveTreeBuilder(comment, comment.id)
            
        self.commentTree = self.newTree
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
            
    def recursiveTreeBuilder(self, parent, parent_id):
        for child in parent.replies:
            try:
                self.newTree.insert(parent_id, 'end', child.id, text=child.body)
            except:
                self.newTree.insert(parent_id, 'end', child.id, text="CHARACTER ERROR")
            self.recursiveTreeBuilder(child, child.id)
            
    def loadCommentsPopup(self):
        self.win= tk.Toplevel(self)
        self.label=tk.Label(self.win, text="Enter an URL")
        self.label.pack()
        self.urlEntry=tk.Entry(self.win)
        self.urlEntry.pack()
        self.btn=tk.Button(self.win,text='Load comments',command=self.loadComments)
        self.btn.pack()
    
    def loadComments(self):
        self.submisUrl = self.urlEntry.get()
        threading.Thread(target=self.showComments).start()
        self.win.destroy()

class ResponseCommentTreeDisplay(CommentTreeDisplay):
    def __init__(self, parent, reddit, queue):
        CommentTreeDisplay.__init__(self, parent, reddit, queue)
        self.commentTree.bind("<Double-1>", self.addComment)
    
    def addComment(self, event):
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
    ctd = CommentTreeDisplay(root, reddit)
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
