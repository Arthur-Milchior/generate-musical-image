import unittest
from dataclasses import dataclass
from typing import Optional

import solfege.note
from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.note import Note


@dataclass
class PianoNote:
    """Represents a note played on the keyboard."""
    note: Note
    finger: int

    def __str__(self):
        return f"{self.note}-{self.finger}"


    def lily(self, use_color=True):
        try:
            return f"{self.note.lily(use_color=use_color)}-{self.finger}"
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

class TestPianoNote(unittest.TestCase):
    def test_lily(self):
        self.assertEquals(PianoNote(Note(chromatic=0, diatonic=0), finger=1).lily(use_color=False), "c'-1")
