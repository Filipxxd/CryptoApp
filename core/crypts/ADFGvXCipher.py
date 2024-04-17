import math
import string

from core.StringExtensions import StringExtensions
from core.ValidationError import ValidationError


class ADFGvXCipher:
    def __init__(self, version='ADFGVX', language='cz'):
        if version not in ['ADFGVX', 'ADFGX']:
            raise ValidationError('Typ šifrování musí být buďto \'ADFGVX\' nebo \'ADFGX\' ')

        self.min_key_length = 2
        self.base = version
        self.marker = 'YL'
        self.replacement_dict = {' ': 'SP'}

        if version == 'ADFGX':
            self.replacement_dict = {
                '0': 'ZE', '1': 'ON', '2': 'TV', '3': 'TH', '4': 'FO',
                '5': 'FI', '6': 'SI', '7': 'SE', '8': 'EI', '9': 'NI', ' ': 'SP'
            }
            self.ignored_char = 'J' if language == 'cz' else 'Q'
            self.replacement_char = 'I' if language == 'cz' else 'K'

    def create_alphabet_matrix(self, alphabet: str) -> list[list[chr]]:
        available_characters = string.ascii_uppercase

        # 5x5 vs 6x6 available chars
        if self.base == 'ADFGVX':
            alphabet = StringExtensions.sanitize_text(alphabet, r'[^A-Z0-9]')
            available_characters += string.digits
        else:
            alphabet = StringExtensions.sanitize_text(alphabet).replace(self.ignored_char, '')
            available_characters = available_characters.replace(self.ignored_char, '')

        alphabet = StringExtensions.remove_duplicates(alphabet)

        # Add missing chars to user-defined alphabet
        for char in available_characters:
            if char not in alphabet:
                alphabet += char

        # Create matrix
        matrix_size = len(self.base)
        cipher_table = [['' for _ in range(matrix_size)] for _ in range(matrix_size)]
        for i, char in enumerate(alphabet):
            row = i // matrix_size
            col = i % matrix_size
            cipher_table[row][col] = char

        return cipher_table

    def encrypt(self, plain_text: str, key: str, alphabet='') -> (str, str, str, list[list[chr]], list[list[chr]]):
        key = StringExtensions.sanitize_text(key)
        plain_text = StringExtensions.sanitize_text(plain_text, r'[^A-Z0-9 ]')
        alphabet_matrix = self.create_alphabet_matrix(alphabet)

        if len(plain_text) < 1:
            raise ValidationError('Text nesmí být prázdný')

        if len(key) < self.min_key_length:
            raise ValidationError(f'Klíč musí být dlouhý alespoň {self.min_key_length} znaků')

        if len(key) > (len(plain_text) * 2):
            raise ValidationError('Klíč musí být kratší či roven dvojnásobku délky otevřeného textu')

        for value in self.replacement_dict.values():
            if self.marker + value in plain_text:
                raise ValidationError(f'Text obsahuje rezervovaný výraz: \'{self.marker + value}\'')

        # Replace non-crypt-able characters
        if self.base == 'ADFGVX':
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
            for row in range(len(self.base)):
                if char in alphabet_matrix[row]:
                    col = alphabet_matrix[row].index(char)
                    encrypted_text += self.base[row] + self.base[col]

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
        encrypted_text_final = ' '.join([''.join([row[i] for row in sorted_array[1:]]) for i in range(len(sorted_array[0]))])

        return encrypted_text_final, converted_text, encrypted_text, alphabet_matrix, sorted_array

    def decrypt(self, encrypted_text: str, key: str, alphabet='') -> (str, str, str, list[list[chr]], list[list[chr]]):
        key = StringExtensions.sanitize_text(key)
        encrypted_text = StringExtensions.sanitize_text(encrypted_text, f'[^{self.base}]')

        if len(encrypted_text) < 1:
            raise ValidationError('Text nesmí být prázdný')

        if len(key) < self.min_key_length:
            raise ValidationError(f'Klíč musí být dlouhý alespoň {self.min_key_length} znaků')

        if len(encrypted_text) % 2 != 0:
            raise ValidationError(f'Šifrovaný text \'{encrypted_text}\' musí mít sudý počet znaků')

        # Key chars with potential last row placement
        additional_cols = key[:len(encrypted_text) % len(key)]
        sorted_key = ''.join(sorted(key))
        num_rows = math.ceil(len(encrypted_text) / len(sorted_key))
        decryption_table = [[''] * len(sorted_key) for _ in range(num_rows)]

        # If last row non-full
        if additional_cols:
            decryption_table = [list(sorted_key)] + decryption_table
            x_index = 0
            y_index = 1

            # Get key chars with last row placement (sorted X unsorted key)
            for char in encrypted_text:
                if y_index >= num_rows:
                    if sorted_key[x_index] in additional_cols and y_index == num_rows:
                        additional_cols = StringExtensions.remove_first_occurrence(additional_cols, sorted_key[x_index])
                    else:
                        x_index += 1
                        y_index = 1

                decryption_table[y_index][x_index] = char
                y_index += 1
        # Last row full
        else:
            for index, char in enumerate(encrypted_text):
                row = index % num_rows
                col = index // num_rows
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
        alphabet_matrix = self.create_alphabet_matrix(alphabet)
        decrypted_text_raw = ''
        for i in range(0, len(original_pairs), 2):
            char_pair = original_pairs[i:i + 2]
            decrypted_text_raw += alphabet_matrix[self.base.index(char_pair[0])][self.base.index(char_pair[1])]

        # Replace non-crypt-able character text alternatives
        decrypted_text = decrypted_text_raw
        for dict_key, value in self.replacement_dict.items():
            decrypted_text = decrypted_text.replace(self.marker + value, dict_key)

        decryption_table.insert(0, StringExtensions.create_chunks(sorted_key, 1))
        return decrypted_text, encrypted_text, original_pairs, alphabet_matrix, decryption_table
