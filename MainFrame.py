import tkinter as tk
from tkinter import ttk
from Statistics import FlashCardStatistics
from term import TermFrame
from options import OptionFrame


class MainFrame(ttk.Frame):
    def __init__(self, flashCardInterferace):
        super().__init__(flashCardInterferace)

        self.TermFrame = TermFrame(self)
        self.OptionFrame = OptionFrame(self, termFrame=self.TermFrame)

        self.pack()