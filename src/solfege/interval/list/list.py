from dataclasses import dataclass
from typing import List, Tuple, Union

from solfege.interval.interval import Interval, unison
from solfege.note.abstract_note import AbstractNote
from solfege.note.chromatic_note import ChromaticNote
from solfege.note.note import Note
from utils.util import assert_typing


@dataclass(frozen=True)
class IntervalList:
    """The list of intervals, all relative to a common starting note."""
    _absolute_intervals: List[Interval]

    def __post_init__(self):
        assert self._absolute_intervals[0] == unison
        assert_typing(self._absolute_intervals, list)
        for interval in self._absolute_intervals:
            assert_typing(interval, Interval) 

    @classmethod
    def make_absolute(cls, absolute_intervals: List[Union[int, Interval, Tuple[int, int]]], *args, add_implicit_zero: bool = True, **kwargs):
        absolute_intervals = [Interval.make_single_argument(absolute_interval) for absolute_interval in absolute_intervals]
        first_interval = absolute_intervals[0]
        if first_interval != unison and add_implicit_zero:
            absolute_intervals = [unison] + absolute_intervals
        return cls(absolute_intervals, *args, **kwargs)

    @classmethod
    def make_relative(cls, relative_intervals: List[Union[int, Interval, Tuple[int, int]]], *args, **kwargs):
        absolute_intervals = [unison]
        for relative_interval in relative_intervals:
            relative_interval = Interval.make_single_argument(relative_interval)
            absolute_intervals.append(absolute_intervals[-1] + relative_interval)
        return cls(absolute_intervals, *args, **kwargs)

    def absolute_intervals(self):
        yield from self._absolute_intervals

    def relative_intervals(self, assume_implicit_zero=True):
        assert self._absolute_intervals[0] == unison
        for i in range(len(self._absolute_intervals)-1):
            yield self._absolute_intervals[i+1] - self._absolute_intervals[i]

    def from_note(self, note: Union[ChromaticNote, Note]):
        for absolute_interval in self._absolute_intervals:
            if isinstance(note, ChromaticNote):
                absolute_interval = absolute_interval.chromatic
            yield note + absolute_interval

    def relative_chromatic(self):
        for interval in self.relative_intervals():
            yield interval.chromatic

    def relative_diatonic(self):
        for interval in self.relative_intervals():
            yield interval.diatonic

    def absolute_chromatic(self):
        for interval in self.absolute_intervals():
            yield interval.chromatic

    def absolute_diatonic(self):
        for interval in self.absolute_intervals():
            yield interval.diatonic