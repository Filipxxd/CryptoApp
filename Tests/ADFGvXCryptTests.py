import string
import unittest
from Crypts.ADFGvXCrypt import ADFGvXCrypt, Version


class ADFGvXCryptTest(unittest.TestCase):

    def test_ADFGVX_even_text_even_key(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'asdfasdfasdfasdfasdfasdfasdfasdf'
        key = 'asdf'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'AAAAAAAAAAAAAAAAGAGAGAGAGAGAGAGAAXAXAXAXAXAXAXAXAGAGAGAGAGAGAGAG'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_odd_text_odd_key(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'asdfghj'
        key = 'asdfg'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'AGDGXDADGAAAAD'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_odd_text_even_key(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'asdfg'
        key = 'asdf'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'AADGAAXAGA'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_even_text_odd_key(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'asdfgh'
        key = 'asdfg'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'AGDGXADAAAAD'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_key_multiple_occurrences_even(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'asdfghjkl'
        key = 'pkakfk'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'GDDADDAXGAAVGDXAAD'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_key_multiple_occurrences_2(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'asdfghjklmaxavavava'
        key = 'petrklekkkd'
        alphabet = string.ascii_uppercase + string.digits

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_key_multiple_occurrences_3(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'nemam ted na mysli s velkou zahradou a velkou bolesti v krku a kaslik a basta'
        key = 'xxppetreklekkkd'
        alphabet = string.ascii_uppercase + string.digits

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_key_multiple_occurrences_4(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'nemam ted na mysli s velkou zahradou a velkou bolesti v krku a kaslik a basta'
        key = 'jajsempepikpetrkliiiicekkkhahak'
        alphabet = string.ascii_uppercase + string.digits

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_numbers(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = '1234567890'
        key = 'petrklic'
        expected_encrypt = 'AVGDXXXVXXGVXXVFFVXV'
        alphabet = string.ascii_uppercase + string.digits

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_spaces(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'Moje jmeno Pepa'
        key = 'petrklic'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'VGDAGAAGFGAAFFGFDGADAGAVXVFVDFFAFXAAGFDFVF'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertTrue(expected_encrypt == actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertTrue(actual_decrypt == text.upper())

    def test_ADFGVX_full_sentence(self):
        crypt = ADFGvXCrypt(Version.ADFGVX)
        text = 'Moje jméno je Pepa Novák a je mně 18.'
        key = 'petrklíč123'
        alphabet = string.ascii_uppercase + string.digits
        expected_encrypt = 'VGDAAGADVGAAAXVAAGFGXVXFAAGXDAAFFGVFVFDFGVFDXDGADAFAFAGDAFVVGAVXVGAGAAXVGAGFVDFFDADFVAFDFGFXAAGAGAGXAGAVGFDFVDGFGGDVDGAF'
        expected_decrypt = 'MOJE JMENO JE PEPA NOVAK A JE MNE 18'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertEqual(expected_encrypt, actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_encrypt_odd_text_odd_key(self):
        crypt = ADFGvXCrypt(Version.ADFGX)
        text = 'asdfghi'
        key = 'asdfg'
        alphabet = string.ascii_uppercase
        expected_decrypt = text.upper()

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_encrypt_even_text_even_key(self):
        crypt = ADFGvXCrypt(Version.ADFGX)
        text = 'asdfgh'
        key = 'asdf'
        alphabet = string.ascii_uppercase
        expected_encrypt = 'AADGDDFAFAGD'
        expected_decrypt = text.upper()

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertEqual(expected_encrypt, actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_encrypt_odd_text_even_key(self):
        crypt = ADFGvXCrypt(Version.ADFGX)
        text = 'asdfg'
        key = 'sdaf'
        alphabet = string.ascii_uppercase
        expected_encrypt = 'GDAGDFAAAD'
        expected_decrypt = text.upper()

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertEqual(expected_encrypt, actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_encrypt_even_text_odd_key(self):
        crypt = ADFGvXCrypt(Version.ADFGX)
        text = 'asdfgh'
        key = 'sdfga'
        alphabet = string.ascii_uppercase
        expected_encrypt = 'ADADFGAFDAGD'
        expected_decrypt = text.upper()

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertEqual(expected_encrypt, actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_encrypt_even_text_odd_key_reversed(self):
        crypt = ADFGvXCrypt(Version.ADFGX)
        text = 'asdfgh'
        key = 'gfdsa'
        alphabet = string.ascii_uppercase
        expected_encrypt = 'ADGAADFAGDFD'
        expected_decrypt = text.upper()

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        self.assertEqual(expected_encrypt, actual_encrypt)

        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_full_sentence_cz(self):
        crypt = ADFGvXCrypt(Version.ADFGX, 'cz')
        text = 'Moje jméno je Pepa Novák a je mně 18.QQ'
        key = 'petrklíč123'
        alphabet = string.ascii_uppercase
        expected_decrypt = 'MOIE IMENO IE PEPA NOVAK A IE MNE 18QQ'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_full_sentence_en(self):
        crypt = ADFGvXCrypt(Version.ADFGX, 'en')
        text = 'Moje jméno je Pepa Novák a je mně 18.QQ'
        key = 'petrklíč123'
        alphabet = string.ascii_uppercase
        expected_decrypt = 'MOJE JMENO JE PEPA NOVAK A JE MNE 18KK'

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ADFGX_key_multiple_occurrences(self):
        crypt = ADFGvXCrypt(Version.ADFGX)
        text = 'asdfpoder'
        key = 'kakfk'
        alphabet = string.ascii_uppercase
        expected_decrypt = text.upper()

        actual_encrypt = crypt.encrypt(text, key, alphabet)
        actual_decrypt = crypt.decrypt(actual_encrypt, key, alphabet)
        self.assertEqual(actual_decrypt, expected_decrypt)
