import unittest
from unittest import TestSuite


def load_tests(*args):
    suite = TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('.', '*Tests.py'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)
    return suite


if __name__ == '__main__':
    unittest.main()
