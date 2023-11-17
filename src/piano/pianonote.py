import unittest
from dataclasses import dataclass
from typing import Optional

import solfege.note
from solfege.note import Note


@dataclass
class PianoNote:
    """Represents a note played on the keyboard."""
    note: Note
    finger: int

    def __str__(self):
        return f"{self.note}-{self.finger}"


    def lily(self, use_color=True):
        return f"{self.note.lily(use_color=use_color)}-{self.finger}"


class TestPianoNote(unittest.TestCase):
    def test_lily(self):
        self.assertEquals(PianoNote(Note(chromatic=0, diatonic=0), finger=1).lily(use_color=False), "c'-1")
