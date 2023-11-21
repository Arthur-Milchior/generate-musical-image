from __future__ import annotations

from typing import List, Generic

from solfege.note.abstract import NoteType


class Scale(Generic[NoteType]):
    notes: List[NoteType]

    # pattern: ScalePattern

    def __init__(self, notes: List[NoteType], pattern  #: ScalePattern
                 ):
        self.notes = notes
        self.pattern = pattern

    def all_blacks(self):
        return all(note.is_black_key_on_piano() for note in self.notes)

    def __eq__(self, other):
        return self.notes == other.notes

    def __repr__(self):
        return f"Scale(notes={self.notes})"
