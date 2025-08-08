from __future__ import annotations

from typing import Generic, List

from solfege.interval import DiatonicInterval
from solfege.interval.abstract import IntervalType
from solfege.interval.interval import Interval
from src.utils.util import assert_all_same_class


class SetOfIntervals(Generic[IntervalType]):
    """A set of intervals, modulo octave"""

    def __init__(self, set_: List[IntervalType]):
        self.set_ = list()
        self.set_base_octave = set()
        for interval in set_:
            self.set_.append(interval)
            self.set_base_octave.add(interval.get_in_base_octave())
        
        # Checks all elements have the same class
        assert_all_same_class(set_)
        assert_all_same_class(self.set_base_octave)


    def __contains__(self, interval):
        """Whether this note belongs to the set (up to octave)"""
        return interval.get_in_base_octave() in self.set_base_octave

    def __iter__(self):
        """Intervals belonging to this set."""
        return iter(self.set_base_octave)

    def __add__(self, other: Interval):
        from solfege.note import Note
        from solfege.note.set_of_notes import SetOfNotes
        if isinstance(other, Note):
            return SetOfNotes([interval + other for interval in self.set_])
        return SetOfIntervals([interval + other for interval in self.set_])

    def __eq__(self, other: SetOfIntervals[IntervalType]):
        return self.set_ == other.set_

    def __repr__(self):
        return f"""SetOfIntervals(set_={self.set_})"""


