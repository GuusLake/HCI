#!/usr/bin/python3
# File name: part1.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N ()
# Date: 26-02-20

import praw
import tkinter as tk
import time
import queue

class updateTimer:
    
    def __init__(self):
        self.timer = 10
        self.paused = False

    def setTimer(self, t):
        self.timer = t

    def getTimer(self):
        return self.timer
    
    def pause(self):
        self.paused = True
    
    def play(self):
        self.paused = False
        
    def checkPause(self):
        return self.paused
        
def checkSubreddits(reddit, subredditList):
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
            reddit.subreddits.search_by_name(subreddit, exact=True)
        except:
            # If it fails return False
            return False
    return True
        

def updateLoop(timer, reddit):
    
    while(1):
        if (not(timer.checkPause())):
            # ADD reddit posts
            time.sleep(timer.getTimer())
            

class IncomingSubmissions(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.topframe = tk.Frame(self)
        self.time_slider = tk.Scale(self.topframe, from_=1, to=60)
        self.time_slider.set(10)
        self.btn = tk.Button(self.topframe, text='Play/Pause')
        self.topframe.pack()
    
    

def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    loadQueue = queue.Queue(maxsize = 10)
    
    root = tk.Tk()
    st = IncomingSubmissions(root)
    st.pack()
    root.mainloop()
    self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Whitelist")
        self.filemenu.add_command(label="Load Blacklist")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

if __name__ == "__main__":
    main()
