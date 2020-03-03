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
from part3 import ResponseCommentTreeDisplay


class updateTreeDisplay(ResponseCommentTreeDisplay):
    def __init__(self, parent, reddit):
        ResponseCommentTreeDisplay.__init__(self, parent, reddit)
        print("Init complete")
        self.update_slider = tk.Scale(self, from_=1, to=100, orient='horizontal', label='Select time between looking for updates in seconds')
        self.update_slider.set(10)
        self.update_slider.grid(column=0, row=1, columnspan=3, sticky = tk.NSEW)
    
    def update_tree()
        
def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    root.attributes('-zoomed', True)
    ctd = ResponseCommentTreeDisplay(root, reddit)
    ctd.pack(fill=tk.BOTH, expand = True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
