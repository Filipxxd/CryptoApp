import string
import unittest

from Core import TextSubstitution


class TestTextSubstitution(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(TextSubstitution.sub(''), '')
        self.assertEqual(TextSubstitution.sub_reverse(''), '')

    def test_alphabet(self):
        self.assertEqual(TextSubstitution.sub(string.ascii_letters), string.ascii_letters)

    def test_special_chars(self):
        self.assertEqual(TextSubstitution.sub(string.punctuation), string.punctuation)

    def test_sub_char_single(self):
        self.assertEqual(TextSubstitution.sub('0'), 'YLZE')
        self.assertEqual(TextSubstitution.sub('1'), 'YLON')
        self.assertEqual(TextSubstitution.sub(' '), 'YLSP')

    def test_sub_char_multi(self):
        self.assertEqual(TextSubstitution.sub('012'), 'YLZEYLONYLTV')
        self.assertEqual(TextSubstitution.sub('hello world'), 'helloYLSPworld')

    def test_sub_reverse_char_single(self):
        self.assertEqual(TextSubstitution.sub_reverse('YLZE'), '0')
        self.assertEqual(TextSubstitution.sub_reverse('YLON'), '1')
        self.assertEqual(TextSubstitution.sub_reverse('a'), 'a')

    def test_sub_reverse_char_multi(self):
        self.assertEqual(TextSubstitution.sub_reverse('YLZEYLONYLTV'), '012')
        self.assertEqual(TextSubstitution.sub_reverse('helloYLSPworld'), 'hello world')

    def test_reserved_word_in_string(self):
        with self.assertRaises(ValueError):
            TextSubstitution.sub('Hello YLZE')

    def test_marker_in_string(self):
        self.assertEqual(TextSubstitution.sub('YLOK'), 'YLOK')

    def test_sub_reverse_no_substitution(self):
        self.assertEqual(TextSubstitution.sub_reverse('hello world'), 'hello world')
        self.assertEqual(TextSubstitution.sub_reverse('VINYL'), 'VINYL')
