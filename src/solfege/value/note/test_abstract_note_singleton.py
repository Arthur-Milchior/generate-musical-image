import unittest

from solfege.value.interval.test_abstract_interval_singleton import *
from solfege.value.note.singleton_note import AbstractSingletonNote
from solfege.value.note.abstract_note import *


class FakeSingletonNote(AbstractSingletonNote):
    IntervalClass: ClassVar[Type[Singleton]] = FakeSingletonInterval

    def get_chromatic(self):
        return self

    def get_diatonic(self):
        return self
    
    def get_name_up_to_octave(self):
        return "fake_name_up_to_octave"
    
    def non_ambiguous_string_for_file_name(self):
        return "fake_string_for_file_name"

class TestBaseNoteSingleton(unittest.TestCase):
    zero = FakeSingletonInterval.make(0)
    un = FakeSingletonInterval.make(1)
    moins_un = FakeSingletonInterval.make(-1)
    deux = FakeSingletonInterval.make(2)
    trois = FakeSingletonInterval.make(3)
    C4 = FakeSingletonNote.make(0)
    D4 = FakeSingletonNote.make(1)
    B3 = FakeSingletonNote.make(-1)
    E4 = FakeSingletonNote.make(2)
    F4 = FakeSingletonNote.make(3)

    # def test_is_note(self):
    #     self.assertTrue(self.C4.is_note())

    def test_get_number(self):
        self.assertEqual(self.C4.value, 0)

    def test_equal(self):
        self.assertEqual(self.C4, self.C4)
        self.assertNotEqual(self.D4, self.C4)
        self.assertEqual(self.D4, self.D4)

    def test_add(self):
        self.assertEqual(self.D4 + self.deux, self.F4)
        self.assertEqual(self.deux + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEqual(self.F4 - self.deux, self.D4)
        self.assertEqual(self.F4 - self.D4, self.deux)

    def test_lt(self):
        self.assertLess(self.C4, self.D4)
        self.assertLessEqual(self.C4, self.D4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEqual(repr(self.D4), "FakeSingletonNote(value=1)")

    def test_low_and_high(self):
        self.assertEqual(low_and_high(self.C4, self.C4), (self.C4, self.C4))
        self.assertEqual(low_and_high(self.D4, self.C4), (self.C4, self.D4))
        self.assertEqual(low_and_high(self.C4, self.D4), (self.C4, self.D4))

    def test_pinky_and_thumb(self):
        self.assertEqual(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=False), (self.C4, self.C4))
        self.assertEqual(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=False), (self.C4, self.D4))
        self.assertEqual(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=False), (self.C4, self.D4))
        self.assertEqual(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=True), (self.C4, self.C4))
        self.assertEqual(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=True), (self.D4, self.C4))
        self.assertEqual(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=True), (self.D4, self.C4))
