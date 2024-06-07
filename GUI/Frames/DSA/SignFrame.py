import tkinter as tk
from glob import glob
from tkinter import messagebox

from customtkinter import *
from datetime import datetime

from core.crypts.DSACrypt import DSACrypt
from GUI.Base.FrameBase import FrameBase
from GUI.Shared import FileDialogs
from GUI.Shared.FileEntry import FileEntry
from core.ValidationError import ValidationError


class SignFrame(FrameBase):
    def __init__(self, parent: CTkFrame, return_frame: CTkFrame):
        FrameBase.__init__(self, parent)

        self.return_frame = return_frame

        self.private_key_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.file_path = tk.StringVar()
        self.file_size = tk.StringVar()
        self.time_created = tk.StringVar()
        self.time_updated = tk.StringVar()
        self.name = tk.StringVar()
        self.type = tk.StringVar()

        signature_file_frame = CTkFrame(self, corner_radius=10)
        signature_file_frame.grid(row=0, column=0)

        file_path_frame = FileEntry(signature_file_frame,
                                    self.file_path,
                                    'Vybrat soubor',
                                    'Podepisovaný Soubor',
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
                                'Vybrat složku',
                                'Výstupní Adresář',
                                lambda: FileDialogs.ask_directory(self.output_path, 'Vyberte složku'))
        output_path.grid(row=0, column=0, pady=(0, 15), sticky='w')

        key_file_frame = CTkFrame(self, corner_radius=10)
        key_file_frame.grid(row=1, column=0, pady=(10, 0))

        key_path_frame = FileEntry(key_file_frame,
                                   self.private_key_path,
                                   'Vybrat klíč',
                                   'Soukromý Klíč',
                                   lambda: FileDialogs.ask_file(self.private_key_path,
                                                                'Vyberte Soukromý Klíč',
                                                                [('Soukromý klíč',
                                                                  f'*.{DSACrypt().ext_private}')]))
        key_path_frame.grid(row=0, column=0, pady=(0, 15), sticky='w')

        control_btn_frame = CTkFrame(self, fg_color='transparent')
        control_btn_frame.grid(row=7, column=0, pady=(10, 0))

        back_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Zpět',
            command=lambda: self.__return_back()
        )
        back_btn.grid(row=0, column=0, padx=(0, 60))

        key_gen_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Generovat Klíče',
            command=lambda: self.__create_keys()
        )
        key_gen_btn.grid(row=0, column=1)

        key_gen_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Podepsat Soubor',
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
                messagebox.showwarning('Upozornění', 'Musí být zadána výstupní složka.')
                return

            crypt = (DSACrypt(path))
            crypt.get_key_files()

            messagebox.showinfo('Úspěch', 'Klíče úspěšně vygenerovány.')

            key_files = glob(f'{path}/*.{crypt.ext_private}')
            latest_private = max(key_files, key=os.path.getmtime)
            self.private_key_path.set(f'{latest_private}'.replace('\\', '/'))

        except ValidationError:
            messagebox.showerror('Upozornění', 'Klíče nelze vygenerovat.')

    def __sign_file(self):
        try:
            if not os.path.lexists(self.output_path.get()):
                messagebox.showwarning('Upozornění', 'Musí být zadána výstupní složka.')
                return

            if not os.path.lexists(self.file_path.get()):
                messagebox.showwarning('Upozornění', 'Musí být zadána správná cesta k souboru.')
                return

            if not os.path.lexists(self.private_key_path.get()):
                messagebox.showwarning('Upozornění', 'Musí být zadána správná cesta k privátnímu klíči.')
                return

            DSACrypt(self.output_path.get()).sign_file(self.file_path.get(), self.private_key_path.get())
            messagebox.showinfo('Úspěch', 'Soubor úspěšně podepsán.')

        except ValidationError:
            messagebox.showerror('Upozornění', 'Soubor nelze podepsat.')

        self.__return_back()

    def __select_file(self):
        FileDialogs.ask_file(self.file_path,
                             'Vyberte soubor k podpisu',
                             [('Všechny soubory', f'*')])

        path = self.file_path.get()

        if not os.path.lexists(path):
            return

        self.file_path.set(path)

        name = os.path.basename(path).split('.')
        self.name.set(f'Název: {name[0]}')
        self.type.set(f'Přípona: {name[1]}')
        self.file_size.set(f'Velikost souboru: {os.path.getsize(path)} B')

        datetime_created = datetime.fromtimestamp(os.path.getctime(path)).strftime('%d/%m/%Y %H:%M:%S')
        self.time_created.set(f'Datum vytvoření: {datetime_created}')
        datetime_updated = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d/%m/%Y %H:%M:%S')
        self.time_updated.set(f'Datum aktualizace: {datetime_updated}')
