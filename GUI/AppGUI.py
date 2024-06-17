from customtkinter import CTkButton, CTkFrame, CTk

from GUI.Base.PageFrame import PageFrame
from GUI.Frames.ADFGvXFrame import ADFGvXFrame
from GUI.Frames.AffineFrame import AffineFrame
from GUI.Frames.DSA.DSAFrame import DSAPageFrame
from GUI.Frames.PlayfairFrame import PlayfairFrame
from GUI.Frames.RSAFrame import RSAFrame


class AppGUI(CTk):
    def __init__(self):
        super().__init__()

        root = CTkFrame(self, fg_color='transparent')
        root.grid(row=0, column=0, sticky='nsew')

        home_frame = PageFrame(root)
        dsa_frame = DSAPageFrame(root, home_frame)
        rsa_frame = RSAFrame(root, home_frame)
        adfgvx_frame = ADFGvXFrame(root, home_frame)
        playfair_frame = PlayfairFrame(root, home_frame)
        affine_frame = AffineFrame(root, home_frame)

        buttons_frame = CTkFrame(home_frame)
        buttons_frame.grid(row=0, column=0)

        CTkButton(
            buttons_frame,
            text='DSA',
            command=lambda: dsa_frame.tkraise()
        ).grid(row=0, column=0, pady=7)

        CTkButton(
            buttons_frame,
            text='RSA',
            command=lambda: rsa_frame.tkraise()
        ).grid(row=1, column=0)

        CTkButton(
            buttons_frame,
            text='ADFGVX',
            command=lambda: adfgvx_frame.tkraise()
        ).grid(row=2, column=0, pady=7)

        CTkButton(
            buttons_frame,
            text='Playfair',
            command=lambda: playfair_frame.tkraise()
        ).grid(row=3, column=0)

        CTkButton(
            buttons_frame,
            text='Affine',
            command=lambda: affine_frame.tkraise()
        ).grid(row=4, column=0, pady=7)

        CTkButton(
            buttons_frame,
            text='Exit',
            command=lambda: self.destroy()
        ).grid(row=5, column=0)

        home_frame.tkraise()
