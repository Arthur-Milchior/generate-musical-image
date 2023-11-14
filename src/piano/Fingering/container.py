from __future__ import annotations

import unittest
from typing import Dict, Optional

from piano.pianonote import PianoNote
from solfege.note import Note
from solfege.note.with_tonic import NoteWithTonic
from solfege.Scale.pattern import ScalePattern


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
    right_hand: bool

    """The finger used to play the tonic once at an extremety. Usually the fifth, or sometime fourth, to start the 
    increasing scale on the left hand and to end the increasing scale on the right end."""
    finger_for_the_tonic_at_start: bool

    def __init__(self, right_hand: bool = True):
        self._dic = dict()
        self.tonic = None
        self.right_hand = right_hand
        self.finger_for_the_tonic_at_start = None

    def _copy(self) -> Fingering:
        nex = Fingering()
        nex.tonic = self.tonic
        nex.finger_for_the_tonic_at_start = self.finger_for_the_tonic_at_start
        nex.right_hand = self.right_hand
        nex._dic = dict(self._dic)
        return nex

    def __contains__(self, note):
        note = note.get_in_base_octave()
        return note in self._dic

    def add(self, note, finger) -> Fingering:
        """
        Returns:
            * False if the note was already here in the fingering with a different finger
            * True if the note was already in the fingering with this finger
            * A new fingering, similar to self, plus this note associated to this finger.
            In this last case, if `self` is empty, this note is assumed to be the tonic.
            """
        nex = self._copy()
        note = note.get_in_base_octave()
        if self.tonic is None:
            nex.tonic = note
            nex.finger_for_the_tonic_at_start = finger
        else:
            if note in nex._dic:
                return nex._dic[note] == finger
            nex._dic[note] = finger
        return nex

    def ends_and_start_on_same_finger(self) -> bool:
        """Whether the first and last finger of the scale's fingering are the same"""
        return self.get_last_finger() == self.get_first_finger()

    def ends_with_a_thumb(self) -> bool:
        """Whether the last finger of the scale's fingering is a thumb"""
        return self.get_last_finger() == 1

    def is_end_nice(self) -> bool:
        """Whether the first and last finger is the thumb"""
        return self.ends_with_a_thumb() or self.ends_and_start_on_same_finger()

    def get_last_finger(self) -> Optional[int]:
        """The finger used to end the scale. Usually a 5"""
        return self.get_finger(self.tonic)

    def get_first_finger(self) -> Optional[int]:
        """The finger used to start the scale. Usually a thumb"""
        return self.finger_for_the_tonic_at_start

    def get_finger(self, note, starting_finger=False) -> Optional[int]:
        """Get the finger for `note`.
        If `note` is the tonic and `starting_finger` holds, get the starting finger"""
        note = note.get_in_base_octave()
        if starting_finger:
            assert (note == self.tonic)
            return self.finger_for_the_tonic_at_start
        return self._dic.get(note)

    def __repr__(self):
        text = f"""Fingering:{{ (base={self.tonic!r},{self.finger_for_the_tonic_at_start})"""
        for key in self._dic:
            text += f", ({key},{self._dic[key]})"
        text += "}"
        return text

    def concrete(self, starting_note: Note, scale: ScalePattern, number_of_octaves: int = 1):
        first_note =
        if self.is_right:

        lastNote = PianoNote(chromatic=starting_note.get_chromatic().get_number(), diatonic=starting_note.get_diatonic().get_number(), finger=self.get_finger(starting_note, starting_finger=True)).
        l = []



class TestFingering(unittest.TestCase):
    empty = Fingering(right_hand=True)
    tonic = NoteWithTonic(chromatic=0, diatonic=0, tonic=True)
    octave = NoteWithTonic(chromatic=12, diatonic=7, tonic=tonic)
    second = NoteWithTonic(chromatic=2, diatonic=1, tonic=tonic)
    thumb_0 = empty.add(tonic, 1)
    index_1 = thumb_0.add(second, 2)
    ended = index_1.add(octave, 5)

    def test_one_note(self):
        self.assertIsInstance(self.thumb_0, Fingering)
        self.assertEquals(self.thumb_0.get_first_finger(), 1)
        self.assertEquals(self.thumb_0.get_last_finger(), None)
        self.assertEquals(self.thumb_0.tonic, self.tonic)
        self.assertEquals(self.thumb_0.get_finger(self.tonic), None)
        self.assertEquals(self.thumb_0.get_finger(self.tonic, starting_finger=True), 1)
        self.assertEquals(self.thumb_0.get_finger(self.second), None)
        with self.assertRaises(Exception):
            self.thumb_0.get_finger(self.second, starting_finger=True)
        self.assertEquals(repr(self.thumb_0), "Fingering:{ (base=NoteWithTonic(value=0, repr=self),1)}")

    def test_ended(self):
        self.assertIsInstance(self.ended, Fingering)
        self.assertEquals(self.ended.get_first_finger(), 1)
        self.assertEquals(self.ended.get_last_finger(), 5)
        self.assertEquals(self.ended.tonic, self.tonic)
        self.assertEquals(self.ended.get_finger(self.tonic), 5)
        self.assertEquals(self.ended.get_finger(self.tonic, starting_finger=True), 1)
        self.assertEquals(self.ended.get_finger(self.second), 2)
        with self.assertRaises(Exception):
            self.ended.get_finger(self.second, starting_finger=True)

    def test_two_note(self):
        self.assertIsInstance(self.index_1, Fingering)
        self.assertEquals(self.index_1.get_first_finger(), 1)
        self.assertEquals(self.index_1.get_last_finger(), None)
        self.assertEquals(self.index_1.tonic, self.tonic)
        self.assertEquals(self.index_1.get_finger(self.tonic), None)
        self.assertEquals(self.index_1.get_finger(self.tonic, starting_finger=True), 1)
        self.assertEquals(self.index_1.get_finger(self.second), 2)
        with self.assertRaises(Exception):
            self.index_1.get_finger(self.second, starting_finger=True)
        self.assertEquals(repr(self.index_1), "Fingering:{ (base=NoteWithTonic(value=0, repr=self),1), "
                                              "(NoteWithTonic(value=2, repr=NoteWithTonic(value=0, repr=self)),2)}")

    def test_add_two_same_note(self):
        self.assertTrue(self.index_1.add(self.second, 2))
        self.assertFalse(self.index_1.add(self.second, 3))

    def test_add_three_tonic_same_note(self):
        self.assertTrue(self.ended.add(self.octave, 5))
        self.assertFalse(self.ended.add(self.octave, 1))
