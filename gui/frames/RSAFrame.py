import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

from core.crypts.RSACrypt import RSACrypt
from core.ValidationError import ValidationError
from customtkinter import *


class RSAFrame(CTkFrame):
    def __init__(self, parent, return_frame: CTkFrame):
        CTkFrame.__init__(self, parent, fg_color='transparent')
        super().__init__(self)

        self.return_frame = return_frame

        self.crypt = RSACrypt()

        input_frame = CTkFrame(self, fg_color='transparent')
        input_frame.grid(row=0, column=0, sticky='n')

        p_entry_label = tk.Label(input_frame, text='P:')
        p_entry_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        self.p_entry = tk.Text(input_frame, wrap=tk.WORD, height=1, width=40)
        self.p_entry.grid(row=1, column=0, sticky='w', padx=10, pady=0)

        q_entry_label = tk.Label(input_frame, text='Q:')
        q_entry_label.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        self.q_entry = tk.Text(input_frame, wrap=tk.WORD, height=1, width=40)
        self.q_entry.grid(row=3, column=0, sticky='w', padx=10, pady=0)

        separatorX = ttk.Separator(input_frame, orient='horizontal')
        separatorX.grid(row=5, column=0, sticky='nswe', pady=10)

        text_entry_label = tk.Label(input_frame, text='Vstup:')
        text_entry_label.grid(row=6, column=0, sticky='w', padx=10, pady=5)

        self.text_entry = tk.Text(input_frame, wrap=tk.WORD, height=8, width=40)
        self.text_entry.grid(row=7, column=0, sticky='w', padx=10, pady=0)

        modulo_entry_label = tk.Label(input_frame, text='Modulus (n):')
        modulo_entry_label.grid(row=8, column=0, sticky='w', padx=10, pady=5)

        self.modulus_entry = tk.Text(input_frame, wrap=tk.WORD, height=4, width=40)
        self.modulus_entry.grid(row=9, column=0, sticky='w', padx=10, pady=0)

        public_entry_label = tk.Label(input_frame, text='Část Veřejného Klíče (e):')
        public_entry_label.grid(row=10, column=0, sticky='w', padx=10, pady=5)

        self.public_entry = tk.Text(input_frame, wrap=tk.WORD, width=40, height=2)
        self.public_entry.grid(row=11, column=0, sticky='w', padx=10, pady=0)

        private_entry_label = tk.Label(input_frame, text='Část Soukromého Klíče (d):')
        private_entry_label.grid(row=12, column=0, sticky='w', padx=10, pady=5)

        self.private_entry = tk.Text(input_frame, wrap=tk.WORD, width=40, height=2)
        self.private_entry.grid(row=13, column=0, sticky='w', padx=10, pady=0)

        button_frame = CTkFrame(input_frame, fg_color='transparent')
        button_frame.grid(row=14, column=0, sticky='w', pady=15)

        gen_keys_btn = tk.Button(button_frame, text='Generovat Q a P', command=lambda: self.__generate_primes())
        gen_keys_btn.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        gen_p_q_btn = tk.Button(button_frame, text='Generovat Klíče', command=lambda: self.__generate_keys())
        gen_p_q_btn.grid(row=0, column=1, sticky='w', padx=10, pady=10)

        encrypt_btn = tk.Button(button_frame, text='Šifrovat', command=lambda: self.__cryption('encrypt'))
        encrypt_btn.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        decrypt_btn = tk.Button(button_frame, text="Dešifrovat", command=lambda: self.__cryption('decrypt'))
        decrypt_btn.grid(row=1, column=1, sticky='e', padx=10, pady=10)

        separator = ttk.Separator(self, orient='vertical')
        separator.grid(row=0, column=1, sticky='ns', rowspan=7)

        output_frame = CTkFrame(self, fg_color='transparent', width=560)
        output_frame.grid(row=0, column=2, sticky='nsw')

        cipher_output_label = tk.Label(output_frame, text='Výstup:')
        cipher_output_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        self.cipher_output = tk.Text(output_frame, wrap=tk.WORD, state='disabled', height=20, width=75)
        self.cipher_output.grid(row=1, column=0, sticky='nsw', padx=10, pady=0)

        encrypt_btn = tk.Button(output_frame, text='Kopírovat do Vstupu', command=lambda: self.__copy_to_text_entry())
        encrypt_btn.grid(row=2, column=0, sticky='w', padx=10, pady=10)

    def __generate_primes(self):
        self.q_entry.delete(1.0, tk.END)
        self.p_entry.delete(1.0, tk.END)

        first = self.crypt.get_random_prime()
        second = self.crypt.get_random_prime()

        while second == first:
            second = self.crypt.get_random_prime()

        self.q_entry.insert(tk.END, str(first))
        self.p_entry.insert(tk.END, str(second))

    def __generate_keys(self):
        try:
            q = self.q_entry.get(1.0, tk.END)
            p = self.p_entry.get(1.0, tk.END)

            public, private = self.crypt.create_keys(self.__get_as_int(q), self.__get_as_int(p))

            self.modulus_entry.delete(1.0, tk.END)
            self.public_entry.delete(1.0, tk.END)
            self.private_entry.delete(1.0, tk.END)

            self.modulus_entry.insert(tk.END, str(public[0]))
            self.public_entry.insert(tk.END, str(public[1]))
            self.private_entry.insert(tk.END, str(private[1]))

        except ValidationError as ex:
            tk.messagebox.showwarning('Upozornění', str(ex))

        except Exception as ex:
            tk.messagebox.showerror('Nastala chyba', f'Nastala neočekávaná chyba.\n{str(ex)}')

    def __get_as_int(self, input: str) -> int:
        sanitized_input = re.sub(f'[^0-9]', '', input)

        if len(sanitized_input) < 1:
            raise ValidationError('Nemůže být prázdný!')

        return int(sanitized_input)

    def __cryption(self, mode: str):
        try:
            text = self.text_entry.get(1.0, tk.END)
            modulus = self.__get_as_int(self.modulus_entry.get(1.0, tk.END))
            public_part = self.__get_as_int(self.public_entry.get(1.0, tk.END))
            private_part = self.__get_as_int(self.private_entry.get(1.0, tk.END))

            self.cipher_output.configure(state='normal')
            self.cipher_output.delete(1.0, tk.END)

            text_output = ''

            if mode == 'encrypt':
                text_output = self.crypt.encrypt(text, (modulus, public_part))
                text_output = [text_output[i:i + len(str(modulus))] for i in
                               range(0, len(text_output), len(str(modulus)))]
                text_output = ' '.join(text_output)

            elif mode == 'decrypt':
                text_output = self.crypt.decrypt(text, (modulus, private_part))

            self.cipher_output.insert(tk.END, text_output)
            self.cipher_output.configure(state='disabled')

        except ValidationError as ex:
            tk.messagebox.showwarning('Upozornění', str(ex))

        except Exception as ex:
            tk.messagebox.showerror('Nastala chyba', f'Nastala neočekávaná chyba.\n{str(ex)}')

    def __copy_to_text_entry(self):
        output = self.cipher_output.get(1.0, tk.END).strip()

        self.text_entry.delete(1.0, tk.END)
        self.text_entry.insert(tk.END, output)
