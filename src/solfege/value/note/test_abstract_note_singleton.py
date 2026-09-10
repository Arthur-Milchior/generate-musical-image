import unittest
from typing import Self

from solfege.value.interval.test_abstract_interval_singleton import *
from solfege.value.note.singleton_note import AbstractSingletonNote
from solfege.value.note.abstract_note import *


class FakeSingletonNote(AbstractSingletonNote):
    """Minimal concrete `AbstractSingletonNote` used to exercise the base class in isolation."""
    IntervalClass: ClassVar[Type[Singleton]] = FakeSingletonInterval
    """Interval class this fake note is added to/subtracted into."""

    def get_chromatic(self) -> Self:
        """Stub: this fake note is its own chromatic representation."""
        return self

    def get_diatonic(self) -> Self:
        """Stub: this fake note is its own diatonic representation."""
        return self

    def get_name_up_to_octave(self) -> str:
        """Stub name, unused by the tests other than for interface completeness."""
        return "fake_name_up_to_octave"

    def non_ambiguous_string_for_file_name(self) -> str:
        """Stub file-name string, unused by the tests other than for interface completeness."""
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

    def test_get_number(self) -> None:
        """The `value` attribute exposes the raw int position."""
        self.assertEqual(self.C4.value, 0)

    def test_equal(self) -> None:
        """Equality compares by value."""
        self.assertEqual(self.C4, self.C4)
        self.assertNotEqual(self.D4, self.C4)
        self.assertEqual(self.D4, self.D4)

    def test_add(self) -> None:
        """Adding an interval to a note (either order) shifts it; adding a note to a note fails."""
        self.assertEqual(self.D4 + self.deux, self.F4)
        self.assertEqual(self.deux + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self) -> None:
        """Negating a note is not supported (notes, unlike intervals, have no sign)."""
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self) -> None:
        """Subtracting an interval shifts the note; subtracting a note yields an interval."""
        self.assertEqual(self.F4 - self.deux, self.D4)
        self.assertEqual(self.F4 - self.D4, self.deux)

    def test_lt(self) -> None:
        """Notes order by their underlying value."""
        self.assertLess(self.C4, self.D4)
        self.assertLessEqual(self.C4, self.D4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self) -> None:
        """`repr` shows the constructor call that would rebuild the note."""
        self.assertEqual(repr(self.D4), "FakeSingletonNote(value=1)")

    def test_low_and_high(self) -> None:
        """`low_and_high` returns the pair ordered from lowest to highest."""
        self.assertEqual(low_and_high(self.C4, self.C4), (self.C4, self.C4))
        self.assertEqual(low_and_high(self.D4, self.C4), (self.C4, self.D4))
        self.assertEqual(low_and_high(self.C4, self.D4), (self.C4, self.D4))

    def test_pinky_and_thumb(self) -> None:
        """`pinky_and_thumb_side` returns (pinky-side, thumb-side), which flips with hand
        laterality."""
        self.assertEqual(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=False), (self.C4, self.C4))
        self.assertEqual(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=False), (self.C4, self.D4))
        self.assertEqual(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=False), (self.C4, self.D4))
        self.assertEqual(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=True), (self.C4, self.C4))
        self.assertEqual(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=True), (self.D4, self.C4))
        self.assertEqual(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=True), (self.D4, self.C4))
