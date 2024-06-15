import tkinter as tk
from tkinter import messagebox, DISABLED
import re
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox

from GUI.Base.PageFrame import PageFrame
from Core.Crypts.RSACrypt import RSACrypt
from Core.ValidationError import ValidationError
from GUI.Shared.TextBox import TextBox


class RSAFrame(PageFrame):
    def __init__(self, parent: CTkFrame, return_frame: CTkFrame):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.return_frame = return_frame
        self.crypt = RSACrypt()

        self.input = tk.StringVar()
        self.p_entry = tk.StringVar()
        self.q_entry = tk.StringVar()
        self.modulus_entry = tk.StringVar()
        self.public_entry = tk.StringVar()
        self.private_entry = tk.StringVar()
        self.output = tk.StringVar()

        # Center frame
        center_frame = CTkFrame(self, fg_color='transparent')
        center_frame.grid(row=0, column=0, sticky='n')
        center_frame.grid_columnconfigure(0, weight=1)

        input_frame = CTkFrame(center_frame, fg_color='transparent')
        input_frame.grid(row=0, column=0, columnspan=4, pady=20)
        input_frame.grid_rowconfigure(4, weight=1)

        prime_numbers_frame = CTkFrame(input_frame, fg_color='transparent')
        prime_numbers_frame.grid(row=0, column=0, columnspan=4, pady=5)

        # Prime nums
        CTkLabel(prime_numbers_frame, text='P:').grid(row=0, column=0)
        CTkEntry(prime_numbers_frame, textvariable=self.p_entry, width=140).grid(row=0, column=1, padx=5)

        CTkLabel(prime_numbers_frame, text='Q:').grid(row=0, column=2)
        CTkEntry(prime_numbers_frame, textvariable=self.q_entry, width=140).grid(row=0, column=3, padx=5)

        # Modulus
        CTkLabel(input_frame, text='Modulus (n):').grid(row=1, column=0, pady=5)
        CTkEntry(input_frame, textvariable=self.modulus_entry, width=200).grid(row=1, column=1, columnspan=3, padx=5)

        # Public key
        CTkLabel(input_frame, text='Veřejný Klíč (e):').grid(row=2, column=0, pady=5)
        CTkEntry(input_frame, textvariable=self.public_entry, width=200).grid(row=2, column=1, columnspan=3, padx=5)

        # Private key
        CTkLabel(input_frame, text='Soukromý Klíč (d):').grid(row=3, column=0, pady=5)
        CTkEntry(input_frame, textvariable=self.private_entry, width=200).grid(row=3, column=1, columnspan=3, padx=5)

        # Input
        CTkLabel(input_frame, text='Vstup:').grid(row=4, column=0, pady=5)
        TextBox(input_frame, 200, 100, self.input).grid(row=4, column=1, columnspan=3, padx=5)

        # Buttons
        button_frame = CTkFrame(input_frame, fg_color='transparent')
        button_frame.grid(row=9, column=0, columnspan=4, pady=10)

        CTkButton(button_frame, text='Generovat Q a P', command=self.__generate_primes).grid(row=0, column=0, padx=5)
        CTkButton(button_frame, text='Generovat Klíče', command=self.__generate_keys).grid(row=0, column=1, padx=5)

        CTkButton(button_frame, text='Šifrovat', command=lambda: self.__crypt('encrypt')).grid(row=1, column=0, padx=5)
        CTkButton(button_frame, text='Dešifrovat', command=lambda: self.__crypt('decrypt')).grid(row=1, column=1, padx=5)

        CTkButton(button_frame, text='Zpět', command=lambda: self.__return_back()).grid(row=2, column=0, padx=5)

        # Output
        output_frame = CTkFrame(center_frame, fg_color='transparent')
        output_frame.grid(row=0, column=4, rowspan=6, padx=10, pady=10, sticky='nw')
        output_frame.grid_rowconfigure(1, weight=1)

        CTkLabel(output_frame, text='Výstup:').grid(row=0, column=0, sticky='nw')
        TextBox(output_frame, 200, 200, self.output, DISABLED).grid(row=1, column=0, pady=5)
        CTkButton(output_frame, text='Kopírovat do Vstupu', command=self.__copy_to_input).grid(row=2, column=0)

    def __return_back(self):
        self.input.set('')
        self.p_entry.set('')
        self.q_entry.set('')
        self.modulus_entry.set('')
        self.public_entry.set('')
        self.private_entry.set('')
        self.output.set('')
        self.return_frame.tkraise()

    def __generate_primes(self):
        first = self.crypt.get_random_prime()
        second = self.crypt.get_random_prime()

        while second == first:
            second = self.crypt.get_random_prime()

        self.q_entry.set(str(first))
        self.p_entry.set(str(second))

    def __generate_keys(self):
        try:
            q = self.q_entry.get()
            p = self.p_entry.get()

            public, private = self.crypt.create_keys(self.__get_as_int(q), self.__get_as_int(p))

            self.modulus_entry.set(str(public[0]))
            self.public_entry.set(str(public[1]))
            self.private_entry.set(str(private[1]))

        except ValidationError as ex:
            messagebox.showwarning('Upozornění', str(ex))

        except Exception as ex:
            messagebox.showerror('Nastala chyba', f'Nastala neočekávaná chyba.\n{str(ex)}')

    def __get_as_int(self, input: str) -> int:
        sanitized_input = re.sub(r'[^0-9]', '', input)

        if not sanitized_input:
            raise ValidationError('Nemůže být prázdný!')

        return int(sanitized_input)

    def __crypt(self, mode: str):
        try:
            text = self.input.get()
            modulus = self.__get_as_int(self.modulus_entry.get())

            if mode == 'encrypt':
                public_part = self.__get_as_int(self.public_entry.get())
                text_output = self.crypt.encrypt(text, (modulus, public_part))
                text_output = ' '.join(
                    [text_output[i:i + len(str(modulus))] for i in range(0, len(text_output), len(str(modulus)))])
            else:
                private_part = self.__get_as_int(self.private_entry.get())
                text_output = self.crypt.decrypt(text, (modulus, private_part))

            self.output.set(text_output)

        except ValidationError as ex:
            messagebox.showwarning('Upozornění', str(ex))

        except Exception as ex:
            messagebox.showerror('Nastala chyba', f'Nastala neočekávaná chyba.\n{str(ex)}')

    def __copy_to_input(self):
        output = self.output.get().strip()
        self.input.set(output)
