import string
import unittest
from core.crypts.ADFGvXCipher import ADFGvXCipher


class ADFGVXCipherTest(unittest.TestCase):

    def test_even_text_even_key(self):
        text = 'asdfasdfasdfasdfasdfasdfasdfasdf'
        key = 'asdf'
        expected_encrypt = 'AAAAAAAAAAAAAAAAGAGAGAGAGAGAGAGAAXAXAXAXAXAXAXAXAGAGAGAGAGAGAGAG'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_odd_text_odd_key(self):
        text = 'asdfghj'
        key = 'asdfg'
        expected_encrypt = 'AGDGXDADGAAAAD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_odd_text_even_key(self):
        text = 'asdfg'
        key = 'asdf'
        expected_encrypt = 'AADGAAXAGA'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_even_text_odd_key(self):
        text = 'asdfgh'
        key = 'asdfg'
        expected_encrypt = 'AGDGXADAAAAD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_key_multiple_occurrences_even(self):
        text = 'asdfghjkl'
        key = 'pkakfk'
        expected_encrypt = 'GDDADDAXGAAVGDXAAD'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_key_multiple_occurrences_2(self):
        text = 'asdfghjklmaxavavava'
        key = 'petrklekkkd'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_key_multiple_occurrences_3(self):
        text = 'nemam ted na mysli s velkou zahradou a velkou bolesti v krku a kaslik a basta'
        key = 'xxppetreklekkkd'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_key_multiple_occurrences_4(self):
        text = 'nemam ted na mysli s velkou zahradou a velkou bolesti v krku a kaslik a basta'
        key = 'jajsempepikpetrkliiiicekkkhahak'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key,
                                                            string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == text.upper())

    def test_numbers(self):
        crypt = ADFGvXCipher()
        text = f'1234567890'
        key = 'petrklic'
        expected_encrypt = 'AVGDXXXVXXGVXXVFFVXV'
        actual_encrypt, _, _, _, _ = crypt.encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase)
        self.assertTrue(actual_decrypt == text.upper())

    # JUST WHEN whitespace == 'YLSP'
    def test_spaces(self):
        crypt = ADFGvXCipher()
        text = f'Moje jmeno Pepa'
        key = 'petrklic'
        expected_encrypt = 'VGDAGAAGFGAAFFGFDGADAGAVXVFVDFFAFXAAGFDFVF'
        actual_encrypt, _, _, _, _ = crypt.encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase)
        self.assertTrue(actual_decrypt == text.upper())

    # JUST WHEN whitespace == 'YLSP'
    def test_full_sentence(self):
        text = 'Moje jméno je Pepa Novák a je mně 18.'
        key = 'petrklíč123'
        expected_encrypt = 'VGDAAGADVGAAAXVAAGFGXVXFAAGXDAAFFGVFVFDFGVFDXDGADAFAFAGDAFVVGAVXVGAGAAXVGAGFVDFFDADFVAFDFGFXAAGAGAGXAGAVGFDFVDGFGGDVDGAF'
        actual_encrypt, _, _, _, _ = ADFGvXCipher().encrypt(text, key, string.ascii_uppercase + string.digits)
        actual_encrypt = actual_encrypt.replace(' ', '')
        self.assertTrue(expected_encrypt == actual_encrypt)
        actual_decrypt, _, _, _, _ = ADFGvXCipher().decrypt(actual_encrypt, key, string.ascii_uppercase + string.digits)
        self.assertTrue(actual_decrypt == 'MOJE JMENO JE PEPA NOVAK A JE MNE 18')
