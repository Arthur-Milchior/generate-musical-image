import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.string.string_deltas import *
from instruments.fretted_instrument.position.string.strings import *
from instruments.fretted_instrument.position.string.string import String

def strings_make(l):
    return Strings.make(l)

no_strings = strings_make(None)
all_strings = Guitar.strings()
strings = Guitar.strings().strings

empty_first_string = strings[0]
empty_fourth_string = strings[3]
empty_sixth_string = strings[5]

instrument = Guitar


class TestStringDeltas(unittest.TestCase):
    def test_min(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).min(Guitar, empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).min(Guitar, empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).min(Guitar, empty_first_string), strings[0])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).min(Guitar, empty_first_string), strings[1])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).min(Guitar, empty_first_string), strings[1])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).min(Guitar, empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).min(Guitar, empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).min(Guitar, empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).min(Guitar, empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).min(Guitar, empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).min(Guitar, empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).min(Guitar, empty_fourth_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).min(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).min(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).min(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).min(Guitar, empty_sixth_string), None)
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).min(Guitar, empty_sixth_string), None)
        self.assertEqual(StringDelta.ANY_STRING(Guitar).min(Guitar, empty_sixth_string), strings[0])

    def test_max(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).max(Guitar, empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).max(Guitar, empty_first_string), strings[1])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).max(Guitar, empty_first_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).max(Guitar, empty_first_string), strings[1])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).max(Guitar, empty_first_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).max(Guitar, empty_first_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).max(Guitar, empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).max(Guitar, empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).max(Guitar, empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).max(Guitar, empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).max(Guitar, empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).max(Guitar, empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).max(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).max(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).max(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).max(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).max(Guitar, empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Guitar).max(Guitar, empty_sixth_string), strings[5])

    def test_strings(self):
        same_string_only = StringDelta.SAME_STRING_ONLY(Guitar)
        actual = same_string_only.range(Guitar, empty_first_string)
        expected = strings_make([strings[0]])
        assert_typing(actual, Strings)
        assert_typing(expected, Strings)
        self.assertEqual(expected, actual, f"{expected} != {actual}")
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).range(Guitar, empty_first_string), strings_make([strings[0], strings[1]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).range(Guitar, empty_first_string), all_strings)
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).range(Guitar, empty_first_string), strings_make([strings[1]]))
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).range(Guitar, empty_first_string), Strings.make_interval(Guitar, strings[1], strings[5]))
        self.assertEqual(StringDelta.ANY_STRING(Guitar).range(Guitar, empty_first_string), all_strings)
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).range(Guitar, empty_fourth_string), strings_make([strings[3]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).range(Guitar, empty_fourth_string), strings_make([strings[3], strings[4]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).range(Guitar, empty_fourth_string), Strings.make_interval(Guitar, strings[3], strings[5]))
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Guitar).range(Guitar, empty_fourth_string), strings_make([strings[4]]))
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).range(Guitar, empty_fourth_string), strings_make([strings[4], strings[5]]))
        self.assertEqual(StringDelta.ANY_STRING(Guitar).range(Guitar, empty_fourth_string), all_strings)
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Guitar).range(Guitar, empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Guitar).range(Guitar, empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Guitar).range(Guitar, empty_sixth_string), strings_make([strings[5]]))
        actual = StringDelta.NEXT_STRING_ONLY(Guitar).range(Guitar, empty_sixth_string)
        self.assertEqual(no_strings, actual)
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Guitar).range(Guitar, empty_sixth_string), no_strings)
        self.assertEqual(StringDelta.ANY_STRING(Guitar).range(Guitar, empty_sixth_string), all_strings)
