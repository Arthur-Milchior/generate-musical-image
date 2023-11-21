import unittest
from dataclasses import dataclass

from solfege.note import Note, IntervalMode


@dataclass
class Clef:
    note: Note
    number_of_flats: int = 0
    number_of_sharps: int = 0

    def __str__(self):
        return f"{self.note}" + (f" with {self.number_of_flats} ♭" if self.number_of_flats else "")+ (f" with {self.number_of_sharps} #" if self.number_of_sharps else "")


clefs = [
    Clef(Note(chromatic=11, diatonic=7), number_of_flats=7),  # Cb
    Clef(Note(chromatic=6, diatonic=4), number_of_flats=6),  # Gb
    Clef(Note(chromatic=1, diatonic=1), number_of_flats=5),  # Db
    Clef(Note(chromatic=8, diatonic=5), number_of_flats=4),  # Ab
    Clef(Note(chromatic=3, diatonic=2), number_of_flats=3),  # Eb
    Clef(Note(chromatic=10, diatonic=6), number_of_flats=2),  # Bb
    Clef(Note(chromatic=5, diatonic=3), number_of_flats=1),  # F
    Clef(Note(chromatic=0, diatonic=0)),  # C
    Clef(Note(chromatic=7, diatonic=4), number_of_sharps=1),  # G
    Clef(Note(chromatic=2, diatonic=1), number_of_sharps=2),  # D
    Clef(Note(chromatic=9, diatonic=5), number_of_sharps=3),  # A
    Clef(Note(chromatic=4, diatonic=2), number_of_sharps=4),  # E
    Clef(Note(chromatic=11, diatonic=6), number_of_sharps=5),  # B
    Clef(Note(chromatic=6, diatonic=3), number_of_sharps=6),  # F#
    Clef(Note(chromatic=1, diatonic=0), number_of_sharps=7),  # C#
]


class TestClef(unittest.TestCase):
    def test_alteration(self):
        self.assertEquals(clefs[0].note.get_alteration(), IntervalMode(-1))
        self.assertEquals(clefs[1].note.get_alteration(), IntervalMode(-1))
        self.assertEquals(clefs[2].note.get_alteration(), IntervalMode(-1))
        self.assertEquals(clefs[3].note.get_alteration(), IntervalMode(-1))
        self.assertEquals(clefs[4].note.get_alteration(), IntervalMode(-1))
        self.assertEquals(clefs[5].note.get_alteration(), IntervalMode(-1))
        self.assertEquals(clefs[6].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[7].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[8].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[9].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[10].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[11].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[12].note.get_alteration(), IntervalMode(0))
        self.assertEquals(clefs[13].note.get_alteration(), IntervalMode(1))
        self.assertEquals(clefs[14].note.get_alteration(), IntervalMode(1))
