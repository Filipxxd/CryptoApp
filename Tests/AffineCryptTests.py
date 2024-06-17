import string
import unittest
from Crypts.AffineCrypt import AffineCrypt


class AffineCryptTest(unittest.TestCase):

    def setUp(self):
        self.crypt = AffineCrypt()

    def test_empty_text(self):
        encrypted = self.crypt.encrypt('', 5, 8)
        decrypted = self.crypt.decrypt('', 5, 8)

        self.assertEqual(encrypted, '')
        self.assertEqual(decrypted, '')

    def test_valid_text(self):
        text = 'HELLO'
        a = 5
        b = 8

        encrypted = self.crypt.encrypt(text, a, b)
        decrypted = self.crypt.decrypt(encrypted, a, b)
        self.assertEqual(decrypted, text)

    def test_text_with_spaces(self):
        text = 'HELLO WORLD'
        a = 5
        b = 8

        encrypted = self.crypt.encrypt(text, a, b)
        decrypted = self.crypt.decrypt(encrypted, a, b)
        self.assertEqual(decrypted, text)

    def test_text_with_numbers(self):
        text = 'HELLO1234567890'
        a = 5
        b = 8

        encrypted = self.crypt.encrypt(text, a, b)
        decrypted = self.crypt.decrypt(encrypted, a, b)
        self.assertEqual(decrypted, text)

    def test_text_with_special_chars(self):
        text = 'HELLO' + string.punctuation
        a = 5
        b = 8
        expected_decrypt = 'HELLO'

        encrypted = self.crypt.encrypt(text, a, b)
        decrypted = self.crypt.decrypt(encrypted, a, b)
        self.assertEqual(decrypted, expected_decrypt)

    def test_non_coprime_a(self):
        with self.assertRaises(ValueError):
            self.crypt.encrypt('HELLO', 6, 8)
            self.crypt.decrypt('HELLO', 6, 8)

    def test_decrypt_text_with_invalid_modular_inverse(self):
        with self.assertRaises(ValueError):
            self.crypt.encrypt('XDDDD', 0, 8)
            self.crypt.decrypt('XDDDD', 0, 8)
