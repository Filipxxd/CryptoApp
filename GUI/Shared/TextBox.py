from customtkinter import CTkTextbox, CTkFrame
from tkinter import StringVar, END, NORMAL, DISABLED


class TextBox(CTkTextbox):
    def __init__(self, master: CTkFrame, height: int, width: int, text_variable: StringVar, state=NORMAL):
        super().__init__(master, height=height, width=width, state=state)
        self.disabled = True if state == DISABLED else False
        self.text_variable = text_variable
        self.trace_active = False

        self.bind('<KeyRelease>', self.__value_changed)
        self.text_variable.trace_add('write', self.__variable_changed)

    def __value_changed(self, *args):
        if not self.trace_active:
            self.trace_active = True
            self.text_variable.set(self.get(1.0, END).strip())
            self.trace_active = False

    def __variable_changed(self, *args):
        if not self.trace_active:
            self.trace_active = True

            if self.disabled:
                self.configure(state=NORMAL)

            self.delete(1.0, END)
            self.insert(1.0, self.text_variable.get())

            if self.disabled:
                self.configure(state=DISABLED)

            self.trace_active = False
