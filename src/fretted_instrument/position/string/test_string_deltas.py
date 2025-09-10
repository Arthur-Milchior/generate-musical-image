import unittest

from fretted_instrument.fretted_instrument.fretted_instruments import Gui_tar
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.string.string_deltas import *
from fretted_instrument.position.string.strings import *
from fretted_instrument.position.string.string import String

def strings_make(l):
    return Strings.make(Gui_tar, l)

no_strings = strings_make([])
all_strings = Gui_tar.strings()
strings = Gui_tar.strings().strings

empty_first_string = strings[0]
empty_fourth_string = strings[3]
empty_sixth_string = strings[5]

instrument = Gui_tar


class TestStringDeltas(unittest.TestCase):
    def test_min(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).min(empty_first_string), strings[1])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).min(empty_first_string), strings[1])
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).min(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).min(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).min(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).min(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).min(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).min(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).min(empty_fourth_string), strings[0])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).min(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).min(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).min(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).min(empty_sixth_string), None)
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).min(empty_sixth_string), None)
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).min(empty_sixth_string), strings[0])

    def test_max(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).max(empty_first_string), strings[0])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).max(empty_first_string), strings[1])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).max(empty_first_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).max(empty_first_string), strings[1])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).max(empty_first_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).max(empty_first_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).max(empty_fourth_string), strings[3])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).max(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).max(empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).max(empty_fourth_string), strings[4])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).max(empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).max(empty_fourth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).max(empty_sixth_string), strings[5])
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).max(empty_sixth_string), strings[5])

    def test_strings(self):
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).set(empty_first_string), strings_make([strings[0]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).set(empty_first_string), strings_make([strings[0], strings[1]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).set(empty_first_string), all_strings)
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).set(empty_first_string), strings_make([strings[1]]))
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).set(empty_first_string), StringsInterval(Gui_tar, strings[1], strings[5]))
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).set(empty_first_string), all_strings)
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).set(empty_fourth_string), strings_make([strings[3]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).set(empty_fourth_string), strings_make([strings[3], strings[4]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).set(empty_fourth_string), StringsInterval(Gui_tar, strings[3], strings[5]))
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).set(empty_fourth_string), strings_make([strings[4]]))
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).set(empty_fourth_string), strings_make([strings[4], strings[5]]))
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).set(empty_fourth_string), all_strings)
        self.assertEqual(StringDelta.SAME_STRING_ONLY(Gui_tar).set(empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.SAME_OR_NEXT_STRING(Gui_tar).set(empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.SAME_STRING_OR_GREATER(Gui_tar).set(empty_sixth_string), strings_make([strings[5]]))
        self.assertEqual(StringDelta.NEXT_STRING_ONLY(Gui_tar).set(empty_sixth_string), no_strings)
        self.assertEqual(StringDelta.NEXT_STRING_OR_GREATER(Gui_tar).set(empty_sixth_string), no_strings)
        self.assertEqual(StringDelta.ANY_STRING(Gui_tar).set(empty_sixth_string), all_strings)
