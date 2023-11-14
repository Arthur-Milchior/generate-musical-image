from __future__ import annotations

from typing import List

from solfege.note.base import AbstractNote


class Scale:
    def __init__(self, notes: List[AbstractNote]):
        self.notes = notes

    def __eq__(self, other):
        return self.notes == other.notes

    def __repr__(self):
        return f"Scale(notes={self.notes})"
