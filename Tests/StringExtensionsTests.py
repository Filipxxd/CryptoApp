import unittest
from Core.StringExtensions import StringExtensions


class StringExtensionsTest(unittest.TestCase):
    def test_remove_duplicates_default(self):
        text = 'asdffasdf'
        expected = 'asdf'
        actual = StringExtensions.remove_duplicates(text)

        self.assertEqual(expected, actual)

    def test_shuffle_default(self):
        text = 'asdffasdf'
        actual = StringExtensions.shuffle(text)

        self.assertNotEqual(actual, text)

    def test_sanitize_text_alphabetical(self):
        text = 'asdf123456789-:- čš'
        expected = 'ASDFCS'
        actual = StringExtensions.sanitize_text(text)

        self.assertEqual(actual, expected)

    def test_sanitize_text_alnums_spaces(self):
        text = 'asdf123456789-:- čš'
        pattern = r'[A-Z0-9 ]'
        expected = 'ASDF123456789 CS'
        actual = StringExtensions.sanitize_text(text, pattern)

        self.assertEqual(actual, expected)

    def test_remove_first_occurrence_not_present(self):
        text = 'abcdefghij'
        char_to_remove = 'x'
        expected = text
        actual = StringExtensions.remove_first_occurrence(text, char_to_remove)

        self.assertEqual(expected, actual)

    def test_remove_first_occurrence_multiple(self):
        text = 'banana'
        char_to_remove = 'a'
        expected = 'bnana'
        actual = StringExtensions.remove_first_occurrence(text, char_to_remove)

        self.assertEqual(expected, actual)

    def test_remove_duplicates_empty(self):
        text = ''
        expected = ''
        actual = StringExtensions.remove_duplicates(text)

        self.assertEqual(expected, actual)

    def test_sanitize_text_empty(self):
        text = ''
        expected = ''
        actual = StringExtensions.sanitize_text(text)

        self.assertEqual(expected, actual)

    def test_shuffle_empty(self):
        text = ''
        expected = ''
        actual = StringExtensions.shuffle(text)

        self.assertEqual(expected, actual)
