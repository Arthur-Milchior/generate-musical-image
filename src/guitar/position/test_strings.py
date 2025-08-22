import unittest

from .strings import *

class TestStrings(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(NO_STRINGS, NO_STRINGS)
        self.assertEqual(NO_STRINGS, Strings([]))
        self.assertNotEqual(NO_STRINGS, ALL_STRINGS)

    def test_le(self):
        self.assertLess(NO_STRINGS, ALL_STRINGS)