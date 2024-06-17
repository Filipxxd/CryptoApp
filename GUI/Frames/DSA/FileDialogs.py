import os
from tkinter import StringVar, filedialog


def ask_directory(variable: StringVar, title: str):
    path = filedialog.askdirectory(title=title,
                                   mustexist=True,
                                   initialdir=os.getcwd())
    variable.set(path)


def ask_file(variable: StringVar, title: str, filetypes: list[tuple[str, str]]):
    path = filedialog.askopenfilename(title=title,
                                      initialdir=os.getcwd(),
                                      filetypes=filetypes)
    variable.set(path)
