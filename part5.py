#!/usr/bin/python3
# File name: part2.py
# Authors: Lakeman, G (s3383180) and Algra, N (s3133125)
# Date: 03-03-20

import praw
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import time
import queue
import threading


class RedditStream:
    ''' Threading class to get new submissions '''
    def __init__(self, sub, reddit, q):
        self.subreddit = reddit.subreddit(sub)
        self.queue = q
        threading.Thread(target=self.redditLoop).start()
        self.lastsubmission = None

    def redditLoop(self):
        ''' Loop which checks for new submissions '''
        while True:
            for submission in self.subreddit.new(limit=1):
                # if the submission is not the same as the last new submission
                if submission.fullname != self.lastsubmission:
                    self.lastsubmission = submission.fullname
                    # send the title, subreddit, and id to queue
                    self.queue.sendItem([submission.title, submission.subreddit.display_name, submission.id])
            time.sleep(0.001)


class SubmissionQueue:
    ''' Queue class to transfer new submission data between threads '''
    def __init__(self, maxsize =100):
        self.myqueue=queue.Queue(maxsize)

    def sendItem(self,item):
        ''' Add item to queue '''
        self.myqueue.put(item, block=True)

    def getNextItem(self):
        ''' Get item from queue '''
        message=self.myqueue.get(block=False)
        return message


