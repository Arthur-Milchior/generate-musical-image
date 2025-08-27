from __future__ import annotations

from typing import Optional, List, Union

from lily.Lilyable.local_lilyable import LocalLilyable
from solfege.interval.interval import Interval
from solfege.interval.set.set_of_intervals import SetOfIntervals
from solfege.note.note import Note


class SetOfNotes(LocalLilyable):
    notes: List[Note]
    tonic: Optional[Note]

    def __init__(self, notes: List[Note], tonic: Optional[Note] = None):
        self.notes = notes
        self.tonic = tonic

    def __eq__(self, other: SetOfNotes):
        return self.notes == other.notes and self.tonic == other.tonic

    def __radd__(self, interval: Interval):
        return self + interval

    def __add__(self, interval: Interval):
        tonic = self.tonic + interval if self.tonic else None
        return SetOfNotes([note + interval for note in self.notes], tonic=tonic)

    def __sub__(self, other: Union[Note, Interval]):
        if isinstance(other, Note):
            return SetOfIntervals.make([note - other for note in self.notes])
        return SetOfNotes([note - other for note in self.notes], self.tonic - other if self.tonic else None)

    def __iter__(self):
        return sorted(self.notes)

    def lily_in_scale(self):
        return f"""<{" ".join(note.lily_in_scale() for note in sorted(self.notes))}>"""

    def __repr__(self):
        return f"""SetOfNotes(notes={self.notes!r}{f", tonic={self.tonic!r}" if self.tonic else ""}"""

    def __str__(self):
        return f"""SetOfNotes([{",".join(str(note) for note in self.notes)}]{f"/{self.tonic}" if self.tonic else ""}"""

    def add_octaves(self, octaves: int):
        return SetOfNotes([note.add_octave(octaves) for note in self.notes], self.tonic.add_octave(octaves))


