import math
import string
from enum import Enum

from Core.StringExtensions import StringExtensions
from Core.ValidationError import ValidationError


class Version(Enum):
    ADFGX = 0
    ADFGVX = 1


class ADFGvXCrypt:
    def __init__(self, version=Version.ADFGVX, language='cz'):
        if version not in Version:
            raise ValidationError('Typ šifrování musí být buďto \'ADFGVX\' nebo \'ADFGX\' ')

        self.min_key_length = 3
        self.version = version
        self.marker = 'YL'
        self.replacement_dict = {' ': 'SP'}

        if version == Version.ADFGX:
            self.replacement_dict = {
                '0': 'ZE', '1': 'ON', '2': 'TV', '3': 'TH', '4': 'FO',
                '5': 'FI', '6': 'SI', '7': 'SE', '8': 'EI', '9': 'NI', ' ': 'SP'
            }
            self.ignored_char = 'J' if language == 'cz' else 'Q'
            self.replacement_char = 'I' if language == 'cz' else 'K'

    def encrypt(self, plain_text: str, key: str, alphabet='') -> str:
        key = StringExtensions.sanitize_text(key)
        plain_text = StringExtensions.sanitize_text(plain_text, r'[^A-Z0-9 ]')
        alphabet = self.fill_alphabet(alphabet)
        alphabet_matrix = self.__create_matrix(alphabet)

        if len(plain_text) < 1:
            raise ValidationError('Text je prázdný nebo obsahuje nepovolené znaky')

        if len(key) < self.min_key_length:
            raise ValidationError(f'Klíč musí být dlouhý alespoň {self.min_key_length} znaků')

        if len(key) > (len(plain_text) * 2):
            raise ValidationError('Klíč musí být kratší či roven dvojnásobku délky otevřeného textu')

        for value in self.replacement_dict.values():
            if self.marker + value in plain_text:
                raise ValidationError(f'Text obsahuje rezervovaný výraz: \'{self.marker + value}\'')

        # Replace non-crypt-able characters
        if self.version == Version.ADFGVX:
            converted_text = ''.join(
                [self.marker + self.replacement_dict[char] if char.isspace()
                 else char for char in plain_text])
        else:
            converted_text = ''.join(
                [self.marker + self.replacement_dict[char] if char.isnumeric() or char.isspace() else char for char in
                 plain_text]).replace(self.ignored_char, self.replacement_char)

        # Substitute via alphabet matrix to cipher text
        encrypted_text = ''
        for char in converted_text:
            for row in range(len(self.version.name)):
                if char in alphabet_matrix[row]:
                    col = alphabet_matrix[row].index(char)
                    encrypted_text += self.version.name[row] + self.version.name[col]

        # Transform
        row_length = len(key)
        table = [list(key)]
        index = 0
        while index < len(encrypted_text):
            row = list(encrypted_text[index:index + row_length])

            while len(row) < row_length:
                row.append('')

            table.append(row)
            index += row_length

        # Fill last row
        if index < len(encrypted_text):
            remaining_chars = encrypted_text[index:]
            table[-1] = list(remaining_chars) + [''] * (row_length - len(remaining_chars))

        # Get Indexes of sorted columns
        sorted_indexes = sorted(range(len(table[0])), key=lambda k: table[0][k])
        sorted_array = [[row[i] for i in sorted_indexes] for row in table]
        encrypted_text_final = ''.join([''.join([row[i] for row in sorted_array[1:]]) for i in range(len(sorted_array[0]))])

        return encrypted_text_final

    def decrypt(self, encrypted_text: str, key: str, alphabet='') -> str:
        key = StringExtensions.sanitize_text(key)
        encrypted_text = StringExtensions.sanitize_text(encrypted_text, f'[^{self.version.name}]')

        if len(encrypted_text) < 1:
            raise ValidationError('Text nesmí být prázdný')

        if len(key) < self.min_key_length:
            raise ValidationError(f'Klíč musí být dlouhý alespoň {self.min_key_length} znaků')

        if len(encrypted_text) % 2 != 0:
            raise ValidationError(f'Šifrovaný text \'{encrypted_text}\' musí mít sudý počet znaků')

        # Key chars with potential last row placement
        additional_cols = key[:len(encrypted_text) % len(key)]
        sorted_key = ''.join(sorted(key))
        row_count = math.ceil(len(encrypted_text) / len(sorted_key))
        decryption_table = [[''] * len(sorted_key) for _ in range(row_count)]

        # If last row non-full
        if additional_cols:
            decryption_table = [list(sorted_key)] + decryption_table
            x_index = 0
            y_index = 1

            # Get key chars with last row placement (sorted X unsorted key)
            for char in encrypted_text:
                if y_index >= row_count:
                    if sorted_key[x_index] in additional_cols and y_index == row_count:
                        additional_cols = StringExtensions.remove_first_occurrence(additional_cols, sorted_key[x_index])
                    else:
                        x_index += 1
                        y_index = 1

                decryption_table[y_index][x_index] = char
                y_index += 1
        # Last row full
        else:
            for index, char in enumerate(encrypted_text):
                row = index % row_count
                col = index // row_count
                decryption_table[row][col] = char

            decryption_table = [list(sorted_key)] + decryption_table

        # Get original col indexes
        indexes = []
        mapped_chars = ''
        for char in decryption_table[0]:
            if char in mapped_chars:
                index = key.index(char, indexes[mapped_chars.rindex(char)] + 1)
            else:
                index = key.index(char)

            indexes.append(index)
            mapped_chars += char

        # Sort table cols via indexes
        decryption_table = decryption_table[1:]
        original_pairs = ''
        for subarray in decryption_table:
            sorted_subarray = [''] * len(subarray)

            for i, new_index in enumerate(indexes):
                sorted_subarray[new_index] = subarray[i]

            original_pairs += ''.join(sorted_subarray)

        # Substitute back to plain text
        alphabet = self.fill_alphabet(alphabet)
        alphabet_matrix = self.__create_matrix(alphabet)
        decrypted_text_raw = ''
        for i in range(0, len(original_pairs), 2):
            char_pair = original_pairs[i:i + 2]
            x_index = self.version.name.index(char_pair[0])
            y_index = self.version.name.index(char_pair[1])
            decrypted_text_raw += alphabet_matrix[x_index][y_index]

        # Replace non-crypt-able character text alternatives
        decrypted_text = decrypted_text_raw
        for dict_key, value in self.replacement_dict.items():
            decrypted_text = decrypted_text.replace(self.marker + value, dict_key)

        return decrypted_text

    def fill_alphabet(self, current_alphabet: str):
        available_characters = string.ascii_uppercase

        # 5x5 vs 6x6 available chars
        if self.version == Version.ADFGVX:
            alphabet = StringExtensions.sanitize_text(current_alphabet, r'[^A-Z0-9]')
            available_characters += string.digits
        else:
            alphabet = StringExtensions.sanitize_text(current_alphabet).replace(self.ignored_char, '')
            available_characters = available_characters.replace(self.ignored_char, '')

        alphabet = StringExtensions.remove_duplicates(alphabet)

        # Add missing chars to user-defined alphabet
        for char in available_characters:
            if char not in alphabet:
                alphabet += char

        return alphabet

    def __create_matrix(self, alphabet: str) -> list[list[chr]]:
        matrix_size = len(self.version.name)
        cipher_table = [['' for _ in range(matrix_size)] for _ in range(matrix_size)]
        for i, char in enumerate(alphabet):
            row = i // matrix_size
            col = i % matrix_size
            cipher_table[row][col] = char

        return cipher_table
