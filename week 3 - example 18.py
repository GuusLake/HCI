import tkinter as tk; import datetime; import time

class MyScrolledTextLog(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)  
        self.topframe = tk.Frame(self)
        self.text = tk.Text(self.topframe, *args, **kwargs)
        self.vsb = tk.Scrollbar(self.topframe, orient="vertical",command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.topframe.pack()        
        self.bottomframe = tk.Frame(self)
        self.entry = tk.Entry(self)
        self.entry.pack(fill=tk.X, side="left", expand=True)
        self.button = tk.Button(self,text = "ADDLOG", command=self.addlog)
        self.button.pack(side="right", fill=tk.X)
    
    def addlog(self):
        prefix = str(datetime.date.today())+str(datetime.datetime.now().time()) +"]"
        self.text.insert(tk.END,prefix+self.entry.get()+"\n")
        self.entry.delete(0,tk.END)
        self.text.see(tk.END)
              
root = tk.Tk()
st = MyScrolledTextLog(root)
st.pack()
root.mainloop()

