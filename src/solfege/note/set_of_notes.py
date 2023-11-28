from __future__ import annotations

import unittest
from typing import Optional, FrozenSet, List

from lily.Interface import Lilyable
from util import _indent
from solfege.interval.interval import Interval
from solfege.note import Note


class SetOfNotes(Lilyable):
    fundamental: Optional[Note]
    notes: List[Note]

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

    def __iter__(self):
        return sorted(self.notes)

    def lily(self):
        newline = "\n"
        return f"""\\clef treble <
{_indent(newline.join(note.lily() for note in sorted(self.notes)))}
>"""

    def __repr__(self):
        return f"""SetOfNotes(notes={self.notes!r}{f", fundamental={self.fundamental!r}" if self.fundamental else ""}"""

    def __str__(self):
        return f"""SetOfNotes([{",".join(str(note) for note in self.notes)}]{f"/{self.fundamental}" if self.fundamental else ""}"""


class TestSetOfNotes(unittest.TestCase):
    C_minor = SetOfNotes(
        [Note.from_name("C"),
         Note.from_name("E♭"),
         Note.from_name("G"),
         ])

    F_minor = SetOfNotes(
        [Note.from_name("F"),
         Note.from_name("A♭"),
         Note.from_name("C5"),
         ])

    def test_eq(self):
        self.assertNotEquals(self.C_minor, self.F_minor)
        self.assertEquals(self.C_minor, self.C_minor)

    def test_add(self):
        self.assertEquals(self.C_minor + Interval(diatonic=3, chromatic=5), self.F_minor)

    def test_lily(self):
        self.assertEquals(self.C_minor.lily(), """\\clef treble <
  c'
  ees'
  g'
>""")
