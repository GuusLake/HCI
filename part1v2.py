#!/usr/bin/python3
# File name: part1.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N (s3133125)
# Date: 26-02-20

import praw
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
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
        self.reddit = reddit
        self.queue = q
        self.tree = ttk.Treeview(self, columns=('title'))
        self.tree.pack(fill=tk.BOTH)
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Whitelist")
        self.filemenu.add_command(label="Load Blacklist")
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        parent.config(menu=self.menubar)
        self.paused = False
        self.button = tk.Button(self, text = "Pause", command = self.pause)
        self.button.pack()
        self.time_slider = tk.Scale(self, from_=1, to=60)
        self.time_slider.set(10)
        self.time_slider.pack()
        
        self.after(self.time_slider.get(), self.checkQueue)
    
    def checkQueue(self):
        if not self.paused:
            # print("Checking queue...")
            try:
                # Do something with submissions, yeet them into treeview
                [title, subreddit] = self.queue.getNextItem()
                self.tree.insert('', 'end', text=title,values=(subreddit))
                self.tree.yview_moveto(1)
            except: pass
        self.after(self.time_slider.get(), self.checkQueue)
        
    def pause(self):
        if self.paused:
            self.paused = False
            self.button.config(text='Pause')
        else:
            self.paused = True
            self.button.config(text='Resume')
            
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
            try:
                # Try to do a subreddit exact search
                self.reddit.subreddits.search_by_name(subreddit, exact=True)
            except:
                # If it fails return False
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
