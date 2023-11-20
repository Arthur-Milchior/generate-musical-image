from __future__ import annotations

import copy
import unittest
from typing import Union, Optional, Any

from piano.Fingering.fingering import Fingering

FingerNumbers = int  # 1 to 5


class Penalty:
    """Represents how complex is a piano fingering for a part of a scale.

    A fingering is acceptable if:
    * passing the thumb is on a note at most two half-tone away from previous note
    * the finger for the first note is 4 or 5, for the last note is 1, unless first and last use the same finger.

    A fingering is better than another one if, in order of importance:
    * it's number of non-adjacent thumb passing is lower,
    * the number of thumb-over is lower,
    * the extremity is good
    * the starting finger is higher
    * the ending finger is lower
    * the number of white after a thumb is higher
    """

    fingering: Optional[Fingering]

    """The finger on the tonic when starting/ending on the pinky side"""
    _pinky_side_tonic_finger: Optional[FingerNumbers]

    """The finger on the tonic when starting/ending on the thumb side"""
    _thumb_side_tonic_finger: Optional[FingerNumbers]

    """The number of time a thumb have to pass over more than two half-tone"""
    _thumb_non_adjacent: int

    """Number of thumb over"""
    _nb_thumb_over: int

    """Number of time a white note is played after the thumb"""
    _nb_white_after_thumb: int

    """Whether starts and end allow to nicely play a second octave"""
    _nice_extremity: Optional[bool]

    """The number of times two far away consecutive notes are played by 3rd and 4rth finger"""
    _number_of_3_and_4_non_adjacent: int
    _number_of_thumbs_on_black: int

    def __init__(self, fingering: Optional[Fingering] = None, _pinky_side_tonic_finger: Optional[FingerNumbers] = None,
                 thumb_non_adjacent: int = 0,
                 thumb_side_tonic_finger: Optional[FingerNumbers] = None, nb_thumb_over: int = 0,
                 nb_white_after_thumb: int = 0, nice_extremity: Optional[bool] = None,
                 number_of_spaced_3_and_four: int = 0, number_of_thumbs_on_black: int = 0):
        self.fingering = fingering
        self._pinky_side_tonic_finger = _pinky_side_tonic_finger
        self._thumb_non_adjacent = thumb_non_adjacent
        self._thumb_side_tonic_finger = thumb_side_tonic_finger
        self._nb_thumb_over = nb_thumb_over
        self._nb_white_after_thumb = nb_white_after_thumb
        self._nice_extremity = nice_extremity
        self._number_of_3_and_4_non_adjacent = number_of_spaced_3_and_four
        self._number_of_thumbs_on_black = number_of_thumbs_on_black

    @staticmethod
    def _and_optional(left: Optional[int], right: Optional[int]):
        if left is None:
            return right
        if right is None:
            return left
        return left and right

    @staticmethod
    def _at_most_one_non_optional(left: Optional[int], right: Optional[int]):
        if left is None:
            return right
        assert right is None
        return left

    @staticmethod
    def _add_optional(left: Optional[int], right: Optional[int]):
        if left is None:
            return right
        if right is None:
            return left
        return left + right

    def __add__(self, other: Penalty):
        """Merge the penalty of self and other."""
        return Penalty(fingering=None,
                       _pinky_side_tonic_finger=self._at_most_one_non_optional(self._pinky_side_tonic_finger,
                                                                              other._pinky_side_tonic_finger),
                       thumb_non_adjacent=+self._thumb_non_adjacent + other._thumb_non_adjacent,
                       thumb_side_tonic_finger=self._at_most_one_non_optional(self._thumb_side_tonic_finger,
                                                                              other._thumb_side_tonic_finger),
                       nb_thumb_over=+self._nb_thumb_over + other._nb_thumb_over,
                       nb_white_after_thumb=+self._nb_white_after_thumb + other._nb_white_after_thumb,
                       nice_extremity=self._and_optional(self._nice_extremity, other._nice_extremity),
                       number_of_thumbs_on_black=self._number_of_thumbs_on_black,
                       number_of_spaced_3_and_four=self._number_of_3_and_4_non_adjacent)

    def add_thumb_on_black(self, fingering=None):
        c = self._copy(fingering=fingering)
        c._number_of_thumbs_on_black += 1
        return c

    def add_pinky_side_finger(self, finger, fingering=None):
        assert self._pinky_side_tonic_finger is None
        c = self._copy(fingering=fingering)
        c._pinky_side_tonic_finger = finger
        return c

    def add_thumb_side_finger(self, finger, fingering=None):
        assert self._thumb_side_tonic_finger is None
        c = self._copy(fingering=fingering)
        c._thumb_side_tonic_finger = finger
        return c

    def add_3_and_four_non_adjacent(self, fingering=None):
        c = self._copy(fingering=fingering)
        c._number_of_3_and_4_non_adjacent += 1
        return c

    def add_thumb_non_adjacent(self, fingering=None):
        c = self._copy(fingering=fingering)
        c._thumb_non_adjacent += 1
        return c

    def add_white_after_thumb(self, fingering=None):
        c = self._copy(fingering=fingering)
        c._nb_white_after_thumb += 1
        return c


    def add_thumb_over(self, fingering=None):
        c = self._copy(fingering=fingering)
        c._nb_thumb_over += 1
        return c


    def set_bad_extremity(self, fingering=None):
        return self.set_extremity(False, fingering=fingering)

    def set_good_extremity(self, fingering=None):
        return self.set_extremity(True, fingering=fingering)

    def set_extremity(self, niceness: bool, fingering=None):
        assert self._nice_extremity is None
        c = self._copy(fingering=fingering)
        c._nice_extremity = niceness
        return c

    def is_bad_extremity(self):
        return not self._nice_extremity

    def is_good_extremity(self):
        return self._nice_extremity

    def __ge__(self, other: Optional[Penalty]):
        return self == other or self > other

    def __gt__(self, other: Optional[Penalty]):
        """Whether self is worse than other"""
        if other is None:
            return False

        if self._number_of_thumbs_on_black > other._number_of_thumbs_on_black:
            return True
        if self._number_of_thumbs_on_black < other._number_of_thumbs_on_black:
            return False

        if self._thumb_non_adjacent > other._thumb_non_adjacent:
            return True
        if self._thumb_non_adjacent < other._thumb_non_adjacent:
            return False

        if self._nb_thumb_over > other._nb_thumb_over:
            return True
        if self._nb_thumb_over < other._nb_thumb_over:
            return False

        if self.is_bad_extremity() and other.is_good_extremity():
            return True
        if other.is_bad_extremity() and self.is_bad_extremity():
            return False

        if self._number_of_3_and_4_non_adjacent != other._number_of_3_and_4_non_adjacent:
            return self._number_of_3_and_4_non_adjacent > other._number_of_3_and_4_non_adjacent

        assert (self._pinky_side_tonic_finger is not None) == (other._pinky_side_tonic_finger is not None)
        if self._pinky_side_tonic_finger is not None:
            if self._pinky_side_tonic_finger > other._pinky_side_tonic_finger:
                return False
            if self._pinky_side_tonic_finger < other._pinky_side_tonic_finger:
                return True

        if self._thumb_side_tonic_finger != other._thumb_side_tonic_finger:
            return self._thumb_side_tonic_finger > other._thumb_side_tonic_finger

        if self._nb_white_after_thumb != other._nb_white_after_thumb:
            return self._nb_white_after_thumb > other._nb_white_after_thumb

        return False

    def warning(self):
        text = ""
        if self._thumb_side_tonic_finger != self._pinky_side_tonic_finger:
            if self._pinky_side_tonic_finger < 4:
                text += "Starting finger is %s.\n" % self._pinky_side_tonic_finger
            if self._thumb_side_tonic_finger > 1:
                text += "Ending finger is %s.\n" % self._thumb_side_tonic_finger
        if self._thumb_non_adjacent:
            text += "Number of thumb passing followed by an interval which is not adjacent: %s.\n" % self._thumb_non_adjacent
        return text

    def acceptable(self):
        if self._thumb_non_adjacent:
            return False
        if self._thumb_side_tonic_finger != self._pinky_side_tonic_finger:
            if self._thumb_side_tonic_finger not in [0, 1]:
                return False
            if self._pinky_side_tonic_finger not in [0, 4, 5]:
                return False
        return True

    def _copy(self, fingering=None):
        c = copy.copy(self)
        c.fingering = fingering or c.fingering
        return c


class TestPenalty(unittest.TestCase):
    empty = Penalty()

    def test_fail_add_two_starting_finger(self):
        with self.assertRaises(Exception):
            Penalty().add_pinky_side_finger(1).add_pinky_side_finger(1)

    def test_fail_add_two_ending_finger(self):
        with self.assertRaises(Exception):
            Penalty().add_thumb_side_finger(1).add_thumb_side_finger(1)

    def test_fail_set_nice_twice(self):
        with self.assertRaises(Exception):
            Penalty().set_good_extremity().set_good_extremity()
        with self.assertRaises(Exception):
            Penalty().set_good_extremity().set_bad_extremity()
        with self.assertRaises(Exception):
            Penalty().set_bad_extremity().set_good_extremity()
        with self.assertRaises(Exception):
            Penalty().set_bad_extremity().set_bad_extremity()

    def test_set_nice(self):
        nice = Penalty().set_good_extremity()
        self.assertTrue(nice.is_good_extremity())
        self.assertFalse(nice.is_bad_extremity())
        bad = Penalty().set_bad_extremity()
        self.assertTrue(bad.is_bad_extremity())
        self.assertFalse(bad.is_good_extremity())
