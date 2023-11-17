from __future__ import annotations

import copy
import unittest
from typing import Union, Optional, Any

from piano.Fingering.fingering import Fingering

FingerNumbers = int # 1 to 5


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
    pinky_side_tonic_finger: Optional[FingerNumbers]

    """The finger on the tonic when starting/ending on the thumb side"""
    thumb_side_tonic_finger: Optional[FingerNumbers]

    """The number of time a thumb have to pass over more than two half-tone"""
    thumb_non_adjacent: int

    """Number of thumb over"""
    nb_thumb_over: int

    """Number of time a white note is played after the thumb"""
    nb_white_after_thumb: int

    """Whether starts and end allow to nicely play a second octave"""
    nice_extremity: Optional[bool]

    """The number of times two far away consecutive notes are played by 3rd and 4rth finger"""
    number_of_3_and_4_non_adjacent: int

    def __init__(self, fingering:Optional[Fingering]=None, pinky_side_tonic_finger: Optional[FingerNumbers] = None,
                 thumb_non_adjacent: int = 0,
                 thumb_side_tonic_finger: Optional[FingerNumbers] = None, nb_thumb_over: int = 0,
                 nb_white_after_thumb: int = 0, nice_extremity: Optional[bool] = None, number_of_spaced_3_and_four:int =0):
        self.fingering = fingering
        self.pinky_side_tonic_finger = pinky_side_tonic_finger
        self.thumb_non_adjacent = thumb_non_adjacent
        self.thumb_side_tonic_finger = thumb_side_tonic_finger
        self.nb_thumb_over = nb_thumb_over
        self.nb_white_after_thumb = nb_white_after_thumb
        self.nice_extremity = nice_extremity
        self.number_of_3_and_4_non_adjacent = number_of_spaced_3_and_four

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
                       pinky_side_tonic_finger=self._at_most_one_non_optional(self.pinky_side_tonic_finger, other.pinky_side_tonic_finger),
                       thumb_non_adjacent=+self.thumb_non_adjacent + other.thumb_non_adjacent,
                       thumb_side_tonic_finger=self._at_most_one_non_optional(self.thumb_side_tonic_finger, other.thumb_side_tonic_finger),
                       nb_thumb_over=+self.nb_thumb_over + other.nb_thumb_over,
                       nb_white_after_thumb=+self.nb_white_after_thumb + other.nb_white_after_thumb,
                       nice_extremity=self._and_optional(self.nice_extremity, other.nice_extremity))

    def add_starting_finger(self, finger, fingering=None):
        assert self.pinky_side_tonic_finger is None
        c = self._copy(fingering=fingering)
        c.pinky_side_tonic_finger = finger
        return c

    def add_ending_finger(self, finger, fingering=None):
        assert self.thumb_side_tonic_finger is None
        c = self._copy(fingering=fingering)
        c.thumb_side_tonic_finger = finger
        return c

    def add_3_and_four_non_adjacent(self, fingering=None):
        return Penalty(fingering or self.fingering, self.pinky_side_tonic_finger, self.thumb_non_adjacent + 1, self.thumb_side_tonic_finger,
                       self.nb_thumb_over, self.nb_white_after_thumb, self.nice_extremity, self.number_of_3_and_4_non_adjacent + 1)

    def add_thumb_non_adjacent(self, fingering=None):
        return Penalty(fingering or self.fingering, self.pinky_side_tonic_finger, self.thumb_non_adjacent + 1, self.thumb_side_tonic_finger,
                       self.nb_thumb_over, self.nb_white_after_thumb, self.nice_extremity, self.number_of_3_and_4_non_adjacent)

    def add_white_after_thumb(self, fingering=None):
        return Penalty(fingering or self.fingering, self.pinky_side_tonic_finger, self.thumb_non_adjacent, self.thumb_side_tonic_finger,
                       self.nb_thumb_over, self.nb_white_after_thumb + 1, self.nice_extremity, self.number_of_3_and_4_non_adjacent)

    def add_passing_finger(self, fingering=None):
        return Penalty(fingering or self.fingering, self.pinky_side_tonic_finger, self.thumb_non_adjacent, self.thumb_side_tonic_finger,
                       self.nb_thumb_over + 1, self.nb_white_after_thumb, self.nice_extremity, self.number_of_3_and_4_non_adjacent)

    def set_bad_extremity(self, fingering=None):
        return self.set_extremity(False, fingering=fingering)

    def set_good_extremity(self, fingering=None):
        return self.set_extremity(True, fingering=fingering)

    def set_extremity(self, niceness:bool, fingering=None):
        assert self.nice_extremity is None
        c = self._copy(fingering=fingering)
        c.nice_extremity = niceness
        return c

    def is_bad_extremity(self):
        return not self.nice_extremity

    def is_good_extremity(self):
        return self.nice_extremity

    def __gt__(self, other):
        """Whether self is worse than other"""
        if self.thumb_non_adjacent > other.thumb_non_adjacent:
            return True
        if self.thumb_non_adjacent < other.thumb_non_adjacent:
            return False

        if self.nb_thumb_over > other.nb_thumb_over:
            return True
        if self.nb_thumb_over < other.nb_thumb_over:
            return False

        if self.is_bad_extremity() and other.is_good_extremity():
            return True
        if other.is_bad_extremity() and self.is_bad_extremity():
            return False

        if self.number_of_3_and_4_non_adjacent != other.number_of_3_and_4_non_adjacent:
            return self.number_of_3_and_4_non_adjacent > other.number_of_3_and_4_non_adjacent

        assert (self.pinky_side_tonic_finger is not None) == (other.pinky_side_tonic_finger is not None)
        if self.pinky_side_tonic_finger is not None:
            if self.pinky_side_tonic_finger > other.pinky_side_tonic_finger:
                return False
            if self.pinky_side_tonic_finger < other.pinky_side_tonic_finger:
                return True

        if self.thumb_side_tonic_finger != other.thumb_side_tonic_finger:
            return self.thumb_side_tonic_finger > other.thumb_side_tonic_finger

        if self.nb_white_after_thumb != other.nb_white_after_thumb:
            return self.nb_white_after_thumb > other.nb_white_after_thumb

        return False

    def warning(self):
        text = ""
        if self.thumb_side_tonic_finger != self.pinky_side_tonic_finger:
            if self.pinky_side_tonic_finger < 4:
                text += "Starting finger is %s.\n" % self.pinky_side_tonic_finger
            if self.thumb_side_tonic_finger > 1:
                text += "Ending finger is %s.\n" % self.thumb_side_tonic_finger
        if self.thumb_non_adjacent:
            text += "Number of thumb passing followed by an interval which is not adjacent: %s.\n" % self.thumb_non_adjacent
        return text

    def acceptable(self):
        if self.thumb_non_adjacent:
            return False
        if self.thumb_side_tonic_finger != self.pinky_side_tonic_finger:
            if self.thumb_side_tonic_finger not in [0, 1]:
                return False
            if self.pinky_side_tonic_finger not in [0, 4, 5]:
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
            Penalty().add_starting_finger(1).add_starting_finger(1)

    def test_fail_add_two_ending_finger(self):
        with self.assertRaises(Exception):
            Penalty().add_ending_finger(1).add_ending_finger(1)

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
