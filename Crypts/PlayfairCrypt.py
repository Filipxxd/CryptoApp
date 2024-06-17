import string
from enum import Enum

from Core.StringExtensions import StringExtensions
from Core import TextSubstitution
from Exceptions.ValidationError import ValidationError


class Mode(Enum):
    Encrypt = 0
    Decrypt = 1


class PlayfairCrypt:

    def __init__(self, language='cz'):
        self.min_key_length = 5

        self.ignored_char = 'W' if language == 'cz' else 'Q'
        self.replacement_char = 'V' if language == 'cz' else 'K'

        self.text_sub = TextSubstitution
        self.additional_chars = ('X', 'Z')

    def encrypt(self, plain_text: str, key: str):
        sanitized_text = StringExtensions.sanitize_text(plain_text, r'[A-Z0-9 ]')
        replaced_text = sanitized_text.replace(self.ignored_char, self.replacement_char)

        if len(replaced_text) < 1:
            return ''

        for char in self.additional_chars:
            if self.text_sub.marker + char in replaced_text:
                raise ValidationError(f'Text obsahuje rezervovaný výraz: \'{self.text_sub.marker + char}\'')

        processed_text = self.text_sub.sub(replaced_text)

        # Separate same chars in pair
        i = 1
        while i < len(processed_text):
            if processed_text[i - 1] == processed_text[i]:
                processed_text = processed_text[:i] + self.__get_additional_mark(processed_text[i]) + processed_text[i:]
            i += 2

        if len(processed_text) % 2 != 0:
            processed_text += self.__get_additional_mark(processed_text[-1])

        table = self.__create_table(key)
        encrypted_text = self.__crypt(processed_text, table, Mode.Encrypt)

        return encrypted_text

    def decrypt(self, encrypted_text: str, key: str):
        sanitized_text = StringExtensions.sanitize_text(encrypted_text)

        if len(sanitized_text) < 1:
            return ''

        if len(sanitized_text) % 2 != 0:
            raise ValidationError(f'Šifrovaný text \'{sanitized_text}\' musí mít sudý počet znaků')

        table = self.__create_table(key)
        raw_decrypted_text = self.__crypt(sanitized_text, table, Mode.Decrypt)

        decrypted_text = self.text_sub.sub_reverse(raw_decrypted_text)

        for char in self.additional_chars:
            decrypted_text = decrypted_text.replace(self.text_sub.marker + char, '')

        return decrypted_text

    def __create_table(self, key: str):
        sanitized_key = StringExtensions.sanitize_text(key).replace(self.ignored_char, self.replacement_char)
        unique_key = StringExtensions.remove_duplicates(sanitized_key)

        if len(unique_key) < self.min_key_length:
            raise ValidationError(f'Klíč musí mít alespoň {self.min_key_length} unikátních znaků abecedy, tj. A-Z')

        alphabet = string.ascii_uppercase.replace(self.ignored_char, '')
        return unique_key + ''.join(char for char in alphabet if char not in unique_key)

    def __get_additional_mark(self, last_char: chr):
        return self.text_sub.marker + (
            self.additional_chars[0] if last_char != self.additional_chars[0] else self.additional_chars[1])

    @staticmethod
    def __crypt(text: str, table: str, mode: Mode):
        output_text = []

        for i in range(0, len(text), 2):
            row1, col1 = divmod(table.index(text[i]), 5)
            row2, col2 = divmod(table.index(text[i + 1]), 5)

            if row1 == row2:
                col1 = (col1 + 1) % 5 if mode == Mode.Encrypt else (col1 - 1) % 5
                col2 = (col2 + 1) % 5 if mode == Mode.Encrypt else (col2 - 1) % 5
            elif col1 == col2:
                row1 = (row1 + 1) % 5 if mode == Mode.Encrypt else (row1 - 1) % 5
                row2 = (row2 + 1) % 5 if mode == Mode.Encrypt else (row2 - 1) % 5
            else:
                col1, col2 = col2, col1

            output_text.extend([table[row1 * 5 + col1], table[row2 * 5 + col2]])

        return ''.join(output_text)
