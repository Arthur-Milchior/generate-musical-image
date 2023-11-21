import unittest
from dataclasses import dataclass
from typing import Optional

import solfege.note
from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.note import Note


class PianoNote(Note):
    """Represents a note played on the keyboard."""
    finger: int
    ClassToTransposeTo = Note

    def __eq__(self, other):
        if isinstance(other, PianoNote):
            if self.finger != other.finger:
                return False
        return self.value == other.value and self.get_diatonic() == other.get_diatonic()

    def __hash__(self):
        return hash((super().__hash__(), self.finger))

    def __init__(self, chromatic: int, diatonic: int, finger: int):
        super().__init__(chromatic=chromatic, diatonic=diatonic)
        self.finger = finger

    def __str__(self):
        return f"{super().__str__()}-{self.finger}"

    def lily(self, use_color=True):
        try:
            return f"{super().lily(use_color=use_color)}-{self.finger}"
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise


class TestPianoNote(unittest.TestCase):
    def test_lily(self):
        self.assertEquals(PianoNote(chromatic=0, diatonic=0, finger=1).lily(use_color=False), "c'-1")
