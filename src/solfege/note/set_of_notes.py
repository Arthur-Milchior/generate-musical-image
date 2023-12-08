from __future__ import annotations

import unittest
from typing import Optional, List, Union

from lily.Lilyable.lilyable import Lilyable
from solfege.interval.set_of_intervals import SetOfIntervals
from solfege.interval.interval import Interval
from solfege.note import Note


class SetOfNotes(Lilyable):
    notes: List[Note]
    fundamental: Optional[Note]

    def __init__(self, notes: List[Note], fundamental: Optional[Note] = None):
        self.notes = notes
        self.fundamental = fundamental

    def __eq__(self, other: SetOfNotes):
        return self.notes == other.notes and self.fundamental == other.fundamental

    def __radd__(self, interval: Interval):
        return self + interval

    def __add__(self, interval: Interval):
        fundamental = self.fundamental + interval if self.fundamental else None
        return SetOfNotes([note + interval for note in self.notes], fundamental=fundamental)

    def __sub__(self, other: Union[Note, Interval]):
        if isinstance(other, Note):
            return SetOfIntervals([note - other for note in self.notes])
        return SetOfNotes([note - other for note in self.notes], self.fundamental - other if self.fundamental else None)

    def __iter__(self):
        return sorted(self.notes)

    def lily(self):
        return f"""<{" ".join(note.lily() for note in sorted(self.notes))}>"""

    def __repr__(self):
        return f"""SetOfNotes(notes={self.notes!r}{f", fundamental={self.fundamental!r}" if self.fundamental else ""}"""

    def __str__(self):
        return f"""SetOfNotes([{",".join(str(note) for note in self.notes)}]{f"/{self.fundamental}" if self.fundamental else ""}"""

    def add_octaves(self, octaves: int):
        return SetOfNotes([note.add_octave(octaves) for note in self.notes], self.fundamental.add_octave(octaves))


class TestSetOfNotes(unittest.TestCase):
    C_minor = SetOfNotes(
        [Note("C"),
         Note("E♭"),
         Note("G"),
         ])

    F_minor = SetOfNotes(
        [Note("F"),
         Note("A♭"),
         Note("C5"),
         ])

    def test_eq(self):
        self.assertNotEquals(self.C_minor, self.F_minor)
        self.assertEquals(self.C_minor, self.C_minor)

    def test_add(self):
        self.assertEquals(self.C_minor + Interval(diatonic=3, chromatic=5), self.F_minor)
