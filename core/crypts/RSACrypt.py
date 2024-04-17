import math
import random
import re

from core.ValidationError import ValidationError


class RSACrypt:
    def __init__(self):
        self.text_block = 7  # -> number of chars (from plain text) in each cipher block
        self.binary_block = 10  # -> max allowed length of unicode char converted to binary
        self.prime_length = 12  # -> generate primes from 10 ** (x - 1) to 10 ** x

    def get_random_prime(self) -> int:
        while True:
            current = random.randint(10 ** (self.prime_length - 1), 10 ** self.prime_length)
            current += 1 if current % 2 == 0 else 0

            if len(str(current)) == self.prime_length and self.__is_prime(current):
                return current

    def create_keys(self, p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
        if p == q:
            raise ValidationError('Parametry \'p\' a \'q\' nesmí být totožné')

        if not self.__is_prime(p):
            raise ValidationError('Parametry \'p\' musí být prvočíslo')

        if not self.__is_prime(q):
            raise ValidationError('Parametr \'q\' musí být prvočíslo')

        if len(str(p)) != self.prime_length:
            raise ValidationError(
                f'Parametr \'p\' musí být v rozmezí {10 ** (self.prime_length - 1)} - {10 ** self.prime_length}')

        if len(str(q)) != self.prime_length:
            raise ValidationError(
                f'Parametr \'q\' musí být v rozmezí {10 ** (self.prime_length - 1)} - {10 ** self.prime_length}')

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
            raise ValidationError('Otevřený text nesmí být prázdný!')

        encrypted_text = ''
        modulus_length = len(str(key[0]))

        for i in range(0, len(plain_text), self.text_block):
            substring = plain_text[i:i + self.text_block]
            long_binary = ''

            for char in substring:
                binary_val = bin(ord(char))[2:]

                if len(binary_val) > self.binary_block:
                    raise ValueError(f'Binary representation \'{binary_val}\' for char \'{char}\' '
                                     f'exceeds the max allowed size of binary block: \'{self.binary_block}\'.')

                while len(binary_val) < self.binary_block:
                    binary_val = '0' + binary_val

                long_binary += binary_val

            converted_decimal = int(long_binary, 2)

            if len(str(converted_decimal)) > modulus_length:
                raise ValueError(
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
            raise ValidationError('Šifrovaný text nesmí být prázdný!')

        if len(sanitized_text) % modulus_length != 0:
            raise ValidationError(f'Šifrovaný text je chybný.')

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

    @staticmethod
    def __is_prime(num: int) -> bool:
        if num in [2, 3]:
            return True

        if num % 2 == 0 or num <= 1:
            return False

        r = 0
        d = num - 1

        while d % 2 == 0:
            r += 1
            d //= 2

        x_values = [pow(a, d, num) for a in [random.randint(2, num - 2) for _ in range(5)]]

        if any(x in [1, num - 1] for x in x_values):
            return True

        for _ in range(r - 1):
            x_values = [pow(x, 2, num) for x in x_values]
            if any(x == num - 1 for x in x_values):
                return True

        return False
