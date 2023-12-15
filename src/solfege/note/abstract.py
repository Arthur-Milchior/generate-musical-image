from __future__ import annotations

from typing import Union, TypeVar, Tuple

from solfege.interval.abstract import AbstractInterval, TestBaseInterval


class AbstractNote(AbstractInterval):
    IntervalClass = AbstractInterval
    """A note. Similar to an interval.

    -To a note may be added or subtracted an interval, but not to a note
    -Two note may be subtracted, leading to an interval.

    """

    def is_note(self):
        return True

    def __neg__(self):
        raise Exception("Trying to negate a note makes no sens.")

    def __sub__(self, other: Union[AbstractInterval, AbstractNote]):
        if isinstance(other, AbstractNote):
            return self.sub_note(other)
        else:
            return self.sub_interval(other)

    def sub_interval(self, other: AbstractInterval):
        return self + (-other)

    def sub_note(self, other: AbstractNote):
        return self.IntervalClass(self.get_number() - other.get_number())

    def __radd__(self, other: AbstractInterval):
        # called as other + self
        return self + other

    def __add__(self, other: AbstractInterval):
        if isinstance(other, AbstractNote):
            raise Exception("Adding two note")
        sum_ = super().__add__(
            other)  # Super still makes sens because a class inheriting _Note also inherits some other class.
        return sum_

    def get_octave(self, scientificNotation=False):
        """The octave.  By default, starting at middle c. If scientificNotation, starting at C0"""
        octave = super().get_octave()
        return octave + 4 if scientificNotation else octave

    def get_name_up_to_octave(self) -> str:
        raise NotImplemented

    def get_full_name(self):
        return f"{self.get_name_up_to_octave()}{str(self.get_octave() + 4)}"


NoteType = TypeVar('NoteType', bound=AbstractNote)


def low_and_high(note_1: NoteType, note_2: NoteType) -> Tuple[NoteType, NoteType]:
    """Return the lowest and highest note of the inputs"""
    return min(note_1, note_2), max(note_1, note_2)


def pinky_and_thumb_side(note_1: NoteType, note_2: NoteType, for_right_hand: bool) -> Tuple[NoteType, NoteType]:
    """Return the note on pinky side and thumb side of the hand"""
    low, high = low_and_high(note_1, note_2)
    if for_right_hand:
        return high, low
    else:
        return low, high


class TestBaseNote(TestBaseInterval):
    C4 = AbstractNote(0)
    D4 = AbstractNote(1)
    B3 = AbstractNote(-1)
    E4 = AbstractNote(2)
    F4 = AbstractNote(3)

    def test_is_note(self):
        self.assertTrue(self.C4.is_note())

    def test_has_number(self):
        self.assertTrue(self.C4.has_number())

    def test_get_number(self):
        self.assertEquals(self.C4.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.C4, self.C4)
        self.assertNotEquals(self.D4, self.C4)
        self.assertEquals(self.D4, self.D4)

    def test_add(self):
        self.assertEquals(self.D4 + self.deux, self.F4)
        self.assertEquals(self.deux + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.deux, self.D4)
        self.assertEquals(self.F4 - self.D4, self.deux)

    def test_lt(self):
        self.assertLess(self.D4, self.deux)
        self.assertLessEqual(self.D4, self.deux)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEquals(repr(self.D4), "AbstractNote(value=1)")

    def test_low_and_high(self):
        self.assertEquals(low_and_high(self.C4, self.C4), (self.C4, self.C4))
        self.assertEquals(low_and_high(self.D4, self.C4), (self.C4, self.D4))
        self.assertEquals(low_and_high(self.C4, self.D4), (self.C4, self.D4))

    def test_pinky_and_thumb(self):
        self.assertEquals(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=False), (self.C4, self.C4))
        self.assertEquals(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=False), (self.C4, self.D4))
        self.assertEquals(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=False), (self.C4, self.D4))
        self.assertEquals(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=True), (self.C4, self.C4))
        self.assertEquals(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=True), (self.D4, self.C4))
        self.assertEquals(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=True), (self.D4, self.C4))
