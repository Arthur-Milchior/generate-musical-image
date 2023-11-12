import unittest
from typing import Dict, Optional

from solfege.note import Note
from solfege.note.with_tonic import NoteWithTonic


class Fingering:
    """
    A non mutable class representing an association from note on the scale to one of the five finger of the hand.
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

    """The finger used to play the tonic"""
    finger_for_the_tonic_at_start: bool

    def __init__(self, right_hand: bool = True):
        self._dic = dict()
        self.tonic = None
        self.right_hand = right_hand
        self.finger_for_the_tonic_at_start = None

    def _copy(self):
        nex = Fingering()
        nex.tonic = self.tonic
        nex.finger_for_the_tonic_at_start = self.finger_for_the_tonic_at_start
        nex.right_hand = self.right_hand
        nex._dic = dict(self._dic)
        return nex

    def __contains__(self, note):
        note = note.get_in_base_octave()
        return note in self._dic

    def add(self, note, finger):
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

    def ends_and_start_on_same_finger(self):
        """Whether the first and last finger of the scale's fingering are the same"""
        return self.get_last_finger() == self.get_first_finger()

    def ends_with_a_thumb(self):
        """Whether the last finger of the scale's fingering is a thumb"""
        return self.get_last_finger() == 1

    def is_end_nice(self):
        """Whether the first and last finger is the thumb"""
        return self.ends_with_a_thumb() or self.ends_and_start_on_same_finger()

    def get_last_finger(self):
        """The finger used to end the scale. Usually a 5"""
        return self.get_finger(self.tonic)

    def get_first_finger(self):
        """The finger used to start the scale. Usually a thumb"""
        return self.finger_for_the_tonic_at_start

    def get_finger(self, note, starting_finger=False):
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

class TestFingering(unittest.TestCase):
    def test_add_first_note(self):
        empty = Fingering(right_hand=True)
        tonic = NoteWithTonic(chromatic=0, diatonic=0, tonic=True)
        thumb_0 = empty.add(tonic, 1)
        self.assertIsInstance(thumb_0, Fingering)
        self.assertEquals(thumb_0.get_first_finger(), 1)
        self.assertEquals(thumb_0.get_last_finger(), None)
        self.assertEquals(thumb_0.tonic, tonic)
        self.assertEquals(repr(thumb_0), "Fingering:{ (base=)}")
