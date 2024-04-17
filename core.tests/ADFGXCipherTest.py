import string
import unittest
from core.crypts.ADFGvXCipher import ADFGvXCipher


class ADFGVXCipherTest(unittest.TestCase):

    def test_encrypt_odd_text_odd_key(self):
        text = 'asdfghi'
        key = 'asdfg'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertEqual(text.upper(), actual_decrypt)

    def test_encrypt_even_text_even_key(self):
        text = 'asdfgh'
        key = 'asdf'
        expected_encrypt = 'AADGDDFAFAGD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_encrypt_odd_text_even_key(self):
        text = 'asdfg'
        key = 'sdaf'
        expected_encrypt = 'GDAGDFAAAD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').encrypt(text, key,
                                                                         string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').decrypt(actual_encrypt, key,
                                                                         string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_encrypt_even_text_odd_key(self):
        text = 'asdfgh'
        key = 'sdfga'
        expected_encrypt = 'ADADFGAFDAGD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').encrypt(text, key,
                                                                         string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').decrypt(actual_encrypt, key, string.ascii_uppercase)
        self.assertTrue(actual_decrypt == text.upper())

    def test_encrypt_even_text_odd_key_reversed(self):
        text = 'asdfgh'
        key = 'gfdsa'
        expected_encrypt = 'ADGAADFAGDFD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').encrypt(text, key,
                                                                         string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').decrypt(actual_encrypt, key,
                                                                         string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_full_sentence(self):
        text = 'Moje jméno je Pepa Novák a je mně 18.'
        key = 'petrklíč123'
        actual_encrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'cz').encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_decrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'cz').decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == 'MOIE IMENO IE PEPA NOVAK A IE MNE 18')

    def test_key_multiple_occurrences(self):
        text = 'asdfpoder'
        key = 'kakfk'
        actual_encrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_decrypt, _, _, _, _ = ADFGvXCipher('ADFGX', 'en').decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())
