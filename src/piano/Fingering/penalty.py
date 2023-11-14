from __future__ import annotations

import copy
import unittest
from typing import Union, Optional, Any

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

    """Todo: What is it?"""
    fingering: Any

    """The finger on which the scale starts. 1 is thumb."""
    starting_finger: Optional[FingerNumbers]

    """The finger on which the scale ends. 1 is thumb."""
    ending_finger: Optional[FingerNumbers]

    """The number of time a thumb have to pass over more than two half-tone"""
    thumb_non_adjacent: int

    """Number of thumb over"""
    nb_thumb_over: int

    """Number of time a white note is played after the thumb"""
    nb_white_after_thumb: int

    """Whether starts and end allow to nicely play a second octave"""
    nice_extremity: Optional[bool]

    def __init__(self, fingering=None, starting_finger: Optional[FingerNumbers] = None,
                 thumb_non_adjacent: int = 0,
                 ending_finger: Optional[FingerNumbers] = None, nb_thumb_over: int = 0,
                 nb_white_after_thumb: int = 0, nice_extremity: Optional[bool] = None):
        self.fingering = fingering
        self.starting_finger = starting_finger
        self.thumb_non_adjacent = thumb_non_adjacent
        self.ending_finger = ending_finger
        self.nb_thumb_over = nb_thumb_over
        self.nb_white_after_thumb = nb_white_after_thumb
        self.nice_extremity = nice_extremity

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
                       starting_finger=self._at_most_one_non_optional(self.starting_finger, other.starting_finger),
                       thumb_non_adjacent=+self.thumb_non_adjacent + other.thumb_non_adjacent,
                       ending_finger=self._at_most_one_non_optional(self.ending_finger, other.ending_finger),
                       nb_thumb_over=+self.nb_thumb_over + other.nb_thumb_over,
                       nb_white_after_thumb=+self.nb_white_after_thumb + other.nb_white_after_thumb,
                       nice_extremity=self._and_optional(self.nice_extremity, other.nice_extremity))

    def add_starting_finger(self, finger, fingering=None):
        assert self.starting_finger is None
        c = self._copy(fingering=fingering)
        c.starting_finger = finger
        return c

    def add_ending_finger(self, finger, fingering=None):
        assert self.ending_finger is None
        c = self._copy(fingering=fingering)
        c.ending_finger = finger
        return c

    def add_thumb_non_adjacent(self, fingering=None):
        return Penalty(fingering or self.fingering, self.starting_finger, self.thumb_non_adjacent + 1, self.ending_finger,
                       self.nb_thumb_over, self.nb_white_after_thumb, self.nice_extremity)

    def add_white_after_thumb(self, fingering=None):
        return Penalty(fingering or self.fingering, self.starting_finger, self.thumb_non_adjacent, self.ending_finger,
                       self.nb_thumb_over, self.nb_white_after_thumb + 1, self.nice_extremity)

    def add_passing_finger(self, fingering=None):
        return Penalty(fingering or self.fingering, self.starting_finger, self.thumb_non_adjacent, self.ending_finger,
                       self.nb_thumb_over + 1, self.nb_white_after_thumb, self.nice_extremity)

    def set_bad_extremity(self, fingering=None):
        assert self.nice_extremity is None
        c = self._copy(fingering=fingering)
        c.nice_extremity = False
        return c

    def set_good_extremity(self, fingering=None):
        assert self.nice_extremity is None
        c = self._copy(fingering=fingering)
        c.nice_extremity = True
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

        if self.starting_finger > other.starting_finger:
            return False
        if self.starting_finger < other.starting_finger:
            return True

        if self.ending_finger > other.ending_finger:
            return True
        if self.ending_finger < other.ending_finger:
            return False

        if self.nb_white_after_thumb > other.nb_white_after_thumb:
            return True
        if self.nb_white_after_thumb < other.nb_white_after_thumb:
            return False
        return False

    def warning(self):
        text = ""
        if self.ending_finger != self.starting_finger:
            if self.starting_finger < 4:
                text += "Starting finger is %s.\n" % self.starting_finger
            if self.ending_finger > 1:
                text += "Ending finger is %s.\n" % self.ending_finger
        if self.thumb_non_adjacent:
            text += "Number of thumb passing followed by an interval which is not adjacent: %s.\n" % self.thumb_non_adjacent
        return text

    def acceptable(self):
        if self.thumb_non_adjacent:
            return False
        if self.ending_finger != self.starting_finger:
            if self.ending_finger not in [0, 1]:
                return False
            if self.starting_finger not in [0, 4, 5]:
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
