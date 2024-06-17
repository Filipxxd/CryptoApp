import math
import random
import re

from Core import NumExtensions


class RSACrypt:
    def __init__(self):
        self.text_block = 7  # -> number of chars (from plain text) in each cipher block
        self.binary_block = 10  # -> max allowed length of unicode char converted to binary
        self.prime_length = 12  # -> generate primes from 10 ** (x - 1) to 10 ** x

    def create_keys(self) -> tuple[tuple[int, int], tuple[int, int]]:
        q = NumExtensions.get_random_prime(self.prime_length)

        while True:
            p = NumExtensions.get_random_prime(self.prime_length)
            if q != p:
                break

        modulus = p * q
        euler = (p - 1) * (q - 1)

        while True:
            e = random.randint(2, euler - 1)
            if math.gcd(e, euler) == 1:
                break

        d = pow(e, -1, euler)
        public_key = (modulus, e)
        private_key = (modulus, d)

        return public_key, private_key

    def encrypt(self, plain_text: str, key: tuple[int, int]) -> str:
        plain_text = plain_text.strip()

        if len(plain_text) < 1:
            return ''

        encrypted_text = ''
        modulus_length = len(str(key[0]))

        for i in range(0, len(plain_text), self.text_block):
            substring = plain_text[i:i + self.text_block]
            long_binary = ''

            for char in substring:
                binary_val = bin(ord(char))[2:]

                if len(binary_val) > self.binary_block:
                    raise OverflowError(f'Binary representation \'{binary_val}\' for char \'{char}\' '
                                        'exceeds the max allowed size of binary block: \'{self.binary_block}\'.')

                while len(binary_val) < self.binary_block:
                    binary_val = '0' + binary_val

                long_binary += binary_val

            converted_decimal = int(long_binary, 2)

            if len(str(converted_decimal)) > modulus_length:
                raise OverflowError(
                    f'Substring: \'{substring}\' converted to number: \'{converted_decimal}\' '
                    f'must not have greater length than modulus: \'{key[0]}\'. '
                    f'Reduce \'self.text_block\' value or use larger modulus.')

            encrypted_num = pow(converted_decimal, key[1], key[0])
            encrypted_text += '0' * (modulus_length - len(str(encrypted_num))) + str(encrypted_num)

        return encrypted_text

    def decrypt(self, encrypted_text: str, key: tuple[int, int]) -> str:
        sanitized_text = re.sub(f'[^0-9]', '', encrypted_text)
        modulus_length = len(str(key[0]))

        if len(sanitized_text) < 1:
            return ''

        if len(sanitized_text) % modulus_length != 0:
            raise ValueError(f'Ciphered text \'{sanitized_text}\' is not valid.')

        encrypted_blocks = [sanitized_text[i:i + modulus_length] for i in
                            range(0, len(sanitized_text), modulus_length)]
        orig_text = ''

        for encrypted_block in encrypted_blocks:
            orig_decimal = pow(int(encrypted_block), key[1], key[0])
            orig_binary = bin(orig_decimal)[2:]

            while len(orig_binary) % self.binary_block != 0:
                orig_binary = '0' + orig_binary

            for i in range(0, len(orig_binary), self.binary_block):
                binary_block = orig_binary[i:(i + self.binary_block)]
                orig_text += chr(int(binary_block, 2))

        return orig_text
