#!/usr/bin/env python
import tkinter as tk
import tkinter.scrolledtext

class GuiTextArea(object):
    myGUI = None
    myOutput = None

    # --------------------
    def __init__(self, title):

        # Create and set up the window
        self.myGUI = tk.Tk()
        self.myGUI.title(title)
        self.myOutput = tk.scrolledtext.ScrolledText(self.myGUI)

        # Display the window.
        self.myOutput.pack()

    # --------------------
    def print(self, s):
        self.myOutput.configure(state ='normal')
        self.myOutput.insert(tk.END, s)
        self.myOutput.configure(state ='disabled')

    def println(self, s=""):
        self.print(s + "\n")
