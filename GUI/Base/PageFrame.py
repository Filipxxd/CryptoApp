from customtkinter import CTkFrame


class PageFrame(CTkFrame):
    def __init__(self, parent: CTkFrame):
        super().__init__(parent, fg_color='transparent')
        self.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
