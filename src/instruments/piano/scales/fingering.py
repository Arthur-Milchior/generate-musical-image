from __future__ import annotations

from typing import Dict, Optional, Union, List

from instruments.piano.piano_note import PianoNote
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note
from solfege.pattern.scale.scale_pattern import ScalePattern, minor_melodic
from utils.util import assert_typing

THUMB_TO_PINKY = -1
FOUR_TO_FOUR = 0
SAME_EXTREMITIES = 1
DIFFERENT_EXTREMITIES = 2


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

    @classmethod
    def from_scale(cls, scale: List[PianoNote], for_right_hand: bool) -> Optional[Fingering]:
        self = Fingering(for_right_hand)
        if for_right_hand:
            pinky_side_note = scale[-1]
            non_pinky_note = scale[:-1]
        else:
            pinky_side_note = scale[0]
            non_pinky_note = scale[1:]
        if pinky_side_note.finger == 1:
            return None
        self = self.add_pinky_side(pinky_side_note)
        for note in non_pinky_note:
            self = self.add(note)
        return self

    def _copy(self) -> Fingering:
        nex = Fingering(for_right_hand=self.for_right_hand)
        nex.tonic = self.tonic
        nex.pinky_side_tonic_finger = self.pinky_side_tonic_finger
        nex._dic = dict(self._dic)
        return nex

    def __eq__(self, other: Fingering) -> bool:
        assert isinstance(other, Fingering)
        assert self.for_right_hand == other.for_right_hand  # If we compare fingering for left and right hand, there is a bug somewhere
        return self.tonic == other.tonic and self._dic == other._dic and self.pinky_side_tonic_finger == other.pinky_side_tonic_finger

    def __contains__(self, note: Note) -> bool:
        assert not isinstance(note, PianoNote)
        note = note.in_base_octave()
        return note in self._dic

    def add_pinky_side(self, note: PianoNote) -> Fingering:
        assert_typing(note, PianoNote)
        assert self.pinky_side_tonic_finger is None
        assert note.finger != 1
        nex = self._copy()
        note_in_base_octave = note.in_base_octave()
        nex.pinky_side_tonic_finger = note.finger
        nex.tonic = note_in_base_octave
        return nex

    def add(self, note: PianoNote) -> Union[Fingering, bool]:
        """
        Returns:
            * False if the note was already here in the fingering with a different finger
            * True if the note was already in the fingering with this finger
            * A new fingering, similar to self, plus this note associated to this finger.
            In this last case, if `self` is empty, this note is assumed to be the tonic.
            """
        # assert self.pinky_side_tonic_finger is not None  # scales generation starts with pinky side.
        nex = self._copy()
        note_in_base_octave = note.in_base_octave()
        assert not isinstance(note_in_base_octave, PianoNote)
        if note_in_base_octave in nex._dic:
            return nex._dic[note_in_base_octave] == note.finger
        nex._dic[note_in_base_octave] = note.finger
        return nex

    def ends_and_start_on_same_finger(self) -> bool:
        """Whether the first and last finger of the scale's fingering are the same"""
        return self.get_thumb_side_tonic_finger() == self.get_pinky_side_tonic_finger()

    def pinky_to_thumb(self) -> bool:
        """Whether the last finger of the scale's fingering is a thumb"""
        return self.ends_with_a_thumb() and self.get_pinky_side_tonic_finger() == 5

    def pinky_to_thumb_on_white(self) -> bool:
        return self.pinky_to_thumb() and not self.tonic.is_black_key_on_piano()

    def ends_with_a_thumb(self) -> bool:
        """Whether the last finger of the scale's fingering is a thumb"""
        return self.get_thumb_side_tonic_finger() == 1

    def avoid_this_extremity(self) -> bool:
        """Whether it's something really to avoid."""
        if self.pinky_side_tonic_finger is None:
            return False
        if self.pinky_to_thumb():
            return False
        return self.pinky_side_tonic_finger != self.get_thumb_side_tonic_finger()

    def is_extremity_nice(self) -> int:
        """Whether the ends of the scale allows for a nice transition to second octave"""
        if self.pinky_to_thumb() and not self.tonic.is_black_key_on_piano():
            return THUMB_TO_PINKY
        if self.get_thumb_side_tonic_finger() == self.get_pinky_side_tonic_finger():
            if self.get_thumb_side_tonic_finger() == 4:
                return FOUR_TO_FOUR
            return SAME_EXTREMITIES
        return DIFFERENT_EXTREMITIES

    def get_thumb_side_tonic_finger(self) -> Optional[int]:
        return self.get_finger(self.tonic)

    def get_pinky_side_tonic_finger(self) -> Optional[int]:
        return self.pinky_side_tonic_finger

    def get_finger(self, note: Note, pinky_side_finger=False) -> Optional[int]:
        """Get the finger for `note`.
        If `note` is the tonic and `starting_finger` holds, get the starting finger"""
        note = note.in_base_octave()
        if pinky_side_finger:
            assert note.equals_modulo_octave(self.tonic)
            return self.pinky_side_tonic_finger
        assert not isinstance(note, PianoNote)
        return self._dic.get(note)

    def __repr__(self):
        text = f"""scales(for_right_hand={self.for_right_hand})"""
        if self.tonic:
            text += f""".\n  add_pinky_side(PianoNote.make(chromatic={self.tonic.get_chromatic().value}, diatonic={self.tonic.get_diatonic().value}, finger={self.pinky_side_tonic_finger}))"""
        for note, finger in self._dic.items():
            text += f""".\n  add(PianoNote.make(chromatic={note.get_chromatic().value}, diatonic={note.get_diatonic().value}, finger={finger}))"""
        return text

    def generate(self, first_played_note: Note, scale_pattern: ScalePattern, number_of_octaves: int = 1) -> \
            List[PianoNote]:
        assert first_played_note.equals_modulo_octave(self.tonic)
        assert number_of_octaves != 0
        scale = scale_pattern.from_note(first_played_note, number_of_octaves=number_of_octaves)
        fingered_scale = [
            PianoNote.make(chromatic=note.get_chromatic().value, diatonic=note.get_diatonic().value,
                      finger=self.get_finger(note)) for note in scale.notes]
        pos_of_pinky_side_extremity = -1 if (self.for_right_hand and number_of_octaves > 0) or (
                not self.for_right_hand and number_of_octaves < 0) else 0
        last_note = fingered_scale[pos_of_pinky_side_extremity]
        last_note.finger = self.get_finger(note=last_note, pinky_side_finger=True)
        return fingered_scale


# Test section
