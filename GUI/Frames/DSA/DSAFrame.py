from customtkinter import CTkButton, CTkFrame

from GUI.Base.PageFrame import PageFrame
from GUI.Frames.DSA.CheckFrame import CheckPageFrame
from GUI.Frames.DSA.SignFrame import SignPageFrame


class DSAPageFrame(PageFrame):
    def __init__(self, parent: CTkFrame, return_frame: CTkFrame):
        super().__init__(parent)
        self.return_frame = return_frame

        container_frame = PageFrame(self)
        sign_page = SignPageFrame(self, container_frame)
        check_page = CheckPageFrame(self, container_frame)

        buttons_frame = CTkFrame(container_frame)
        buttons_frame.grid(row=0, column=0)

        sign_page_btn = CTkButton(
            buttons_frame,
            text='Sign File',
            command=lambda: sign_page.tkraise()
        )
        sign_page_btn.grid(row=0, column=0)

        check_page_btn = CTkButton(
            buttons_frame,
            text='Check Signature',
            command=lambda: check_page.tkraise()
        )
        check_page_btn.grid(row=1, column=0, pady=10)

        back_btn = CTkButton(
            buttons_frame,
            text='Back',
            command=lambda: self.return_frame.tkraise()
        )
        back_btn.grid(row=2, column=0)

        container_frame.tkraise()
