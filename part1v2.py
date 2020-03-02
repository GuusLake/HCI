#!/usr/bin/python3
# File name: part1.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N (s3133125)
# Date: 26-02-20

import praw
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import time
import threading
import queue

class RedditStream:
    def __init__(self, sub, reddit, q):
        self.subreddit = reddit.subreddit(sub)
        self.queue = q
        threading.Thread(target=self.redditLoop).start()
        self.lastsubmission = None
    
    def redditLoop(self):
        while True:
            for submission in self.subreddit.new(limit=1):
                if submission.fullname != self.lastsubmission:
                    self.lastsubmission = submission.fullname
                    self.queue.sendItem([submission.title, submission.subreddit.display_name])
            time.sleep(0.001)

class SubmissionQueue:
    def __init__(self, maxsize =100):
        self.myqueue=queue.Queue(maxsize)

    def sendItem(self,item):
        self.myqueue.put(item, block=True)

    def getNextItem(self):
        message=self.myqueue.get(block=False)
        return message


class IncomingSubmissions(tk.Frame):
    def __init__(self, parent, reddit, q):
        tk.Frame.__init__(self, parent)
        
        # Tree
        self.columnconfigure(0, weight=1)
        self.reddit = reddit
        self.queue = q
        self.tree = ttk.Treeview(self, columns=('title'))
        self.yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.grid(row=0, column=2, sticky='nse')
        self.tree.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        
        # Time slider and play/pause
        self.paused = False
        self.time_slider = tk.Scale(self, from_=1, to=60, orient='horizontal')
        self.time_slider.set(10)
        self.time_slider.grid(column=0, row=1, columnspan=2, sticky = tk.NSEW)
        self.buttonPause = tk.Button(self, text = "Pause", command = self.pause)
        self.buttonPause.grid(column=2, row=1, sticky = tk.EW)
        
        # White/Blacklist
        self.wbList = []
        self.listType = 'Whitelist'
        self.listString = tk.StringVar()
        self.listEntry = tk.Entry(self, textvariable=self.listString)
        self.listString.set("Enter subreddits to white/blacklist seperated by a comma")
        self.listEntry.grid(column=0, row=2, sticky= tk.NSEW)
        self.buttonListType = tk.Button(self, text = "Whitelist", command = self.changeListType)
        self.buttonListType.grid(column=1, row=2, sticky = tk.EW)
        self.buttonListSubmit = tk.Button(self, text = "Submit", command = self.changeListStart)
        self.buttonListSubmit.grid(column=2, row=2, sticky = tk.EW)
        
        
        
        self.after(self.time_slider.get()*10, self.checkQueue)
    
    def checkQueue(self):
        if not self.paused:
            # print("Checking queue...")
            try:
                # Do something with submissions, add them into treeview
                [title, subreddit] = self.queue.getNextItem()
                if self.wbList:
                    if (self.listType == 'Whitelist'):
                        if (subreddit in self.wbList):
                            self.tree.insert('', 'end', text=title,values=(subreddit))
                            self.tree.yview_moveto(1)
                    else:
                        if (subreddit not in self.wbList):
                            self.tree.insert('', 'end', text=title,values=(subreddit))
                            self.tree.yview_moveto(1)
                else:
                    self.tree.insert('', 'end', text=title,values=(subreddit))
                    self.tree.yview(1)
                    
            except: pass
        self.after(self.time_slider.get(), self.checkQueue)
        
    def pause(self):
        if self.paused:
            self.paused = False
            self.buttonPause.config(text='Pause')
        else:
            self.paused = True
            self.buttonPause.config(text='Resume')
            
    def changeListType(self):
        if (self.listType == 'Whitelist'):
            self.buttonListType.config(text='Blacklist')
        else:
            self.buttonListType.config(text='Whitelist')
            
    def changeListStart(self):
        threading.Thread(target=self.changeList).start()
            
    def changeList(self):
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
        reddit (obj): reddit object
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
        

def main():
    
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    
    queue = SubmissionQueue()
    prod = RedditStream('all', reddit, queue)
    inc_subm = IncomingSubmissions(root, reddit, queue)
    inc_subm.pack()
    
    root.mainloop()
    

if __name__ == "__main__":
    main()
