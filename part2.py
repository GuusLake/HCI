#!/usr/bin/python3
# File name: part2.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N ()
# Date: 26-02-20

import praw
import tkinter as tk
import time
import queue

class CommentTreeDisplay(tk.Frame, reddit):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
               
        self.topframe = tk.Frame(self)
        self.entry = tk.Entry(self)
        self.entry.pack(fill=tk.X, side="left", expand=True)
        self.button = tk.Button(self,text = "Get Comments")
        self.button.pack(side="right", fill=tk.X)
        
        self.botframe = tk.Frame(self)
        self.commentTree = ttk.Treeview(self.botframe)
        self.vsb = tk.Scrollbar(self.botframe, orient="vertical",command=self.commentTree.yview)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.botframe.pack() 
        
    #def showComments(reddit):
        

def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    st = CommentTreeDisplay(root, reddit)
    st.pack()

if __name__ == "__main__":
    main()
