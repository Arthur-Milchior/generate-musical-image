from __future__ import annotations

import copy
import unittest
from typing import Union, Optional, Any

from piano.scales.fingering import Fingering

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

    """The number of time a thumb have to pass over more than two half-tone"""
    _thumb_non_adjacent: int

    """Number of thumb over"""
    _nb_thumb_over: int

    """Number of time a white note is played after the thumb"""
    _nb_white_after_thumb: int

    """The number of times two far away consecutive note are played by 3rd and 4rth finger"""
    _number_of_3_and_4_non_adjacent: int
    _number_of_thumbs_on_black: int

    def __init__(self, fingering: Optional[Fingering] = None,
                 thumb_non_adjacent: int = 0, nb_thumb_over: int = 0,
                 nb_white_after_thumb: int = 0,
                 number_of_spaced_3_and_four: int = 0, number_of_thumbs_on_black: int = 0):
        self.fingering = fingering
        self._thumb_non_adjacent = thumb_non_adjacent
        self._nb_thumb_over = nb_thumb_over
        self._nb_white_after_thumb = nb_white_after_thumb
        self._number_of_3_and_4_non_adjacent = number_of_spaced_3_and_four
        self._number_of_thumbs_on_black = number_of_thumbs_on_black

    @staticmethod
    def _and_optional(left: Optional[bool], right: Optional[bool]) -> bool:
        if left is None:
            return right
        if right is None:
            return left
        return left and right

    @staticmethod
    def _at_most_one_non_optional(left: Optional[int], right: Optional[int]) -> int:
        if left is None:
            return right
        assert right is None
        return left

    @staticmethod
    def _add_optional(left: Optional[int], right: Optional[int]) -> int:
        if left is None:
            return right
        if right is None:
            return left
        return left + right

    def __add__(self, other: Penalty) -> Penalty:
        """Merge the penalty of self and other."""
        return Penalty(fingering=None,
                       thumb_non_adjacent=+self._thumb_non_adjacent + other._thumb_non_adjacent,
                       nb_thumb_over=+self._nb_thumb_over + other._nb_thumb_over,
                       nb_white_after_thumb=+self._nb_white_after_thumb + other._nb_white_after_thumb,
                       number_of_thumbs_on_black=self._number_of_thumbs_on_black,
                       number_of_spaced_3_and_four=self._number_of_3_and_4_non_adjacent)

    def add_thumb_on_black(self, fingering=None) -> Penalty:
        c = self._copy(fingering=fingering)
        c._number_of_thumbs_on_black += 1
        return c

    def add_3_and_four_non_adjacent(self, fingering=None) -> Penalty:
        c = self._copy(fingering=fingering)
        c._number_of_3_and_4_non_adjacent += 1
        return c

    def add_thumb_non_adjacent(self, fingering=None) -> Penalty:
        c = self._copy(fingering=fingering)
        c._thumb_non_adjacent += 1
        return c

    def add_white_after_thumb(self, fingering=None) -> Penalty:
        c = self._copy(fingering=fingering)
        c._nb_white_after_thumb += 1
        return c

    def add_thumb_over(self, fingering=None) -> Penalty:
        c = self._copy(fingering=fingering)
        c._nb_thumb_over += 1
        return c

    def _ordinal(self):
        pinky_side = self.fingering.pinky_side_tonic_finger
        return (self.fingering.avoid_this_extremity(),
                self._number_of_thumbs_on_black, self._thumb_non_adjacent,
                not self.fingering.pinky_to_thumb_on_white(),
                - pinky_side if pinky_side is not None else "a",
                # two incomparable types
                self._nb_thumb_over,
                self._number_of_3_and_4_non_adjacent,
                -self._nb_white_after_thumb,
                self.fingering.get_thumb_side_tonic_finger(),)

    def __ge__(self, other: Optional[Penalty]) -> bool:
        """Whether self is worse than other"""
        if other is None:
            return False
        return self._ordinal() >= other._ordinal()

    def best_known_is_at_least_as_good(self, other: Optional[Penalty]) -> bool:
        try:
            return self >= other
        except TypeError:
            # Can't compare both penalties because of the pinky_side_tonic_finger not yet being known for one.
            return False

    # def warning(self):
    #     text = ""
    #     if self._thumb_side_tonic_finger != self._pinky_side_tonic_finger:
    #         if self._pinky_side_tonic_finger < 4:
    #             text += "Starting finger is %s.\n" % self._pinky_side_tonic_finger
    #         if self._thumb_side_tonic_finger > 1:
    #             text += "Ending finger is %s.\n" % self._thumb_side_tonic_finger
    #     if self._thumb_non_adjacent:
    #         text += "Number of thumb passing followed by an interval which is not adjacent: %s.\n" % self._thumb_non_adjacent
    #     return text

    def acceptable(self) -> bool:
        if self._thumb_non_adjacent:
            return False
        if self.fingering.get_thumb_side_tonic_finger() != self.fingering.pinky_side_tonic_finger:
            if self.fingering.get_thumb_side_tonic_finger() not in [0, 1]:
                return False
            if self.fingering.pinky_side_tonic_finger not in [0, 4, 5]:
                return False
        return True

    def _copy(self, fingering=None) -> Penalty:
        c = copy.copy(self)
        c.fingering = fingering or c.fingering
        return c

#
# class TestPenalty(unittest.TestCase):
#     empty = Penalty()
#
#     def test_fail_add_two_starting_finger(self):
#         with self.assertRaises(Exception):
#             Penalty().add_pinky_side_finger(1).add_pinky_side_finger(1)
#
#     def test_fail_add_two_ending_finger(self):
#         with self.assertRaises(Exception):
#             Penalty().add_thumb_side_finger(1).add_thumb_side_finger(1)
#
#     def test_fail_set_nice_twice(self):
#         with self.assertRaises(Exception):
#             Penalty().set_extremity(3).set_extremity(2)
