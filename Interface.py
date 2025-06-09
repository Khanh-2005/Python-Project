import tkinter as tk
from tkinter import ttk

import MainFrame
import sv_ttk
from MainFrame import *

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashard")
        self.geometry("800x600")


if __name__ == "__main__":
    interface = Interface()

    sv_ttk.set_theme('dark')
    MainFrame(interface)
    interface.mainloop()