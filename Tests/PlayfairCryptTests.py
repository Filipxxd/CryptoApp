import string
import unittest
from Crypts.PlayfairCrypt import PlayfairCrypt
from Exceptions.ValidationError import ValidationError


class PlayfairCipherTest(unittest.TestCase):
    language = 'cz'

    def test_text_empty(self):
        crypt = PlayfairCrypt(self.language)
        text = ''
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_alphabet_text(self):
        crypt = PlayfairCrypt(self.language)
        text = string.ascii_uppercase
        key = 'qwertz'
        expected_decrypt = text.replace(crypt.ignored_char, crypt.replacement_char)

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_alphabet_key(self):
        crypt = PlayfairCrypt(self.language)
        text = 'Hello'
        key = string.ascii_uppercase

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text.upper())

    def test_case_insensitivity_text(self):
        crypt = PlayfairCrypt(self.language)
        text = 'AsdF gH'
        key = 'qwertz'
        expected_decrypt = text.upper()

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_special_key(self):
        crypt = PlayfairCrypt(self.language)
        text = 'HELL NAH'
        key = 'kkLiiiČek123_@:_'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_large_inputs(self):
        crypt = PlayfairCrypt(self.language)
        text = 'ABCD' * (10 ** 3)
        key = 'qwertz' * (10 ** 3)

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_nums_spaces_text(self):
        crypt = PlayfairCrypt(self.language)
        text = '123 456 789'
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_sentence_text(self):
        crypt = PlayfairCrypt(self.language)
        text = 'Pepík123'
        key = 'qwwqertzzq'
        expected_decrypt = 'PEPIK123'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_special_chars(self):
        crypt = PlayfairCrypt(self.language)
        text = 'Hello!@#$%^&*()_+-=,.<>;:"\'\\[]{}/?|'
        key = 'qwertz'
        expected_decrypt = 'HELLO'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_ignored_char_key(self):
        crypt = PlayfairCrypt(self.language)
        text = 'HELLO ABCD'
        key = crypt.ignored_char + 'abcd'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_ignored_char_text(self):
        crypt = PlayfairCrypt(self.language)
        text = crypt.ignored_char + 'HELLO ABCD'
        key = crypt.ignored_char + 'abcd'
        expected_decrypt = text.replace(crypt.ignored_char, crypt.replacement_char)

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_char_additional(self):
        crypt = PlayfairCrypt(self.language)
        char_1 = crypt.additional_chars[0]
        char_2 = crypt.additional_chars[1]
        text = f'{char_1} {char_1}{char_2}{char_1}0{char_1}{char_1} {char_2}'
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_char_additional_end_even(self):
        crypt = PlayfairCrypt(self.language)
        text = f'HELLO 123{crypt.additional_chars[0] * 4}'
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_char_additional_end_odd(self):
        crypt = PlayfairCrypt(self.language)
        text = f'{crypt.additional_chars[0] * 3}HELLO 123'
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_char_additional_middle(self):
        crypt = PlayfairCrypt(self.language)
        text = (f'{crypt.additional_chars[0] + crypt.additional_chars[1] + crypt.additional_chars[0]}'
                f'ASD{crypt.additional_chars[1] + crypt.additional_chars[0] + crypt.additional_chars[0]}')
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_char_additional_start_even(self):
        crypt = PlayfairCrypt(self.language)
        text = f'{crypt.additional_chars[0] * 4}HELLO 123'
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_char_additional_start_odd(self):
        crypt = PlayfairCrypt(self.language)
        text = f'{crypt.additional_chars[0] * 3}HELLO 123'
        key = 'qwertz'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, text)

    def test_diacritics_ignore(self):
        crypt = PlayfairCrypt(self.language)
        text = 'ĚŠČŘŽÝÁŮÚ'
        key = 'qwertz'
        expected_decrypt = 'ESCRZYAUU'

        encrypt = crypt.encrypt(text, key)
        actual_decrypt = crypt.decrypt(encrypt, key)
        self.assertEqual(actual_decrypt, expected_decrypt)

    def test_empty_key(self):
        crypt = PlayfairCrypt(self.language)
        text = 'Hello'
        key = ''

        with self.assertRaises(ValidationError):
            crypt.encrypt(text, key)

    def test_invalid_key_length(self):
        crypt = PlayfairCrypt(self.language)
        text = 'hello'
        key = 'qwe'

        with self.assertRaises(ValidationError):
            crypt.encrypt(text, key)

    def test_invalid_length_encrypted(self):
        crypt = PlayfairCrypt(self.language)
        text = 'Pepik'
        key = 'qwertz'

        with self.assertRaises(ValidationError):
            crypt.decrypt(text, key)
