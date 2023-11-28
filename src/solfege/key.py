from __future__ import annotations

import unittest

from solfege.note import Note


class Key:
    note: Note
    number_of_flats: int = 0
    number_of_sharps: int = 0
    _from_note = dict()

    def __init__(self, note: Note, number_of_flats: int = 0, number_of_sharps: int = 0):
        self.note = note
        self.number_of_flats = number_of_flats
        self.number_of_sharps = number_of_sharps
        self._from_note[note] = self

    def _number_of_alterations(self):
        return self.number_of_flats + self.number_of_sharps

    @classmethod
    def from_note(cls, note: Note):
        return cls._from_note[note.get_in_base_octave()]

    def __eq__(self, other):
        return self.note == other.note

    def __hash__(self):
        return hash(self.note)

    def __le__(self, other: Key):
        return (self._number_of_alterations(), self.note) <= (other._number_of_alterations(), other.note)

    def __lt__(self, other: Key):
        return (self._number_of_alterations(), self.note) < (other._number_of_alterations(), other.note)

    def __str__(self):
        return self.note.get_symbol_name() + (f" with {self.number_of_flats} ♭" if self.number_of_flats else "") + (
            f" with {self.number_of_sharps} #" if self.number_of_sharps else "")


key_of_C = Key(Note.from_name("C"))

"""All keys, grouped by enharmonic, sorted by minimal number of alteration"""
sets_of_enharmonic_keys = [
    [
        key_of_C,
        Key(Note.from_name("D♭♭"), number_of_flats=12),
        Key(Note.from_name("B#"), number_of_flats=12),
    ],
    [
        Key(Note.from_name("F"), number_of_flats=1),
        Key(Note.from_name("E#"), number_of_sharps=11),
        Key(Note.from_name("G♭♭"), number_of_flats=13),
    ],
    [
        Key(Note.from_name("G"), number_of_sharps=1),
        Key(Note.from_name("A♭♭"), number_of_flats=11),
        Key(Note.from_name("F𝄪"), number_of_flats=13),
    ],
    [
        Key(Note.from_name("B♭"), number_of_flats=2),
        Key(Note.from_name("A#"), number_of_sharps=10),
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
        Key(Note.from_name("A"), number_of_sharps=3),
        Key(Note.from_name("B♭♭"), number_of_flats=9),
    ],
    [
        Key(Note.from_name("A♭"), number_of_flats=4),
        Key(Note.from_name("G#"), number_of_sharps=8),
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
        Key(Note.from_name("B"), number_of_sharps=5),
        Key(Note.from_name("C♭"), number_of_flats=7),
        Key(Note.from_name("A𝄪"), number_of_sharps=7),
    ],
    [
        Key(Note.from_name("F#"), number_of_flats=6),
        Key(Note.from_name("G♭"), number_of_sharps=6),
    ],
]


class TestClef(unittest.TestCase):

    def test_enharmonic(self):
        found = set()
        for enharmonic_key in sets_of_enharmonic_keys:
            chromatic_of_first_key = enharmonic_key[0].note.get_chromatic()
            self.assertNotIn(chromatic_of_first_key, found)
            found.add(chromatic_of_first_key)
            for key in enharmonic_key:
                chromatic_of_key = key.note.get_chromatic()
                self.assertTrue(chromatic_of_first_key.equals_modulo_octave(chromatic_of_key))
            for i in range(len(enharmonic_key) - 1):
                self.assertLessEqual(enharmonic_key[i], enharmonic_key[i + 1])

    # def test_alteration(self):
    #     self.assertEquals(enharmonic_keys[0].note.get_alteration(), IntervalMode(-1))
    #     self.assertEquals(enharmonic_keys[1].note.get_alteration(), IntervalMode(-1))
    #     self.assertEquals(enharmonic_keys[2].note.get_alteration(), IntervalMode(-1))
    #     self.assertEquals(enharmonic_keys[3].note.get_alteration(), IntervalMode(-1))
    #     self.assertEquals(enharmonic_keys[4].note.get_alteration(), IntervalMode(-1))
    #     self.assertEquals(enharmonic_keys[5].note.get_alteration(), IntervalMode(-1))
    #     self.assertEquals(enharmonic_keys[6].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[7].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[8].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[9].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[10].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[11].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[12].note.get_alteration(), IntervalMode(0))
    #     self.assertEquals(enharmonic_keys[13].note.get_alteration(), IntervalMode(1))
    #     self.assertEquals(enharmonic_keys[14].note.get_alteration(), IntervalMode(1))

    def test_get(self):
        self.assertEquals(key_of_C, Key.from_note(Note.from_name("C")))
