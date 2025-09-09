import unittest

from fretted_instrument.position.string.strings import *

class TestStrings(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(NO_STRINGS, NO_STRINGS)
        self.assertEqual(NO_STRINGS, Strings([]))
        self.assertNotEqual(NO_STRINGS, ALL_STRINGS)

    def test_le(self):
        self.assertLess(NO_STRINGS, ALL_STRINGS)

    def test_pop(self):
        self.assertEqual(NO_STRINGS.pop(), None)
        self.assertEqual(ALL_STRINGS.pop(), (strings[0], Strings([strings[i] for i in range (1, 6)])))
        