from __future__ import annotations

from dataclasses import dataclass
from typing import List

from lily.Lilyable.list_piano_lilyable import ListPianoLilyable
from lily.Lilyable.piano_lilyable import PianoLilyable
from lily.lily import compile_
# from piano.progression.pattern import NamedIntervalsPattern, ChordProgressionPattern
from solfege.interval.interval import Interval
from solfege.note import Note
from solfege.note.set_of_notes import SetOfNotes
from utils.constants import test_folder
from utils.util import indent


@dataclass(frozen=True, eq=True)
class TwoHandsChord(PianoLilyable):
    name: str
    left_hand: SetOfNotes
    right_hand: SetOfNotes
    tonic: Note = Note("C4")

    def left_lily(self):
        return self.left_hand.lily_in_scale()

    def right_lily(self):
        return self.right_hand.lily_in_scale()

    def annotations_lily(self):
        return self.name

    def first_key(self) -> str:
        """The lily code for the annotation"""
        return self.tonic.lily_in_scale()

    def __add__(self, other: Interval):
        return TwoHandsChord(self.name, self.left_hand + other, self.right_hand + other, self.tonic + other)

    def __sub__(self, other: Interval
                # Union[Note, Interval]
                ):
        # if isinstance(other, Note):
        #     return NamedIntervalsPattern(role=self.name, left_hand=self.left_hand - other,
        #                                  right_hand=self.right_hand - other)
        return TwoHandsChord(self.name, left_hand=self.left_hand - other, right_hand=self.right_hand - other,
                             tonic=self.tonic - other)


class ChordProgression(ListPianoLilyable):
    progression_name: str
    disambiguation: str
    key: Note
    chords: List[TwoHandsChord]

    def __init__(self, progression_name: str, disambiguation: str, key: Note, chords: List[TwoHandsChord]):
        super().__init__(chords)
        self.progression_name = progression_name
        self.key = key
        self.disambiguation = disambiguation
        self.chords = chords

    def __add__(self, other: Interval):
        return ChordProgression(self.progression_name, self.disambiguation, self.key + other,
                                [chord + other for chord in self.chords])

    def __radd__(self, other: Interval):
        return self + other

    def first_chord(self):
        first_chord = self.chords[0]
        return ChordProgression(first_chord.name, disambiguation=self.disambiguation, key=self.key,
                                chords=[first_chord])

    def __sub__(self, other: Interval  # Optional[Note, Interval]
                ):
        # if isinstance(other, Note):
        #     return ChordProgressionPattern(name=self.progression_name, chords=[chord - other for chord in self.chords])
        return ChordProgression(progression_name=self.progression_name, disambiguation=self.progression_name,
                                key=self.key - other, chords=[chord - other for chord in self.chords])


