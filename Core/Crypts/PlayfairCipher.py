from unidecode import unidecode
from Core.ValidationError import ValidationError
import re


class PlayfairCipher:
    def __init__(self, language='cz'):
        self.min_key_length = 5

        self.ignored_char = 'W' if language == 'cz' else 'Q'
        self.replacement_char = 'V' if language == 'cz' else 'K'

        self.marker = 'YL'
        self.additional_chars = ('X', 'Z')
        self.replacement_dict = {
            '0': 'ZE', '1': 'ON', '2': 'TV', '3': 'TH', '4': 'FO',
            '5': 'FI', '6': 'SI', '7': 'SE', '8': 'EI', '9': 'NI', ' ': 'SP'
        }

    def __sanitize_input(self, input_string: str):
        if len(input_string) < 1:
            raise ValidationError('Text nesmí být prázdný')

        input_string = unidecode(input_string.upper().rstrip())
        input_string = input_string.replace(self.ignored_char, self.replacement_char)

        return input_string

    def __get_table(self, key: str):
        key = self.__sanitize_input(key)
        key = re.sub(r'[^A-Z]+', '', key)

        unique_key = ''
        
        for char in key:
            if char not in unique_key:
                unique_key += char

        if len(unique_key) < self.min_key_length:
            raise ValidationError(f'Klíč musí mít alespoň {self.min_key_length} unikátních znaků abecedy, tj. A-Z')

        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.replace(self.ignored_char, '')
        unique_key += ''.join(char for char in alphabet if char not in unique_key)

        return unique_key

    def __get_additional_mark(self, last_char: chr):
        additional_char = self.additional_chars[0] \
            if last_char != self.additional_chars[0] else self.additional_chars[1]

        return self.marker + additional_char

    @staticmethod
    def __cryption(text: str, table: str, mode: str):
        output_text = []

        for i in range(0, len(text), 2):
            row1, col1 = table.index(text[i]) // 5, table.index(text[i]) % 5
            row2, col2 = table.index(text[i + 1]) // 5, table.index(text[i + 1]) % 5

            if row1 == row2:
                col1 = col1 + 1 if mode == 'encrypt' else col1 - 1
                col2 = col2 + 1 if mode == 'encrypt' else col2 - 1
                encrypted_pair = [table[row1 * 5 + col1 % 5], table[row2 * 5 + col2 % 5]]

            elif col1 == col2:
                row1 = row1 + 1 if mode == 'encrypt' else row1 - 1
                row2 = row2 + 1 if mode == 'encrypt' else row2 - 1
                encrypted_pair = [table[(row1 % 5) * 5 + col1], table[(row2 % 5) * 5 + col2]]

            else:
                encrypted_pair = [table[row1 * 5 + col2], table[row2 * 5 + col1]]

            output_text.extend(encrypted_pair)

        return ''.join(output_text)

    def encrypt(self, plain_text: str, key: str):
        plain_text = self.__sanitize_input(plain_text)
        plain_text = re.sub(r'[^A-Z0-9 ]', '', plain_text)

        for value in self.replacement_dict.values():
            if self.marker + value in plain_text:
                raise ValidationError(f'Text obsahuje rezervovaný výraz: \'{self.marker + value}\'')

        for char in self.additional_chars:
            if self.marker + char in plain_text:
                raise ValidationError(f'Text obsahuje rezervovaný výraz: \'{self.marker + char}\'')

        converted_text = ''.join(
            [self.marker + self.replacement_dict[char] if char.isnumeric() or char.isspace()
             else char for char in plain_text])

        i = 1
        while i < len(converted_text):
            if converted_text[i - 1] == converted_text[i]:
                converted_text = converted_text[:i] + self.__get_additional_mark(converted_text[i]) + converted_text[i:]

            i += 2

        if len(converted_text) % 2 != 0:
            converted_text += self.__get_additional_mark(converted_text[-1])

        table = self.__get_table(key)
        encrypted_text = self.__cryption(converted_text, table, 'encrypt')

        return encrypted_text, converted_text, plain_text, table

    def decrypt(self, encrypted_text: str, key: str):
        filtered_text = self.__sanitize_input(encrypted_text)
        filtered_text = re.sub(r'[^A-Z]', '', filtered_text)

        if len(filtered_text) % 2 != 0:
            raise ValidationError(f'Šifrovaný text \'{filtered_text}\' musí mít sudý počet znaků')

        table = self.__get_table(key)
        decrypted_text_raw = self.__cryption(filtered_text, table, 'decrypt')

        decrypted_text = decrypted_text_raw

        for dict_key, value in self.replacement_dict.items():
            decrypted_text = decrypted_text.replace(self.marker + value, dict_key)

        decrypted_text = decrypted_text.replace(self.marker + self.additional_chars[0], '')
        decrypted_text = decrypted_text.replace(self.marker + self.additional_chars[1], '')

        return decrypted_text, filtered_text, decrypted_text_raw, table
