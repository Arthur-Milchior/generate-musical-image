from __future__ import annotations

from typing import Dict, List

from solfege.interval.interval import Interval
from solfege.note.note import Note
from solfege.note.abstract_note import OctaveOutput
from utils.util import assert_typing


class Key:
    note: Note
    number_of_flats: int = 0
    number_of_sharps: int = 0
    _from_note = dict()
    _key_to_simplest_enharmonic: Dict[Note, Note] = {}

    def __init__(self, note: Note, number_of_flats: int = 0, number_of_sharps: int = 0):
        assert_typing(note, Note)
        assert_typing(number_of_flats, int)
        assert_typing(number_of_sharps, int)
        self.note = note
        self.number_of_flats = number_of_flats
        self.number_of_sharps = number_of_sharps
        self._from_note[note.in_base_octave()] = self

    def simplest_enharmonic_major(self):
        return self.from_note(self._key_to_simplest_enharmonic[self.note.in_base_octave()])

    def simplest_enharmonic_minor(self):
        relative_interval = Interval.make(chromatic=3, diatonic=2)
        return self.from_note(
            self._key_to_simplest_enharmonic[(self.note + relative_interval).in_base_octave()] - relative_interval)

    @classmethod
    def add_enharmonic_set(cls, enharmonic_set: List[Key]):
        simplest = enharmonic_set[0]
        for key in enharmonic_set:
            cls._key_to_simplest_enharmonic[key.note.in_base_octave()] = simplest.note

    def _number_of_alterations(self):
        return self.number_of_flats + self.number_of_sharps

    @classmethod
    def from_note(cls, note: Note) -> Key:
        return cls._from_note[note.in_base_octave()]

    def __eq__(self, other):
        return self.note == other.note

    def __hash__(self):
        return hash(self.note)

    def __le__(self, other: Key):
        return (self._number_of_alterations(), self.note) <= (other._number_of_alterations(), other.note)

    def __lt__(self, other: Key):
        return (self._number_of_alterations(), self.note) < (other._number_of_alterations(), other.note)

    def __str__(self):
        return self.note.get_name_with_octave(octave_notation=OctaveOutput.OCTAVE_MIDDLE_PIANO_4, ascii=False) + (f" with {self.number_of_flats} ♭" if self.number_of_flats else "") + (
            f" with {self.number_of_sharps} #" if self.number_of_sharps else "")


key_of_C = Key(Note.from_name("C"))
key_of_A = Key(Note.from_name("A3"), number_of_sharps=3)

"""All keys, grouped by enharmonic, sorted by minimal number of alteration"""
sets_of_enharmonic_keys = [
    [
        key_of_C,
        Key(Note.from_name("D♭♭"), number_of_flats=12),
        Key(Note.from_name("B#3"), number_of_flats=12),
    ],
    [
        Key(Note.from_name("F3"), number_of_flats=1),
        Key(Note.from_name("E#"), number_of_sharps=11),
        Key(Note.from_name("G♭♭3"), number_of_flats=13),
    ],
    [
        Key(Note.from_name("G"), number_of_sharps=1),
        Key(Note.from_name("A♭♭3"), number_of_flats=11),
        Key(Note.from_name("F𝄪3"), number_of_flats=13),
    ],
    [
        Key(Note.from_name("B♭3"), number_of_flats=2),
        Key(Note.from_name("A#3"), number_of_sharps=10),
        Key(Note.from_name("C♭♭"), number_of_flats=14),
    ],
    [
        Key(Note.from_name("D"), number_of_sharps=2),
        Key(Note.from_name("E♭♭"), number_of_flats=10),
        Key(Note.from_name("C𝄪"), number_of_flats=14),
    ],
    [
        Key(Note.from_name("E♭"), number_of_flats=3),
        Key(Note.from_name("D#"), number_of_sharps=9),
    ],
    [
        key_of_A,
        Key(Note.from_name("B♭♭3"), number_of_flats=9),
    ],
    [
        Key(Note.from_name("A♭3"), number_of_flats=4),
        Key(Note.from_name("G#3"), number_of_sharps=8),
    ],
    [
        Key(Note.from_name("E"), number_of_sharps=4),
        Key(Note.from_name("F♭"), number_of_flats=8),
    ],
    [
        Key(Note.from_name("D♭"), number_of_flats=5),
        Key(Note.from_name("C#"), number_of_sharps=7),
    ],
    [
        Key(Note.from_name("B3"), number_of_sharps=5),
        Key(Note.from_name("C♭"), number_of_flats=7),
        Key(Note.from_name("A𝄪3"), number_of_sharps=7),
    ],
    [
        Key(Note.from_name("F#3"), number_of_flats=6),
        Key(Note.from_name("G♭3"), number_of_sharps=6),
    ],
]

for enharmonic_set in sets_of_enharmonic_keys:
    Key.add_enharmonic_set(enharmonic_set)

seven_sharps = Interval.make(diatonic=0, chromatic=1)  # when playing a C scale, have C# major signature, 3 sharps
three_sharps = Interval.make(diatonic=5, chromatic=9)  # when playing a C scale, have A major signature, 3 sharps
two_sharps = Interval.make(diatonic=1, chromatic=2)  # when playing a C scale, have D major signature, 2 sharps
one_sharp = Interval.make(diatonic=4, chromatic=7)  # when playing a C scale, have G major signature, 1 sharp
nor_flat_nor_sharp = Interval.make(diatonic=0, chromatic=0)  # when playing a C scale, have C signature
one_flat = Interval.make(diatonic=3, chromatic=5)  # when playing a C scale, have F major signature, 1 flat
two_flats = Interval.make(diatonic=6, chromatic=10)  # when playing a C scale, have Bb major signature, 2 flats
three_flats = Interval.make(diatonic=2, chromatic=3)  # when playing a C scale, have Eb major signature, 3 flats
four_flats = Interval.make(diatonic=5, chromatic=8)  # when playing a C scale, have Ab major signature, 4 flats
five_flats = Interval.make(diatonic=1, chromatic=1)  # when playing a C scale, have Bb major signature, 5 flats
height_flats = Interval.make(diatonic=3, chromatic=4)  # when playing a C scale, have Fb major signature, 8 flats including Bbb


