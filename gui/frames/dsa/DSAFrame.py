from customtkinter import CTkButton, CTkFrame

from gui.frames.dsa.CheckPage import CheckFrame
from gui.frames.dsa.SignPage import SignFrame


class DSAFrame(CTkFrame):
    def __init__(self, parent, return_frame: CTkFrame):
        CTkFrame.__init__(self, parent, fg_color='transparent')

        self.return_frame = return_frame

        home_page = CTkFrame(self, fg_color='transparent')
        home_page.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        sign_page = SignFrame(self, home_page)
        sign_page.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        check_page = CheckFrame(self, home_page)
        check_page.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        home_page.grid_rowconfigure(0, weight=1)
        home_page.grid_columnconfigure(0, weight=1)

        container_frame = CTkFrame(home_page, fg_color='transparent')
        container_frame.grid(row=0, column=0)

        sign_page_btn = CTkButton(
            container_frame,
            text='Podepsat Soubor',
            command=lambda: sign_page.tkraise()
        )
        sign_page_btn.grid(row=0, column=0, pady=(0, 10))

        check_page_btn = CTkButton(
            container_frame,
            text='Zkontrolovat Podpis',
            command=lambda: check_page.tkraise()
        )
        check_page_btn.grid(row=1, column=0, pady=(10, 0))

        home_page.tkraise()