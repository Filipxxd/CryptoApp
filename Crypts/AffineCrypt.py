import math
import string

from Core import TextSubstitution
from Core.StringExtensions import StringExtensions
from Exceptions.ValidationError import ValidationError


class AffineCrypt:
    def __init__(self):
        self.alphabet = string.ascii_uppercase

    def encrypt(self, text: str, a: int, b: int) -> string:
        sanitized_text = StringExtensions.sanitize_text(text, r'[A-Z0-9 ]')

        if len(text) < 1:
            return ''

        sub_text = TextSubstitution.sub(sanitized_text)

        if math.gcd(a, len(self.alphabet)) != 1:
            raise ValueError(
                f'Parameter a: \'{a}\' must be coprime with the alphabet length: {len(self.alphabet)}.')

        encrypted_text = ''
        for char in sub_text:
            if char not in self.alphabet:
                raise ValidationError(f'The character \'{char}\' cannot be encrypted.')

            x = self.alphabet.index(char)
            encrypted_text += self.alphabet[(a * x + b) % len(self.alphabet)]

        return encrypted_text

    def decrypt(self, text: str, a: int, b: int) -> string:
        text = StringExtensions.sanitize_text(text)

        if len(text) < 1:
            return ''

        if math.gcd(a, len(self.alphabet)) != 1:
            raise ValueError(
                f'Parameter a: \'{a}\' must be coprime with the alphabet length: \'{len(self.alphabet)}\'.')

        decrypted_text = ''
        for char in text:
            if char not in self.alphabet:
                raise ValidationError(f'The character \'{char}\' cannot be encrypted.')

            inverse_a = pow(a, -1, len(self.alphabet))

            if inverse_a is None:
                raise ValidationError(f'Modular inverse for parameter A: \'{a}\' and alphabet length: '
                                      f'\'{len(self.alphabet)}\' does not exist.')

            x = self.alphabet.index(char)
            decrypted_text += self.alphabet[inverse_a * (x - b) % len(self.alphabet)]

        decrypted_text = TextSubstitution.sub_reverse(decrypted_text)

        return decrypted_text
