import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.string.strings import *

def strings_make(l):
    return Strings.make(l)

no_strings = strings_make([])
all_strings = Guitar.strings()

class TestStrings(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(no_strings, no_strings)
        self.assertEqual(no_strings, strings_make([]))
        self.assertNotEqual(no_strings, all_strings)

    def test_le(self):
        self.assertLess(no_strings, all_strings)

    def test_pop(self):
        self.assertEqual(no_strings.pop(), None)
        first_string, remaining_strings = all_strings.pop()
        self.assertEqual(first_string, Guitar.string(1))
        self.assertEqual(remaining_strings, strings_make([Guitar.string(i) for i in range (2, 7)]))
        