class IncomingSubmissions(tk.Frame):
    ''' Main interface class for the reddit submission stream '''
    def __init__(self, parent, reddit, q, n):
        tk.Frame.__init__(self, parent)

        # Tree
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.reddit = reddit
        self.queue = q
        self.notebook = n
        self.parent = parent
        self.tree = ttk.Treeview(self, columns=('Subreddit'))
        self.tree.heading("#0", text="Title")
        self.tree.heading("Subreddit", text="Subreddit")
        self.yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.grid(row=0, column=2, sticky='nse')
        self.tree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.tree.bind("<Double-1>", self.addNewPage)

        # Make menubar
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load comments", command=self.loadCommentsPopup)
        self.filemenu.add_command(label="Close current tab", command=self.closeTab)
        self.filemenu.add_command(label="exit", command=self.parent.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        parent.config(menu=self.menubar)

        # Time slider and play/pause
        self.paused = False
        self.time_slider = tk.Scale(self, from_=1, to=100, orient='horizontal', label='Select time between posts in 0.1 seconds')
        self.time_slider.set(10)
        self.time_slider.grid(column=0, row=1, columnspan=2, sticky = tk.NSEW)
        self.buttonPause = tk.Button(self, text = "Pause", command = self.pause)
        self.buttonPause.grid(column=2, row=1, sticky = 'sew')

        # White/Blacklist
        self.wbList = []
        self.listType = 'Whitelist'
        self.listString = tk.StringVar()
        self.listEntry = tk.Entry(self, textvariable=self.listString)
        self.listString.set("Example, List, Input")
        self.listEntry.grid(column=0, row=2, sticky= tk.NSEW)
        self.buttonListType = tk.Button(self, text = "Whitelist", command = self.changeListType)
        self.buttonListType.grid(column=1, row=2, sticky = 'sew')
        self.buttonListSubmit = tk.Button(self, text = "Submit", command = self.changeListStart)
        self.buttonListSubmit.grid(column=2, row=2, sticky = 'sew')

        self.after(self.time_slider.get()*100, self.checkQueue)

    def checkQueue(self):
        ''' Recieves items from queue and adds them to treeview '''
        if not self.paused:
            try:
                # Do something with submissions, add them into treeview
                [title, subreddit, id] = self.queue.getNextItem()
                if self.wbList:
                    if (self.listType == 'Whitelist'):
                        if (subreddit in self.wbList):
                            self.tree.insert('', 'end', id, text=title,values=(subreddit))
                            self.tree.yview_moveto(1)
                    else:
                        if (subreddit not in self.wbList):
                            self.tree.insert('', 'end', id, text=title,values=(subreddit))
                            self.tree.yview_moveto(1)
                else:
                    self.tree.insert('', 'end', id, text=title,values=(subreddit))
                    self.tree.yview_moveto(1)

            except: pass
        self.after(self.time_slider.get()*100, self.checkQueue)

    def pause(self):
        ''' Pauses checking queue for new submissions '''
        if self.paused:
            self.paused = False
            self.buttonPause.config(text='Pause')
        else:
            self.paused = True
            self.buttonPause.config(text='Resume')

    def changeListType(self):
        ''' Changes whitelist to blacklist and vice versa '''
        if (self.listType == 'Whitelist'):
            self.buttonListType.config(text='Blacklist')
        else:
            self.buttonListType.config(text='Whitelist')

    def changeListStart(self):
        ''' Starts white/blacklist update '''
        threading.Thread(target=self.changeList).start()

    def changeList(self):
        ''' Updates white/blacklist '''
        if self.listString.get():
            self.wbListTest = self.listString.get().split(', ')
            if (self.checkSubreddits(self.wbListTest)):
                self.wbList = self.wbListTest
                self.listType = self.buttonListType['text']
        else:
            self.wbList = []

    def checkSubreddits(self, subredditList):
        '''
        Checks if the subreddits in the black or whitelist exist

        Parameters:
        subredditList (list): list of subreddits

        Returns:
        bool: True if all subreddits exist and False if not

        '''
        for subreddit in subredditList:
            if not(subredditList):
                return True
            try:
                # Try to do a subreddit exact search
                self.reddit.subreddits.search_by_name(subreddit, exact=True)
            except:
                # If it fails return False
                messagebox.showerror('Error', '{0} does not exist\nThe old '.format(subreddit))
                return False
        return True

    def addNewPage(self, event):
        ''' Makes a new ResponseCommentTreeDisplay and adds it to the notebook '''
        item = self.tree.selection()[0]
        submission = self.reddit.submission(id = item)
        comments = ResponseCommentTreeDisplay(self.parent, self.reddit, item, 'id')
        self.notebook.add(comments, text=submission.subreddit)

    def loadCommentsPopup(self):
        ''' Shows popup asking for a submission url '''
        self.win= tk.Toplevel(self)
        self.label=tk.Label(self.win, text="Enter an URL")
        self.label.pack()
        self.urlEntry=tk.Entry(self.win)
        self.urlEntry.pack()
        self.btn=tk.Button(self.win,text='Load comments',command=self.loadComments)
        self.btn.pack()

    def loadComments(self):
        ''' After url has been given, checks validity and closes the window '''
        self.submisUrl = self.urlEntry.get()
        try:
            # Check for valid reddit post
            submission = self.reddit.submission(url=self.submisUrl)
            comments = ResponseCommentTreeDisplay(self.parent, self.reddit, self.submisUrl, 'url')
            self.notebook.add(comments, text=submission.subreddit)
        except:
            messagebox.showerror('Error', 'THe URL was invalid')
        self.win.destroy()

    def closeTab(self):
        ''' Closes notebook tab '''
        self.notebook.forget(self.notebook.select())


class CommentTreeDisplay(tk.Frame):
    ''' An interface to display comments of a reddit submission in a tree '''
    def __init__(self, parent, reddit, id, method):
        tk.Frame.__init__(self, parent)
        self.reddit = reddit
        self.method = method
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create comment tree
        self.commentTree = ttk.Treeview(self)
        self.yscrollbarComment = ttk.Scrollbar(self, orient='vertical', command=self.commentTree.yview)
        self.commentTree.configure(yscrollcommand=self.yscrollbarComment.set)
        self.yscrollbarComment.grid(row=0, column=0, sticky='nse')
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.submisId = id
        self.showComments()

    def showComments(self):
        ''' Build a tree of comments for the top level comments '''
        self.newTree = ttk.Treeview(self)
        if self.method == 'id':
            submission = self.reddit.submission(id=self.submisId)
        else:
            submission = self.reddit.submission(url=self.submisId)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            try:
                self.newTree.insert('', 'end', comment.id, text=comment.body)
            except:
                self.newTree.insert('', 'end', comment.id, text="CHARACTER ERROR")
            # For each top level comment, recursively build trees for their replies
            self.recursiveTreeBuilder(comment, comment.id)
        self.attachTree()

    def attachTree(self):
        ''' After a new tree is built, replaces the old comment tree with the new one '''
        self.commentTree = self.newTree
        self.yscrollbarComment = ttk.Scrollbar(self, orient='vertical', command=self.commentTree.yview)
        self.commentTree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        self.yscrollbarComment.grid(row=0, column=0, sticky='nse')
        self.commentTree.configure(yscrollcommand=self.yscrollbarComment.set)

    def recursiveTreeBuilder(self, parent, parent_id):
        ''' Recursive method for building trees for replies '''
        for child in parent.replies:
            try:
                self.newTree.insert(parent_id, 'end', child.id, text=child.body)
            except:
                self.newTree.insert(parent_id, 'end', child.id, text="CHARACTER ERROR")
            self.recursiveTreeBuilder(child, child.id)

class ResponseCommentTreeDisplay(CommentTreeDisplay):
    ''' Subclass of CommentTreeDisplay able to respond to comments '''
    def __init__(self, parent, reddit, id, method):
        CommentTreeDisplay.__init__(self, parent, reddit, id, method)
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
        try:
            item = self.commentTree.selection()[0]
            comment = self.reddit.comment(id = item)
            reply = simpledialog.askstring(title = "Add comment", prompt = "Type your comment below:")
            try:
                comment.reply(reply)
            except:
                print("Empty string detected!")
        except: pass


def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )

    root = tk.Tk()
    root.geometry('1280x720')

    queue = SubmissionQueue()
    prod = RedditStream('all', reddit, queue)
    n = ttk.Notebook(root)
    n.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    inc_subm = IncomingSubmissions(root, reddit, queue, n)
    inc_subm.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


    root.mainloop()

if __name__ == "__main__":
    main()
