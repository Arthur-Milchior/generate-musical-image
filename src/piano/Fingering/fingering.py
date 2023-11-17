from __future__ import annotations

import unittest
from typing import Dict, Optional, Union

from piano.pianonote import PianoNote
from solfege.interval.interval import Interval
from solfege.note import Note
from solfege.Scale.pattern import ScalePattern, minor_melodic


class Fingering:
    """
    A non-mutable class representing an association from note on the scale to one of the five finger of the hand.
    1 being the thumb

    """

    """Associate to a note in the base octave a finger. 1 being the thumb. The exception being the tonic, 
    which may be played by two fingers to start and continue/end the scale. The other one is saved at 
    finger_for_the_tonic_at_start"""
    _dic: Dict[Note, int]

    """The tonic for this fingering."""
    tonic: Optional[Note]

    """ Whether it's a fingering for right hand"""
    for_right_hand: bool

    """The finger used to play the tonic once at an extremity. Usually the fifth, or sometime fourth, to start the 
    increasing scale on the left hand and to end the increasing scale on the right end."""
    pinky_side_tonic_finger: Optional[int] = None

    def __init__(self, for_right_hand: bool):
        self._dic = dict()
        self.tonic = None
        self.for_right_hand = for_right_hand
        self.pinky_side_tonic_finger = None

    def _copy(self) -> Fingering:
        nex = Fingering(for_right_hand=self.for_right_hand)
        nex.tonic = self.tonic
        nex.pinky_side_tonic_finger = self.pinky_side_tonic_finger
        nex._dic = dict(self._dic)
        return nex

    def __eq__(self, other: Fingering):
        assert isinstance(other, Fingering)
        assert self.for_right_hand == other.for_right_hand  # If we compare fingering for left and right hand, there is a bug somewhere
        return self.tonic == other.tonic and self._dic == other._dic and self.pinky_side_tonic_finger == other.pinky_side_tonic_finger

    def __contains__(self, note):
        note = note.get_in_base_octave()
        return note in self._dic

    def add_pinky_side(self, note: Note, finger: int):
        assert self.pinky_side_tonic_finger is None
        assert finger != 1
        nex = self._copy()
        note = note.get_in_base_octave()
        nex.pinky_side_tonic_finger = finger
        nex.tonic = note
        return nex

    def add(self, note: Note, finger: int) -> Union[Fingering, bool]:
        """
        Returns:
            * False if the note was already here in the fingering with a different finger
            * True if the note was already in the fingering with this finger
            * A new fingering, similar to self, plus this note associated to this finger.
            In this last case, if `self` is empty, this note is assumed to be the tonic.
            """
        # assert self.pinky_side_tonic_finger is not None  # Fingering generation starts with pinky side.
        nex = self._copy()
        note = note.get_in_base_octave()
        if note in nex._dic:
            return nex._dic[note] == finger
        nex._dic[note] = finger
        return nex

    def ends_and_start_on_same_finger(self) -> bool:
        """Whether the first and last finger of the scale's fingering are the same"""
        return self.get_thumb_side_tonic_finger() == self.get_pinky_side_tonic_finger()

    def ends_with_a_thumb(self) -> bool:
        """Whether the last finger of the scale's fingering is a thumb"""
        return self.get_thumb_side_tonic_finger() == 1

    def is_end_nice(self) -> bool:
        """Whether the first and last finger is the thumb"""
        return self.ends_with_a_thumb() or self.ends_and_start_on_same_finger()

    def get_thumb_side_tonic_finger(self) -> Optional[int]:
        return self.get_finger(self.tonic)

    def get_pinky_side_tonic_finger(self) -> Optional[int]:
        return self.pinky_side_tonic_finger

    def get_finger(self, note: Note, starting_finger=False) -> Optional[int]:
        """Get the finger for `note`.
        If `note` is the tonic and `starting_finger` holds, get the starting finger"""
        note = note.get_in_base_octave()
        if starting_finger:
            assert note.equals_modulo_octave(self.tonic)
            return self.pinky_side_tonic_finger
        return self._dic.get(note)

    def __str__(self):
        text = f"""Fingering(for_right_hand={self.for_right_hand})"""
        if self.tonic:
            text += f""".\n  add_pinky_side(note={self.tonic}, finger={self.pinky_side_tonic_finger})"""
        for note, finger in self._dic.items():
            text += f""".\n  add(note={note}, finger={finger})"""
        return text

    def __repr__(self):
        text = f"""Fingering(for_right_hand={self.for_right_hand})"""
        if self.tonic:
            text += f""".\n  add_pinky_side(note={self.tonic!r}, finger={self.pinky_side_tonic_finger})"""
        for note, finger in self._dic.items():
            text += f""".\n  add(note={note!r}, finger={finger})"""
        return text

    def generate(self, lowest_or_highest_note: Note, scale_pattern: ScalePattern[Interval], number_of_octaves: int = 1):
        assert lowest_or_highest_note.equals_modulo_octave(lowest_or_highest_note)
        scale = scale_pattern.generate(lowest_or_highest_note, number_of_octaves=number_of_octaves)
        fingered_scale = [
            PianoNote(Note(chromatic=note.get_chromatic().get_number(), diatonic=note.get_diatonic().get_number()),
                      finger=self.get_finger(note)) for note in scale.notes]
        pos_of_pinky_side_extremity = -1 if self.for_right_hand else 0
        last_note = fingered_scale[pos_of_pinky_side_extremity]
        last_note.finger = self.get_finger(note=last_note.note, starting_finger=True)
        return fingered_scale


