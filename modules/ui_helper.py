#import required modules
import tkinter as tk
from tkinter import simpledialog

#get user input from the GUI
def get_input(title, prompt):
    ROOT = tk.Tk()
    ROOT.withdraw()
    user_input = simpledialog.askstring(title=title,prompt=prompt)
    return user_input