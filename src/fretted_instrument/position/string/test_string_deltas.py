import unittest

from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.string.strings import ALL_STRINGS
from fretted_instrument.position.string.string_deltas import *
from fretted_instrument.position.string.strings import *
from fretted_instrument.position.string.string import String, strings

empty_first_string = strings[0]
empty_fourth_string = strings[3]
empty_sixth_string = strings[5]

class TestStringDeltas(unittest.TestCase):
    def test_min(self):
        self.assertEqual(SAME_STRING_ONLY.min(empty_first_string), strings[0])
        self.assertEqual(SAME_OR_NEXT_STRING.min(empty_first_string), strings[0])
        self.assertEqual(SAME_STRING_OR_GREATER.min(empty_first_string), strings[0])
        self.assertEqual(NEXT_STRING_ONLY.min(empty_first_string), strings[1])
        self.assertEqual(NEXT_STRING_OR_GREATER.min(empty_first_string), strings[1])
        self.assertEqual(ANY_STRING.min(empty_first_string), strings[0])
        self.assertEqual(SAME_STRING_ONLY.min(empty_fourth_string), strings[3])
        self.assertEqual(SAME_OR_NEXT_STRING.min(empty_fourth_string), strings[3])
        self.assertEqual(SAME_STRING_OR_GREATER.min(empty_fourth_string), strings[3])
        self.assertEqual(NEXT_STRING_ONLY.min(empty_fourth_string), strings[4])
        self.assertEqual(NEXT_STRING_OR_GREATER.min(empty_fourth_string), strings[4])
        self.assertEqual(ANY_STRING.min(empty_fourth_string), strings[0])
        self.assertEqual(SAME_STRING_ONLY.min(empty_sixth_string), strings[5])
        self.assertEqual(SAME_OR_NEXT_STRING.min(empty_sixth_string), strings[5])
        self.assertEqual(SAME_STRING_OR_GREATER.min(empty_sixth_string), strings[5])
        self.assertEqual(NEXT_STRING_ONLY.min(empty_sixth_string), None)
        self.assertEqual(NEXT_STRING_OR_GREATER.min(empty_sixth_string), None)
        self.assertEqual(ANY_STRING.min(empty_sixth_string), strings[0])

    def test_max(self):
        self.assertEqual(SAME_STRING_ONLY.max(empty_first_string), strings[0])
        self.assertEqual(SAME_OR_NEXT_STRING.max(empty_first_string), strings[1])
        self.assertEqual(SAME_STRING_OR_GREATER.max(empty_first_string), strings[5])
        self.assertEqual(NEXT_STRING_ONLY.max(empty_first_string), strings[1])
        self.assertEqual(NEXT_STRING_OR_GREATER.max(empty_first_string), strings[5])
        self.assertEqual(ANY_STRING.max(empty_first_string), strings[5])
        self.assertEqual(SAME_STRING_ONLY.max(empty_fourth_string), strings[3])
        self.assertEqual(SAME_OR_NEXT_STRING.max(empty_fourth_string), strings[4])
        self.assertEqual(SAME_STRING_OR_GREATER.max(empty_fourth_string), strings[5])
        self.assertEqual(NEXT_STRING_ONLY.max(empty_fourth_string), strings[4])
        self.assertEqual(NEXT_STRING_OR_GREATER.max(empty_fourth_string), strings[5])
        self.assertEqual(ANY_STRING.max(empty_fourth_string), strings[5])
        self.assertEqual(SAME_STRING_ONLY.max(empty_sixth_string), strings[5])
        self.assertEqual(SAME_OR_NEXT_STRING.max(empty_sixth_string), strings[5])
        self.assertEqual(SAME_STRING_OR_GREATER.max(empty_sixth_string), strings[5])
        self.assertEqual(NEXT_STRING_ONLY.max(empty_sixth_string), strings[5])
        self.assertEqual(NEXT_STRING_OR_GREATER.max(empty_sixth_string), strings[5])
        self.assertEqual(ANY_STRING.max(empty_sixth_string), strings[5])

    def test_strings(self):
        self.assertEqual(SAME_STRING_ONLY.set(empty_first_string), Strings([strings[0]]))
        self.assertEqual(SAME_OR_NEXT_STRING.set(empty_first_string), Strings([strings[0], strings[1]]))
        self.assertEqual(SAME_STRING_OR_GREATER.set(empty_first_string), ALL_STRINGS)
        self.assertEqual(NEXT_STRING_ONLY.set(empty_first_string), Strings([strings[1]]))
        self.assertEqual(NEXT_STRING_OR_GREATER.set(empty_first_string), StringsInterval(strings[1], strings[5]))
        self.assertEqual(ANY_STRING.set(empty_first_string), ALL_STRINGS)
        self.assertEqual(SAME_STRING_ONLY.set(empty_fourth_string), Strings([strings[3]]))
        self.assertEqual(SAME_OR_NEXT_STRING.set(empty_fourth_string), Strings([strings[3], strings[4]]))
        self.assertEqual(SAME_STRING_OR_GREATER.set(empty_fourth_string), StringsInterval(strings[3], strings[5]))
        self.assertEqual(NEXT_STRING_ONLY.set(empty_fourth_string), Strings([strings[4]]))
        self.assertEqual(NEXT_STRING_OR_GREATER.set(empty_fourth_string), Strings([strings[4], strings[5]]))
        self.assertEqual(ANY_STRING.set(empty_fourth_string), ALL_STRINGS)
        self.assertEqual(SAME_STRING_ONLY.set(empty_sixth_string), Strings([strings[5]]))
        self.assertEqual(SAME_OR_NEXT_STRING.set(empty_sixth_string), Strings([strings[5]]))
        self.assertEqual(SAME_STRING_OR_GREATER.set(empty_sixth_string), Strings([strings[5]]))
        self.assertEqual(NEXT_STRING_ONLY.set(empty_sixth_string), NO_STRINGS)
        self.assertEqual(NEXT_STRING_OR_GREATER.set(empty_sixth_string), NO_STRINGS)
        self.assertEqual(ANY_STRING.set(empty_sixth_string), ALL_STRINGS)
