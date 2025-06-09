import tkinter as tk
from tkinter import ttk


class FlashCardStatistics(tk.LabelFrame):
    def __init__(self, mainFrame):
        super().__init__(mainFrame, text='stats', width=750, height=200)

        options = {'pady': 10, 'padx': 10}

        self.questionNumber = ttk.Label(self, text='Question #', width=30)
        self.rightQuestions = ttk.Label(self, text='Right: 0', width=25)
        self.wrongQuestions = ttk.Label(self, text='Wrong: 0', width=25)
        self.time = ttk.Label(self, text='00:00')

        self.questionNumber.grid(row=0, column=0, columnspan=2, **options)
        self.rightQuestions.grid(row=0, column=2, columnspan=2, **options)
        self.wrongQuestions.grid(row=0, column=4, columnspan=2, **options)
        self.time.grid(row=0, column=6, **options)

        self.pack()
        self.pack_propagate(0)