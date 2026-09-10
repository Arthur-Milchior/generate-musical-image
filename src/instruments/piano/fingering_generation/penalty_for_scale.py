from __future__ import annotations

import copy
from itertools import pairwise
from typing import Optional, Dict, Self, TypeVar, Any, Tuple, List, Union

from instruments.piano.piano_note import PianoNote
from instruments.piano.scales.fingering import Fingering
from solfege.value.note.abstract_note import pinky_and_thumb_side

FingerNumbers = int  # 1 to 5

PenaltyType = TypeVar('PenaltyType')


class PenaltyForScale:
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
    """The `Fingering` this penalty was computed for, or None while it is not yet known (see `Penalty`)."""

    """Number of time a white note is played after the thumb"""
    _nb_same_color_after_thumb_at_distance_diatonic: Dict[int, Dict[int, int]]
    """Keyed by diatonic distance then by the other finger involved: how many times a thumb-passing keeps the
    same key color (white-after-white-thumb or black-after-black-thumb) at that distance/finger."""

    """Number of time a white note is played after the thumb on a black note"""
    _nb_black_after_white_thumb_at_distance_diatonic: Dict[int, Dict[int, int]]
    """Keyed by diatonic distance then by the other finger involved: how many times a black note is played
    right after the thumb was on a white note, at that distance/finger."""

    """Number of time a black thumb is succeeded by a white note"""
    _nb_white_after_black_thumb: int
    """Count of transitions where a white note follows a thumb that was on a black note (theoretically
    impossible/never expected to happen; see the comment in `_ordinal`)."""

    """The number of times two far away consecutive note are played by 3rd and 4rth finger"""
    _three_four_interval_of_two: int
    """Number of non-adjacent 3rd/4th-finger transitions spanning a diatonic distance of 2."""
    _three_four_interval_of_three: int
    """Number of non-adjacent 3rd/4th-finger transitions spanning a diatonic distance of 3."""
    _number_of_thumbs_on_black: int
    """Number of notes played with the thumb (finger 1) on a black key."""

    def __init__(self, fingering: Optional[Fingering] = None,
                 nb_black_after_white_thumb_at_distance_diatonic: Optional[Dict[int, Dict[int, int]]] = None,
                 nb_white_after_black_thumb: int = 0,
                 nb_same_color_after_thumb_at_distance_diatonic: Optional[Dict[int, Dict[int, int]]] = None,
                 three_four_interval_of_three: int = 0,
                 three_four_interval_of_two: int = 0, number_of_thumbs_on_black: int = 0) -> None:
        """Create a penalty from its raw component counts (all default to zero/empty, i.e. no penalty)."""
        self.fingering = fingering
        self._nb_black_after_white_thumb_at_distance_diatonic = nb_black_after_white_thumb_at_distance_diatonic or {}
        self._nb_white_after_black_thumb = nb_white_after_black_thumb
        self._nb_same_color_after_thumb_at_distance_diatonic = nb_same_color_after_thumb_at_distance_diatonic or {}
        self._three_four_interval_of_two = three_four_interval_of_two
        self._three_four_interval_of_three = three_four_interval_of_three
        self._number_of_thumbs_on_black = number_of_thumbs_on_black

    def __eq__(self, other: PenaltyForScale) -> bool:
        """Equal if `fingering` and every component count/dict are equal."""
        return (self.fingering == other.fingering
                and
                self._nb_black_after_white_thumb_at_distance_diatonic == other._nb_black_after_white_thumb_at_distance_diatonic
                and
                self._nb_white_after_black_thumb == other._nb_white_after_black_thumb and
                self._nb_same_color_after_thumb_at_distance_diatonic == other._nb_same_color_after_thumb_at_distance_diatonic
                and
                self._three_four_interval_of_two == other._three_four_interval_of_two and
                self._three_four_interval_of_three == other._three_four_interval_of_three and
                self._number_of_thumbs_on_black == other._number_of_thumbs_on_black
                )

    def __repr__(self) -> str:
        """`eval`-able-looking representation listing every component count/dict."""
        return f"""PenaltyForScale(
  fingering = {self.fingering},
  nb_black_after_white_thumb_at_distance_diatonic = {self._nb_black_after_white_thumb_at_distance_diatonic},
  nb_white_after_black_thumb = {self._nb_white_after_black_thumb},
  nb_same_color_after_thumb_at_distance_diatonic = {self._nb_same_color_after_thumb_at_distance_diatonic},
  three_four_interval_of_two = {self._three_four_interval_of_two},
  three_four_interval_of_three = {self._three_four_interval_of_three},
  number_of_thumbs_on_black = {self._number_of_thumbs_on_black}
)"""

    @staticmethod
    def _and_optional(left: Optional[bool], right: Optional[bool]) -> bool:
        """Boolean `and` of `left`/`right`, treating a missing (None) operand as not constraining the result."""
        if left is None:
            return right
        if right is None:
            return left
        return left and right

    @staticmethod
    def _at_most_one_non_optional(left: Optional[int], right: Optional[int]) -> int:
        """Return whichever of `left`/`right` is not None; asserts that at most one of them is set."""
        if left is None:
            return right
        assert right is None
        return left

    @staticmethod
    def _add_optional(left: Optional[int], right: Optional[int]) -> int:
        """Sum `left`/`right`, treating a missing (None) operand as zero."""
        if left is None:
            return right
        if right is None:
            return left
        return left + right

    def __add__(self, other: PenaltyForScale) -> Self:
        """Merge the penalty of self and other."""
        assert self.__class__ == other.__class__
        nb_same_color_after_thumb_at_distance_diatonic = copy.deepcopy(
            self._nb_same_color_after_thumb_at_distance_diatonic)
        for (distance, nb) in other._nb_same_color_after_thumb_at_distance_diatonic:
            nb_same_color_after_thumb_at_distance_diatonic[distance] = (
                    self._nb_same_color_after_thumb_at_distance_diatonic.get(distance,
                                                                             0)
                    + nb)
        nb_black_after_white_thumb_at_distance_diatonic = copy.deepcopy(
            self._nb_black_after_white_thumb_at_distance_diatonic)
        for (distance, nb) in other._nb_black_after_white_thumb_at_distance_diatonic:
            nb_black_after_white_thumb_at_distance_diatonic[
                distance] = self._nb_black_after_white_thumb_at_distance_diatonic.get(distance, 0) + nb

        return PenaltyForScale(fingering=None,
                               nb_same_color_after_thumb_at_distance_diatonic=nb_same_color_after_thumb_at_distance_diatonic,
                               nb_black_after_white_thumb_at_distance_diatonic=nb_black_after_white_thumb_at_distance_diatonic,
                               nb_white_after_black_thumb=self._nb_white_after_black_thumb + other._nb_white_after_black_thumb,
                               number_of_thumbs_on_black=self._number_of_thumbs_on_black + other._number_of_thumbs_on_black,
                               three_four_interval_of_two=self._three_four_interval_of_two + other._three_four_interval_of_two,
                               three_four_interval_of_three=self._three_four_interval_of_three + other._three_four_interval_of_three)

    def add_thumb_on_black(self, fingering: Optional[Fingering] = None) -> Self:  # -> Self:
        """Return a copy of this penalty with one more thumb-on-a-black-key note recorded."""
        c = self._copy(fingering=fingering)
        c._number_of_thumbs_on_black += 1
        return c

    def add_three_and_four_non_adjacent(self, distance: int, fingering: Optional[Fingering] = None) -> Optional[Self]:  # -> Self:
        """Return a copy of this penalty recording a non-adjacent 3rd/4th-finger transition spanning `distance`
        diatonic steps (absolute value). No-op if `distance` is 0 or 1 (adjacent); returns None (unfingerable)
        if `distance` is more than 3."""
        distance = abs(distance)
        if distance <= 1:
            return self
        c = self._copy(fingering=fingering)
        if distance == 2:
            c._three_four_interval_of_two += 1
        elif distance == 3:
            c._three_four_interval_of_three += 1
        else:
            return None
        return c

    def add_same_color_after_thumb(self, distance: int, other_finger: int, fingering: Optional[Fingering] = None) -> Optional[Self]:  # -> Self:
        """Return a copy of this penalty recording a thumb-passing that keeps the same key color (white after
        white, or black after black), `distance` diatonic steps away, landing on `other_finger`.

        Returns None (unfingerable) if `distance` is more than 4."""
        assert 1 <= distance
        if distance > 4:
            return None
        c = self._copy(fingering=fingering)
        c._add_to_dict(c._nb_same_color_after_thumb_at_distance_diatonic, distance=distance, other_finger=other_finger)
        return c

    @staticmethod
    def _add_to_dict(dict: Dict[int, Dict[int, int]], distance: int, other_finger: int) -> None:
        """Increment, in-place, `dict[distance][other_finger]` (creating either level as needed)."""
        assert 2 <= other_finger <= 5
        if distance not in dict:
            dict[distance] = {}
        dict[distance][other_finger] = dict[distance].get(other_finger, 0) + 1

    def add_white_after_black_thumb(self, fingering: Optional[Fingering] = None) -> Self:  # -> Self:
        """Return a copy of this penalty with one more white-note-after-black-thumb transition recorded."""
        c = self._copy(fingering=fingering)
        c._nb_white_after_black_thumb += 1
        return c

    def add_black_after_white_thumb(self, distance: int, other_finger: int, fingering: Optional[Fingering] = None) -> Optional[Self]:  # -> Self:
        """Return a copy of this penalty recording a black note played `distance` diatonic steps after a thumb
        that was on a white note, landing on `other_finger`. Returns None (unfingerable) if `distance` is more
        than 4."""
        assert 1 <= distance
        if distance > 4:
            return None
        c = self._copy(fingering=fingering)
        c._add_to_dict(c._nb_black_after_white_thumb_at_distance_diatonic, distance, other_finger)
        return c

    @staticmethod
    def _sum_values(d: Dict[Any, int]) -> int:
        """Sum of the values of a single-level counts dict."""
        return sum(d.values())

    @staticmethod
    def _sum_sum_values(ds: Dict[Any, Dict[Any, int]]) -> int:
        """Sum of the values of every nested counts dict in a two-level counts dict."""
        return sum(PenaltyForScale._sum_values(d) for d in ds.values())

    @staticmethod
    def _ordinal_for_thumbover(dict: Dict[int, int]) -> Tuple[int, int, int]:
        """Return the counts for fingers 2, 4 and 3 (in that priority order) from a by-finger counts dict, used
        as a sortable tuple in `_ordinal`."""
        return dict.get(2, 0), dict.get(4, 0), dict.get(3, 0)

    def _ordinal(self) -> Tuple[int, int, int, int, int, int, int, int, bool, int, bool, int,
                                Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int],
                                int, Union[int, bool, None]]:  # -> Self:
        """Return a tuple encoding this penalty's rank, comparable lexicographically (see the class docstring
        for the exact ordering of criteria, worst-first)."""
        nb_thumbover = self._sum_sum_values(
            self._nb_same_color_after_thumb_at_distance_diatonic) + self._sum_sum_values(
            self._nb_black_after_white_thumb_at_distance_diatonic)

        nb_distance_4_same_color_after_thumb = self._sum_values(
            self._nb_same_color_after_thumb_at_distance_diatonic.get(4, {}))
        nb_distance_3_same_color_after_thumb = self._sum_values(
            self._nb_same_color_after_thumb_at_distance_diatonic.get(3, {}))
        nb_distance_4_black_after_white = self._sum_values(
            self._nb_black_after_white_thumb_at_distance_diatonic.get(4, {}))
        nb_distance_3_black_after_white = self._sum_values(
            self._nb_black_after_white_thumb_at_distance_diatonic.get(3, {}))

        pinky_side = self.fingering.pinky_side_tonic_finger if self.fingering else None
        return (
            # This should never occur
            self._nb_white_after_black_thumb,
            nb_thumbover,
            nb_distance_4_same_color_after_thumb,
            nb_distance_4_black_after_white,
            nb_distance_3_same_color_after_thumb,
            nb_distance_3_black_after_white,
            self._nb_same_color_after_thumb_at_distance_diatonic.get(2, {}).get(4, 0),
            self._three_four_interval_of_three,

            # Still pretty bad
            self.fingering.avoid_this_extremity() if self.fingering else False,

            # bad practice but acceptable
            self._number_of_thumbs_on_black,
            (not self.fingering.pinky_to_thumb_on_white()) if self.fingering else False,
            - (pinky_side if pinky_side is not None else 6),

            # Normal things
            self._ordinal_for_thumbover(self._nb_same_color_after_thumb_at_distance_diatonic.get(2, {})),
            self._ordinal_for_thumbover(self._nb_black_after_white_thumb_at_distance_diatonic.get(2, {})),
            self._ordinal_for_thumbover(self._nb_same_color_after_thumb_at_distance_diatonic.get(1, {})),
            self._ordinal_for_thumbover(self._nb_black_after_white_thumb_at_distance_diatonic.get(1, {})),
            self._three_four_interval_of_two,
            self.fingering.get_thumb_side_tonic_finger() if self.fingering else False,
        )

    def __ge__(self, other: Optional[PenaltyForScale]) -> bool:
        """Whether self is as least as complex as other"""
        if other is None:
            return False
        return self._ordinal() >= other._ordinal()

    def __gt__(self, other: Optional[PenaltyForScale]) -> bool:
        """Whether self is worse than other"""
        if other is None:
            return False
        return self._ordinal() > other._ordinal()

    def best_known_is_at_least_as_good(self, other: Optional[PenaltyForScale]) -> bool:
        """Whether `self` is at least as complex as `other` (see `__ge__`), treating a `TypeError` raised while
        comparing (e.g. because one side's `pinky_side_tonic_finger` is not known yet) as False."""
        try:
            return self >= other
        except TypeError:
            # Can't compare both penalties because of the pinky_side_tonic_finger not yet being known for one.
            return False

    # def warning(self):# -> Self:
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
        """Whether this fingering is playable at all: no thumb-passing spans 3+ diatonic steps, and (unless the
        scale starts and ends on the same finger) the thumb-side tonic finger is the thumb (or unset) and the
        pinky-side tonic finger is 4, 5 or unset."""
        for distance, _ in self._nb_black_after_white_thumb_at_distance_diatonic:
            if distance >= 3:
                return False
        for distance, _ in self._nb_same_color_after_thumb_at_distance_diatonic:
            if distance >= 3:
                return False

        if self.fingering.get_thumb_side_tonic_finger() != self.fingering.pinky_side_tonic_finger:
            if self.fingering.get_thumb_side_tonic_finger() not in [0, 1]:
                return False
            if self.fingering.pinky_side_tonic_finger not in [0, 4, 5]:
                return False
        return True

    def _copy(self, fingering: Optional[Fingering] = None) -> Self:  # -> Self:
        """Return a deep-enough copy of this penalty (independent nested dicts), optionally replacing
        `fingering` if one is given."""
        c = copy.copy(self)
        c._nb_black_after_white_thumb_at_distance_diatonic = copy.deepcopy(
            c._nb_black_after_white_thumb_at_distance_diatonic)
        c._nb_same_color_after_thumb_at_distance_diatonic = copy.deepcopy(
            c._nb_same_color_after_thumb_at_distance_diatonic)
        c.fingering = fingering or c.fingering
        return c

    def add_penalty_for_note(self, note: PianoNote) -> Self:  # -> Self:
        """Return the penalty for `self` plus the (single-note) penalty of playing `note`: a thumb-on-black
        penalty if `note` is a black key fingered with the thumb, otherwise `self` unchanged."""
        if note.is_black_key_on_piano() and note.finger == 1:
            return self.add_thumb_on_black()
        return self

    def add_penalty_for_note_transition(self, note_1: PianoNote, note_2: PianoNote,
                                        for_right_hand: bool, ) -> Optional[Self]:  # -> Optional[Self]:
        """None if adding this transition is impossible, otherwise self plus the penalty for this transition"""
        if note_1.finger == note_2.finger:
            return None
        pinky_side_note, thumb_side_note = pinky_and_thumb_side(note_1, note_2, for_right_hand)
        if thumb_side_note.get_chromatic() == pinky_side_note.get_chromatic():
            # same note repeated
            # TODO: penalize change of finger on same note maybe?
            return self
        if pinky_side_note.finger == thumb_side_note.finger:
            # Same finger for two different note is not possible
            return None
        diatonic_distance = abs(thumb_side_note.canonize(for_sharp=for_right_hand).get_diatonic().value -
                                pinky_side_note.canonize(for_sharp=for_right_hand).get_diatonic().value)
        if pinky_side_note.finger == 4 and thumb_side_note.finger == 3:
            return self.add_three_and_four_non_adjacent(diatonic_distance)
        if pinky_side_note.finger != 1:
            if thumb_side_note.finger > pinky_side_note.finger:
                # thumb side should be below pinky side
                return None
            return self

        # We now consider thumbovers. So pinky side finger is the thumb
        if thumb_side_note.finger == 5:
            # thumb over can't lead to 5
            return None
        if pinky_side_note.is_black_key_on_piano():
            if thumb_side_note.is_black_key_on_piano():
                return self.add_same_color_after_thumb(diatonic_distance, thumb_side_note.finger)
            else:
                return None
        else:
            if thumb_side_note.is_white_key_on_piano():
                return self.add_same_color_after_thumb(diatonic_distance, thumb_side_note.finger)
            else:
                return self.add_black_after_white_thumb(diatonic_distance, thumb_side_note.finger)

    @classmethod
    def from_scale(cls, notes: List[PianoNote], for_right_hand: bool) -> Optional[Self]:
        """Compute the total penalty of a fully-fingered `notes` sequence: the per-note penalty of each note
        plus the per-transition penalty between each pair of consecutive notes."""
        penalty = cls()
        for note in notes:
            penalty = penalty.add_penalty_for_note(note)
        for lower, higher in pairwise(notes):
            penalty = penalty.add_penalty_for_note_transition(lower, higher, for_right_hand)
        return penalty


