from customtkinter import CTkButton, CTkFrame

from GUI.Base.FrameBase import FrameBase
from GUI.Frames.DSA.CheckFrame import CheckFrame
from GUI.Frames.DSA.SignFrame import SignFrame


class DSAFrame(FrameBase):
    def __init__(self, parent: CTkFrame, return_frame: CTkFrame):
        FrameBase.__init__(self, parent)
        self.return_frame = return_frame

        container_frame = FrameBase(self)
        sign_page = SignFrame(self, container_frame)
        check_page = CheckFrame(self, container_frame)

        buttons_frame = CTkFrame(container_frame)
        buttons_frame.grid(row=0, column=0)

        sign_page_btn = CTkButton(
            buttons_frame,
            text='Podepsat Soubor',
            command=lambda: sign_page.tkraise()
        )
        sign_page_btn.grid(row=0, column=0)

        check_page_btn = CTkButton(
            buttons_frame,
            text='Zkontrolovat Podpis',
            command=lambda: check_page.tkraise()
        )
        check_page_btn.grid(row=1, column=0, pady=10)

        back_btn = CTkButton(
            buttons_frame,
            text='Zpět',
            command=lambda: self.return_frame.tkraise()
        )
        back_btn.grid(row=2, column=0)

        container_frame.tkraise()
