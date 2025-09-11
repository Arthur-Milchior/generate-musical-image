import unittest

from fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.string.string_deltas import *
from fretted_instrument.position.string.strings import *
from fretted_instrument.position.string.string import String

def strings_make(l):
    return Strings.make(Guitar, l)

no_strings = strings_make([])
all_strings = Guitar.strings()
strings = Guitar.strings().strings

empty_first_string = strings[0]
empty_fourth_string = strings[3]
empty_sixth_string = strings[5]

instrument = Guitar


class TestStringDeltas(unittest.TestCase):
    def test_min(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).min(empty_first_string), strings[1])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).min(empty_first_string), strings[1])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).min(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).min(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).min(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).min(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).min(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).min(empty_fourth_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).min(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).min(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).min(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).min(empty_sixth_string), None)
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).min(empty_sixth_string), None)
        self.assertEqual(StringDelta.ANY_STRING(Guitar).min(empty_sixth_string), strings[0])

    def test_max(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).max(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).max(empty_first_string), strings[1])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).max(empty_first_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).max(empty_first_string), strings[1])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).max(empty_first_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).max(empty_first_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).max(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).max(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).max(empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).max(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).max(empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).max(empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).max(empty_sixth_string), strings[5])

    def test_strings(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).set(empty_first_string), strings_make([strings[0]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).set(empty_first_string), strings_make([strings[0], strings[1]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).set(empty_first_string), all_strings)
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).set(empty_first_string), strings_make([strings[1]]))
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).set(empty_first_string), StringsInterval(Guitar, strings[1], strings[5]))
        self.assertEqual(StringDelta.ANY_STRING(Guitar).set(empty_first_string), all_strings)
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).set(empty_fourth_string), strings_make([strings[3]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).set(empty_fourth_string), strings_make([strings[3], strings[4]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).set(empty_fourth_string), StringsInterval(Guitar, strings[3], strings[5]))
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).set(empty_fourth_string), strings_make([strings[4]]))
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).set(empty_fourth_string), strings_make([strings[4], strings[5]]))
        self.assertEqual(StringDelta.ANY_STRING(Guitar).set(empty_fourth_string), all_strings)
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).set(empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).set(empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).set(empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).set(empty_sixth_string), no_strings)
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).set(empty_sixth_string), no_strings)
        self.assertEqual(StringDelta.ANY_STRING(Guitar).set(empty_sixth_string), all_strings)
