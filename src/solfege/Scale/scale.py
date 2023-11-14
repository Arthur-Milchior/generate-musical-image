from __future__ import annotations

from typing import List, Generic

from solfege.note.abstract import NoteType


class Scale(Generic[NoteType]):
    notes: List[NoteType]

    def __init__(self, notes: List[NoteType]):
        self.notes = notes

    def __eq__(self, other):
        return self.notes == other.notes

    def __repr__(self):
        return f"Scale(notes={self.notes})"
