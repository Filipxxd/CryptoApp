import math

from Core.ValidationError import ValidationError


class AffineCrypt:
    def __init__(self):
        self.alphabet = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.marker = 'XY'

        self.replacement_dict = {
            ' ': 'SP',
            '0': 'ZE',
            '1': 'ON',
            '2': 'TW',
            '3': 'TH',
            '4': 'FO',
            '5': 'FI',
            '6': 'SI',
            '7': 'SE',
            '8': 'EI',
            '9': 'NI'
        }

    def get_alphabets(self, a: int, b: int):
        original_alphabet = []
        ciphered_alphabet = []

        for char in self.alphabet:
            char_index = self.alphabet.index(char)
            encrypted_index = (a * char_index + b) % len(self.alphabet)
            encrypted_char = self.alphabet[encrypted_index]
            original_alphabet.append(char)
            ciphered_alphabet.append(encrypted_char)

        return original_alphabet, ciphered_alphabet

    def replace_num_space(self, string: str):
        string = string.upper()

        for value in self.replacement_dict.values():
            if self.marker + value in string:
                raise ValidationError(f'Text obsahuje rezervovaný výraz: \'{self.marker + value}\'')

        converted_text = ""
        for char in string:
            converted_text += self.marker + self.replacement_dict[char] if char.isnumeric() or char.isspace() else char

        return converted_text

    def cipher_string(self, string: str, a: int, b: int):
        if len(string) == 0:
            raise ValidationError('Text k šifrování nemůže být prázdný.')

        string = string.upper()

        if math.gcd(a, len(self.alphabet)) != 1:
            raise ValidationError(f'Parametr A: \'{a}\' musí být nesoudělný '
                                  f's délkou abecedy: \'{len(self.alphabet)}\'.')

        encrypted_text = ''
        for char in string:
            if char in self.alphabet:
                x = self.alphabet.index(char)
                encrypted_text += self.alphabet[(a * x + b) % len(self.alphabet)]
            else:
                raise ValidationError(f'Znak \'{char}\' nelze zašifrovat.')

        return encrypted_text

    def decipher_string(self, string: str, a: int, b: int):
        string = string.upper()

        if math.gcd(a, len(self.alphabet)) != 1:
            raise ValidationError(f'Parametr A: \'{a}\' musí být nesoudělný '
                                  f's délkou abecedy: \'{len(self.alphabet)}\'.')

        decrypted_text = ""
        for char in string:
            if char.isalpha():
                inverse_a = pow(a, -1, len(self.alphabet))

                if inverse_a is None:
                    raise ValidationError(f'Modulární inverze pro parametr A: \'{a}\' a délku abecedy: '
                                          f'\'{len(self.alphabet)}\' neexistuje.')

                x = self.alphabet.index(char)
                decrypted_text += self.alphabet[inverse_a * (x - b) % len(self.alphabet)]
            else:
                raise ValidationError('Šifrovaný text nesmí obsahovat číslice, mezery a speciální znaky.')

        for key, value in self.replacement_dict.items():
            decrypted_text = decrypted_text.replace(self.marker + value, key)

        return decrypted_text
