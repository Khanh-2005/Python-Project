import tkinter as tk
from tkinter import messagebox
import json


def questionOptions(filePath):
    with open(filePath, 'r') as questionData:
        data = json.load(questionData)
        return data


questionNum = 1
options = questionOptions('questionData.json')


class OptionFrame(tk.LabelFrame):
    def __init__(self, mainframe, termFrame):
        super().__init__(mainframe, text='answers', width=750, height=250, labelanchor='s', bd=5)
        self.termFrame = termFrame

        def checkAnswer(selectedOption):
            global questionNum
            if selectedOption == self.correctAnswer:
                messagebox.showinfo('Result', 'Correct!')

            else:
                messagebox.showinfo('Result', 'Incorrect!')

            questionNum += 1
            updateOptions()
            self.correctAnswer = options[f'Question{questionNum}']['answer']
            self.termFrame.updateTerm()

        self.correctAnswer = options[f'Question{questionNum}']['answer']

        self.buttons = []
        position = [[0, 0], [0, 2], [2, 0], [2, 2]]
        padding = [[(10, 20), (10, 20)],
                   [(0, 10), (10, 20)],
                   [(10, 20), (0, 10)],
                   [(0, 10), (0, 20)],
                   ]

        def updateOptions():
            for i in range(len(self.buttons)):
                self.buttons[i].config(text=options[f'Question{questionNum}']['options'][f'option{i + 1}'])

        for i, option in enumerate(options[f'Question{questionNum}']['options']):
            button = tk.Button(
                self,
                text=options[f'Question{questionNum}']['options'][f'option{i + 1}'],
                width=50,
                height=10,
                bg='black',
                fg='red',
                relief='flat',  # làm phẳng nút, tránh viền theme
                highlightthickness=0,  # bỏ viền nền đè
                bd=1,  # đường viền mỏng
                activebackground='#e6e6e6',  # màu khi hover
                command=lambda opt=option: checkAnswer(opt)
            )
            self.buttons.append(button)

            button.grid(
                row=position[i][0],
                column=position[i][1],
                rowspan=2,
                columnspan=2,
                padx=padding[i][0],
                pady=padding[i][1]
            )

        self.pack()
        self.pack_propagate(0)