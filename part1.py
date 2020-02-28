#!/usr/bin/python3
# File name: part1.py
# 
# Authors: Lakeman, G (s3383180) and Algra, N ()
# Date: 26-02-20

import praw
import tkinter as tk
import time

class timeOut:
    
    def __init__(self):
        self.timer = 100
        
    def setTimer(self, t):
        self.timer = t

    def getTimer(self):
        return self.timer
    
class IncomingSubmissions(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        
        

def main():
    reddit = praw.Reddit(client_id='DgNtrLuFrdzL5Q',
                         client_secret='CJZQjr6En6GpsYOEFVPdWAwwW7w',
                         user_agent='Part1 by /u/guusnick',
                         username = 'guusnick',
                         password = 'Groningen2020'
                         )
    
    root = tk.Tk()
    

if __name__ == "__main__":
    main()
