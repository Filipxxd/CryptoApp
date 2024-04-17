import unittest
from core.StringExtensions import StringExtensions


class StringExtensionsTest(unittest.TestCase):
    def test_remove_duplicates_default(self):
        self.assertTrue(StringExtensions.remove_duplicates('asdffasdf') == 'asdf')

    def test_shuffle_default(self):
        string = 'asdffasdf'
        shuffled = StringExtensions.shuffle(string)
        self.assertTrue(shuffled != string and len(shuffled) == len(string))

    def test_sanitize_text_alphabetical(self):
        self.assertTrue(StringExtensions.sanitize_text('asdf123456789-:- čš') == 'ASDFCS')

    def test_sanitize_text_alphabetical_numerical_spaces(self):
        self.assertTrue(StringExtensions.sanitize_text('asdf123456789-:- čš', r'[^A-Z0-9 ]') == 'ASDF123456789 CS')