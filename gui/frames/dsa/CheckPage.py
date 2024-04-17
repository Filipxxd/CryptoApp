from tkinter import messagebox

from customtkinter import *

from core.crypts.DSACrypt import DSACrypt
from gui.shared.dialogs import FileDialogs
from gui.shared.widgets.FileEntry import FileEntry


class CheckFrame(CTkFrame):
    def __init__(self, parent, return_frame: CTkFrame):
        CTkFrame.__init__(self, parent, fg_color='transparent')

        self.return_frame = return_frame
        self.zip_file_path = StringVar()
        self.public_key_path = StringVar()

        signed_file_frame = CTkFrame(self, corner_radius=10)
        signed_file_frame.grid(row=0, column=0, pady=(10, 0))

        zip_file_path_frame = FileEntry(signed_file_frame,
                                        self.zip_file_path,
                                        'Vybrat archiv',
                                        'Podepsaný Soubor (Archiv)',
                                        lambda: FileExtensions.ask_file(self.zip_file_path,
                                                                        'Vyberte Podepsaný Archiv Se Souborem',
                                                                        [('ZIP Archiv',
                                                                          f'*.{DSACrypt().ext_archive}')]))
        zip_file_path_frame.grid(row=0, column=0, pady=(0, 15), sticky='w')

        public_key_frame = CTkFrame(self, corner_radius=10)
        public_key_frame.grid(row=1, column=0, pady=(10, 0))

        public_key_path_frame = FileEntry(public_key_frame,
                                          self.public_key_path,
                                          'Vybrat klíč',
                                          'Veřejný Klíč',
                                          lambda: FileExtensions.ask_file(self.public_key_path,
                                                                          'Vyberte Veřejný Klíč',
                                                                          [('Veřejný klíč',
                                                                            f'*.{DSACrypt().ext_public}')]))
        public_key_path_frame.grid(row=0, column=0, pady=(0, 15), sticky='w')

        control_btn_frame = CTkFrame(self, fg_color='transparent')
        control_btn_frame.grid(row=2, column=0, pady=(260, 0))

        back_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Zpět',
            command=lambda: self.__return_back()
        )
        back_btn.grid(row=0, column=0, padx=(0, 130))

        key_gen_btn = CTkButton(
            control_btn_frame,
            corner_radius=5,
            text='Zkontrolovat Podpis',
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
                messagebox.showwarning('Upozornění', 'Musí být zadána správná cesta k archivu.')
                return

            if not self.public_key_path.get():
                messagebox.showwarning('Upozornění', 'Musí být zadána správná cesta k veřejnému klíči.')
                return

            result = DSACrypt().check_signature(self.zip_file_path.get(), self.public_key_path.get())

            if result:
                messagebox.showinfo('Úspěch', 'Podpis je PLATNÝ.')
            else:
                messagebox.showerror('Upozornění', 'Podpis je NEPLATNÝ.')

        except Exception as ex:
            print(str(ex))
            messagebox.showerror('Upozornění', 'Podpis nelze ověřit.')

        self.__return_back()
