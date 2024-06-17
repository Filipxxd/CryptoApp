from tkinter import messagebox

from customtkinter import *

from Crypts.DSACrypt import DSACrypt
from GUI.Base.PageFrame import PageFrame
from GUI.Frames.DSA import FileDialogs
from GUI.Shared.FileEntry import FileEntry


class CheckPageFrame(PageFrame):
    def __init__(self, parent, return_frame: CTkFrame):
        super().__init__(parent)

        self.crypt = DSACrypt()
        self.return_frame = return_frame

        self.zip_file_path = StringVar()
        self.public_key_path = StringVar()

        signed_file_frame = CTkFrame(self, corner_radius=10)
        signed_file_frame.grid(row=0, column=0, pady=(10, 0))

        zip_file_path_frame = FileEntry(signed_file_frame,
                                        self.zip_file_path,
                                        'Choose Archive',
                                        'Signed File (Archive)',
                                        lambda: FileDialogs.ask_file(self.zip_file_path,
                                                                     'Choose Archive with signed file',
                                                                     [('zip',
                                                                       f'*.{self.crypt.ext_archive}')]))
        zip_file_path_frame.grid(row=0, column=0, pady=(0, 15), sticky='w')

        public_key_frame = CTkFrame(self, corner_radius=10)
        public_key_frame.grid(row=1, column=0, pady=(10, 0))

        public_key_path_frame = FileEntry(public_key_frame,
                                          self.public_key_path,
                                          'Choose Key',
                                          'Choose Public Key',
                                          lambda: FileDialogs.ask_file(self.public_key_path,
                                                                       'Choose Public Key',
                                                                       [('Public Key',
                                                                         f'*.{self.crypt.ext_public}')]))
        public_key_path_frame.grid(row=0, column=0, pady=(0, 15), sticky='w')

        control_btn_frame = CTkFrame(self, fg_color='transparent')
        control_btn_frame.grid(row=2, column=0, pady=(260, 0))

        back_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Back',
            command=lambda: self.__return_back()
        )
        back_btn.grid(row=0, column=0, padx=(0, 130))

        key_gen_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Check Signature',
            command=lambda: self.__check_signature()
        )
        key_gen_btn.grid(row=0, column=1, padx=(130, 0))

    def __return_back(self):
        self.zip_file_path.set('')
        self.public_key_path.set('')
        self.return_frame.tkraise()

    def __check_signature(self):
        try:
            if not self.zip_file_path.get():
                messagebox.showwarning('Warning', 'Path to archive must be supplied.')
                return

            if not self.public_key_path.get():
                messagebox.showwarning('Warning', 'Path to public key must be supplied.')
                return

            result = self.crypt.check_signature(self.zip_file_path.get(), self.public_key_path.get())

            if result:
                messagebox.showinfo('Success', 'Signature is valid.')
            else:
                messagebox.showerror('Warning', 'Signature is not valid.')

        except Exception as ex:
            print(str(ex))
            messagebox.showerror('Warning', 'Signature cannot be verified.')

        self.__return_back()
