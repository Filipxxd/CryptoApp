from customtkinter import CTkButton, CTkFrame, CTk

from GUI.Base.FrameBase import FrameBase
from GUI.Frames.DSA.DSAFrame import DSAFrame


class AppGUI(CTk):
    def __init__(self):
        super().__init__()

        window = CTkFrame(self, fg_color='transparent')
        window.grid(row=0, column=0)

        home_frame = FrameBase(window)
        dsa_frame = DSAFrame(window, home_frame)

        buttons_frame = CTkFrame(home_frame)
        buttons_frame.grid(row=0, column=0)

        dsa_open_btn = CTkButton(
            buttons_frame,
            text='DSA - Podpis Souborů',
            command=lambda: dsa_frame.tkraise()
        )
        dsa_open_btn.grid(row=0, column=0)

        close_program_btn = CTkButton(
            buttons_frame,
            text='Ukončit Program',
            command=lambda: self.destroy()
        )
        close_program_btn.grid(row=1, column=0)

        home_frame.tkraise()
