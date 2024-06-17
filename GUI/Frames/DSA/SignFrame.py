import os
from glob import glob
from tkinter import messagebox, StringVar

from customtkinter import CTkFrame, CTkLabel, CTkButton
from datetime import datetime

from Crypts.DSACrypt import DSACrypt
from GUI.Base.PageFrame import PageFrame
from GUI.Frames.DSA import FileDialogs
from GUI.Shared.FileEntry import FileEntry
from Exceptions.ValidationError import ValidationError


class SignPageFrame(PageFrame):
    def __init__(self, parent: CTkFrame, return_frame: CTkFrame):
        super().__init__(parent)

        self.crypt = DSACrypt()

        self.return_frame = return_frame

        self.private_key_path = StringVar()
        self.output_path = StringVar()
        self.file_path = StringVar()
        self.file_size = StringVar()
        self.time_created = StringVar()
        self.time_updated = StringVar()
        self.name = StringVar()
        self.type = StringVar()

        signature_file_frame = CTkFrame(self, corner_radius=10)
        signature_file_frame.grid(row=0, column=0)

        file_path_frame = FileEntry(signature_file_frame,
                                    self.file_path,
                                    'Choose File',
                                    'File to Sign',
                                    self.__select_file)
        file_path_frame.grid(row=0, column=0)

        file_info_frame = CTkFrame(signature_file_frame, fg_color='transparent')
        file_info_frame.grid(row=1, column=0, padx=(30, 0), pady=(0, 20), sticky='w')

        name_label = CTkLabel(file_info_frame, textvariable=self.name)
        name_label.grid(row=0, column=0, sticky='w')

        type_label = CTkLabel(file_info_frame, textvariable=self.type)
        type_label.grid(row=1, column=0, sticky='w')

        file_size_label = CTkLabel(file_info_frame, textvariable=self.file_size)
        file_size_label.grid(row=2, column=0, sticky='w')

        time_created_label = CTkLabel(file_info_frame, textvariable=self.time_created)
        time_created_label.grid(row=3, column=0, sticky='w')

        time_updated_label = CTkLabel(file_info_frame, textvariable=self.time_updated)
        time_updated_label.grid(row=4, column=0, sticky='w')

        output_folder_frame = CTkFrame(self, corner_radius=10)
        output_folder_frame.grid(row=5, column=0, pady=(10, 0))

        output_path = FileEntry(output_folder_frame,
                                self.output_path,
                                'Choose Directory',
                                'Output Directory',
                                lambda: FileDialogs.ask_directory(self.output_path, 'Choose Directory'))
        output_path.grid(row=0, column=0, pady=(0, 15), sticky='w')

        key_file_frame = CTkFrame(self, corner_radius=10)
        key_file_frame.grid(row=1, column=0, pady=(10, 0))

        key_path_frame = FileEntry(key_file_frame,
                                   self.private_key_path,
                                   'Choose Key',
                                   'Private Key',
                                   lambda: FileDialogs.ask_file(self.private_key_path,
                                                                'Choose Private Key',
                                                                [('Private Key',
                                                                  f'*.{self.crypt.ext_private}')]))
        key_path_frame.grid(row=0, column=0, pady=(0, 15), sticky='w')

        control_btn_frame = CTkFrame(self, fg_color='transparent')
        control_btn_frame.grid(row=7, column=0, pady=(10, 0))

        back_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Back',
            command=lambda: self.__return_back()
        )
        back_btn.grid(row=0, column=0, padx=(0, 60))

        key_gen_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Generate Keys',
            command=lambda: self.__create_keys()
        )
        key_gen_btn.grid(row=0, column=1)

        key_gen_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Sign File',
            command=lambda: self.__sign_file()
        )
        key_gen_btn.grid(row=0, column=2, padx=(60, 0))

    def __return_back(self):
        self.private_key_path.set('')
        self.output_path.set('')
        self.file_path.set('')
        self.file_size.set('')
        self.time_created.set('')
        self.time_updated.set('')
        self.name.set('')
        self.type.set('')
        self.return_frame.tkraise()

    def __create_keys(self):
        try:
            path = self.output_path.get()

            if not os.path.lexists(path):
                messagebox.showwarning('Warning', 'Output folder must be supplied.')
                return

            self.crypt.output_folder = path
            self.crypt.get_key_files()

            messagebox.showinfo('Success', 'Keys created successfully.')

            key_files = glob(f'{path}/*.{self.crypt.ext_private}')
            latest_private = max(key_files, key=os.path.getmtime)
            self.private_key_path.set(f'{latest_private}'.replace('\\', '/'))

        except ValidationError:
            messagebox.showerror('Warning', 'Keys cannot be generated.')

    def __sign_file(self):
        try:
            if not os.path.lexists(self.output_path.get()):
                messagebox.showwarning('Warning', 'Output folder must be supplied.')
                return

            if not os.path.lexists(self.file_path.get()):
                messagebox.showwarning('Warning', 'Path to file must be supplied.')
                return

            if not os.path.lexists(self.private_key_path.get()):
                messagebox.showwarning('Warning', 'Path to private key must be supplied.')
                return

            self.crypt.output_folder = self.output_path.get()
            self.crypt.sign_file(self.file_path.get(), self.private_key_path.get())

            messagebox.showinfo('Success', 'File signed successfully.')

        except ValidationError:
            messagebox.showerror('Warning', 'File cannot be signed.')

        self.__return_back()

    def __select_file(self):
        FileDialogs.ask_file(self.file_path,
                             'Choose file to be signed',
                             [('All Files', f'*')])

        path = self.file_path.get()

        if not os.path.lexists(path):
            return

        self.file_path.set(path)

        name = os.path.basename(path).split('.')
        self.name.set(f'Name: {name[0]}')
        self.type.set(f'Extension: {name[1]}')
        self.file_size.set(f'File Size: {os.path.getsize(path)} B')

        datetime_created = datetime.fromtimestamp(os.path.getctime(path)).strftime('%d/%m/%Y %H:%M:%S')
        self.time_created.set(f'Date Created: {datetime_created}')
        datetime_updated = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d/%m/%Y %H:%M:%S')
        self.time_updated.set(f'Date Updated: {datetime_updated}')