# Test section
class TestFingering(unittest.TestCase):
    maxDiff = None
    tonic = Note(chromatic=0, diatonic=0)
    right_minor_melodic_fingering = Fingering(for_right_hand=True).add_pinky_side(tonic.add_octave(1), finger=5)
    right_minor_melodic_1 = [PianoNote(tonic, finger=1),
                             PianoNote(Note(chromatic=2, diatonic=1), finger=2),
                             PianoNote(Note(chromatic=3, diatonic=2), finger=3),
                             PianoNote(Note(chromatic=5, diatonic=3), finger=1),
                             PianoNote(Note(chromatic=7, diatonic=4), finger=2),
                             PianoNote(Note(chromatic=9, diatonic=5), finger=3),
                             PianoNote(Note(chromatic=11, diatonic=6), finger=4),
                             PianoNote(Note(chromatic=12, diatonic=7), finger=5),
                             ]
    for note in reversed(right_minor_melodic_1[:-1]):
        right_minor_melodic_fingering = right_minor_melodic_fingering.add(note.note, finger=note.finger)

    left_minor_melodic_fingering = Fingering(for_right_hand=False).add_pinky_side(tonic, 5)
    left_minor_melodic_1 = [PianoNote(tonic, finger=5),
                            PianoNote(Note(chromatic=2, diatonic=1), finger=4),
                            PianoNote(Note(chromatic=3, diatonic=2), finger=3),
                            PianoNote(Note(chromatic=5, diatonic=3), finger=2),
                            PianoNote(Note(chromatic=7, diatonic=4), finger=1),
                            PianoNote(Note(chromatic=9, diatonic=5), finger=3),
                            PianoNote(Note(chromatic=11, diatonic=6), finger=2),
                            PianoNote(Note(chromatic=12, diatonic=7), finger=1),
                            ]

    for note in left_minor_melodic_1[1:]:
        left_minor_melodic_fingering = left_minor_melodic_fingering.add(note.note, finger=note.finger)

    empty = Fingering(for_right_hand=True)
    octave = Note(chromatic=12, diatonic=7)
    second = Note(chromatic=2, diatonic=1)
    thumb_0 = empty.add(tonic, 1)
    index_1 = thumb_0.add(second, 2)
    ended = index_1.add_pinky_side(octave, 5)

    def test_one_note(self):
        self.assertIsInstance(self.thumb_0, Fingering)
        self.assertEquals(self.thumb_0.get_pinky_side_tonic_finger(), 1)
        self.assertEquals(self.thumb_0.get_thumb_side_tonic_finger(), None)
        self.assertEquals(self.thumb_0.tonic, self.tonic)
        self.assertEquals(self.thumb_0.get_finger(self.tonic), None)
        self.assertEquals(self.thumb_0.get_finger(self.tonic, starting_finger=True), 1)
        self.assertEquals(self.thumb_0.get_finger(self.second), None)
        with self.assertRaises(Exception):
            self.thumb_0.get_finger(self.second, starting_finger=True)
        self.assertEquals(repr(self.thumb_0), """Fingering(for_right_hand=True).
  add(note=Note(chromatic = 0, diatonic = 0), finger=1)""")

    def test_ended(self):
        self.assertIsInstance(self.ended, Fingering)
        self.assertEquals(self.ended.get_pinky_side_tonic_finger(), 1)
        self.assertEquals(self.ended.get_thumb_side_tonic_finger(), 5)
        self.assertEquals(self.ended.tonic, self.tonic)
        self.assertEquals(self.ended.get_finger(self.tonic), 5)
        self.assertEquals(self.ended.get_finger(self.tonic, starting_finger=True), 1)
        self.assertEquals(self.ended.get_finger(self.second), 2)
        with self.assertRaises(Exception):
            self.ended.get_finger(self.second, starting_finger=True)

    def test_two_note(self):
        self.assertIsInstance(self.index_1, Fingering)
        self.assertEquals(self.index_1.get_pinky_side_tonic_finger(), 1)
        self.assertEquals(self.index_1.get_thumb_side_tonic_finger(), None)
        self.assertEquals(self.index_1.tonic, self.tonic)
        self.assertEquals(self.index_1.get_finger(self.tonic), None)
        self.assertEquals(self.index_1.get_finger(self.tonic, starting_finger=True), 1)
        self.assertEquals(self.index_1.get_finger(self.second), 2)
        with self.assertRaises(Exception):
            self.index_1.get_finger(self.second, starting_finger=True)
        self.assertEquals(repr(self.index_1), """Fingering(for_right_hand=True).
  add(note=Note(chromatic = 0, diatonic = 0), finger=1).
  add(note=Note(chromatic = 2, diatonic = 1), finger=2)""")

    def test_add_two_same_note(self):
        self.assertTrue(self.index_1.add(self.second, 2))
        self.assertFalse(self.index_1.add(self.second, 3))

    def test_add_three_tonic_same_note(self):
        self.assertTrue(self.ended.add(self.octave, 5))
        self.assertFalse(self.ended.add(self.octave, 1))

    def test_generate_right_hand(self):
        self.assertEquals(
            self.right_minor_melodic_fingering.generate(lowest_or_highest_note=self.tonic, scale_pattern=minor_melodic),
            self.right_minor_melodic_1)
        two_octaves = [
            PianoNote(Note(chromatic=0, diatonic=0), finger=1),
            PianoNote(Note(chromatic=2, diatonic=1), finger=2),
            PianoNote(Note(chromatic=3, diatonic=2), finger=3),
            PianoNote(Note(chromatic=5, diatonic=3), finger=1),
            PianoNote(Note(chromatic=7, diatonic=4), finger=2),
            PianoNote(Note(chromatic=9, diatonic=5), finger=3),
            PianoNote(Note(chromatic=11, diatonic=6), finger=4),
            PianoNote(Note(chromatic=12, diatonic=7), finger=1),
            PianoNote(Note(chromatic=14, diatonic=8), finger=2),
            PianoNote(Note(chromatic=15, diatonic=9), finger=3),
            PianoNote(Note(chromatic=17, diatonic=10), finger=1),
            PianoNote(Note(chromatic=19, diatonic=11), finger=2),
            PianoNote(Note(chromatic=21, diatonic=12), finger=3),
            PianoNote(Note(chromatic=23, diatonic=13), finger=4),
            PianoNote(Note(chromatic=24, diatonic=14), finger=5),
        ]
        self.assertEquals(
            self.right_minor_melodic_fingering.generate(lowest_or_highest_note=self.tonic, scale_pattern=minor_melodic,
                                                        number_of_octaves=2),
            two_octaves)
        two_octaves.reverse()
        self.assertEquals(
            self.right_minor_melodic_fingering.generate(lowest_or_highest_note=self.tonic.add_octave(2),
                                                        scale_pattern=minor_melodic,
                                                        number_of_octaves=-2),
            two_octaves)

    def test_generate_left_hand(self):
        generated = self.left_minor_melodic_fingering.generate(lowest_or_highest_note=self.tonic,
                                                               scale_pattern=minor_melodic)
        self.assertEquals(
            generated,
            self.left_minor_melodic_1)
        two_octaves = [
            PianoNote(Note(chromatic=0, diatonic=0), finger=5),
            PianoNote(Note(chromatic=2, diatonic=1), finger=4),
            PianoNote(Note(chromatic=3, diatonic=2), finger=3),
            PianoNote(Note(chromatic=5, diatonic=3), finger=2),
            PianoNote(Note(chromatic=7, diatonic=4), finger=1),
            PianoNote(Note(chromatic=9, diatonic=5), finger=3),
            PianoNote(Note(chromatic=11, diatonic=6), finger=2),
            PianoNote(Note(chromatic=12, diatonic=7), finger=1),
            PianoNote(Note(chromatic=14, diatonic=8), finger=4),
            PianoNote(Note(chromatic=15, diatonic=9), finger=3),
            PianoNote(Note(chromatic=17, diatonic=10), finger=2),
            PianoNote(Note(chromatic=19, diatonic=11), finger=1),
            PianoNote(Note(chromatic=21, diatonic=12), finger=3),
            PianoNote(Note(chromatic=23, diatonic=13), finger=2),
            PianoNote(Note(chromatic=24, diatonic=14), finger=1),
        ]
        self.assertEquals(
            self.left_minor_melodic_fingering.generate(lowest_or_highest_note=self.tonic, scale_pattern=minor_melodic,
                                                       number_of_octaves=2),
            two_octaves)
        two_octaves.reverse()
        self.assertEquals(
            self.left_minor_melodic_fingering.generate(lowest_or_highest_note=self.tonic.add_octave(2),
                                                       scale_pattern=minor_melodic,
                                                       number_of_octaves=-2),
            two_octaves)
