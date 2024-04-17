import tkinter as tk
from typing import Callable

from customtkinter import CTkEntry, CTkLabel, DISABLED, CTkButton, CTkFrame


class FileEntry(CTkFrame):
    def __init__(self, parent, path_var: tk.StringVar, btn_text: str, label_text: str, btn_command: Callable):
        CTkFrame.__init__(self, parent, fg_color='transparent')

        file_path_label = CTkLabel(self, text=label_text, font=('Arial', 13, 'bold'))
        file_path_label.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(5, 0), sticky='w')

        file_path_entry = CTkEntry(self,
                                   state=DISABLED,
                                   textvariable=path_var,
                                   width=400, fg_color='transparent', corner_radius=0, font=('Arial', 12, 'italic'))
        file_path_entry.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=0)

        pick_file_btn = CTkButton(
            self,
            corner_radius=0, fg_color='transparent', font=('Arial', 11),
            border_width=1, text_color=('gray10', '#DCE4EE'), hover_color=('#C1C0C0', '#4B4B4B'),
            text=btn_text,
            command=btn_command
        )
        pick_file_btn.grid(row=1, column=3, padx=(0, 20))
