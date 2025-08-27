from dataclasses import dataclass
from itertools import pairwise
from typing import ClassVar, Generic, Iterable, List, Tuple, Type, Union

from solfege.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.interval.chromatic_interval import ChromaticInterval
from solfege.interval.interval import Interval
from solfege.note.abstract_note import AbstractNote
from solfege.note.chromatic_note import ChromaticNote
from solfege.note.note import Note
from solfege.value.chromatic import ChromaticGetter
from utils.frozenlist import FrozenList
from utils.util import assert_typing

@dataclass(frozen=True)
class AbstractIntervalList(Generic[IntervalType]):
    interval_type: ClassVar[Type[AbstractInterval]]
    """The list of intervals, all relative to a common starting note."""
    _absolute_intervals: FrozenList[IntervalType]
    increasing: bool

    def __post_init__(self):
        assert self._absolute_intervals[0] == self.interval_type.unison()
        assert_typing(self._absolute_intervals, FrozenList)
        for interval in self._absolute_intervals:
            assert_typing(interval, self.interval_type)
        for first, second in pairwise(self._absolute_intervals):
            if self.increasing:
                assert first < second
            else:
                assert first > second

    @classmethod
    def make_absolute(cls, absolute_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]], *args, increasing:bool = True, add_implicit_zero: bool = True, **kwargs):
        absolute_intervals = [cls.interval_type.make_single_argument(absolute_interval) for absolute_interval in absolute_intervals]
        first_interval = absolute_intervals[0]
        unison = cls.interval_type.unison()
        if first_interval != unison and add_implicit_zero:
            absolute_intervals = [unison] + absolute_intervals
        return cls(FrozenList(absolute_intervals), *args,increasing=increasing, **kwargs)

    @classmethod
    def make_relative(cls, relative_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]], *args, increasing:bool = True, **kwargs):
        unison = cls.interval_type.unison()
        absolute_intervals = [unison]
        for relative_interval in relative_intervals:
            relative_interval = cls.interval_type.make_single_argument(relative_interval)
            absolute_intervals.append(absolute_intervals[-1] + relative_interval)
        return cls(FrozenList(absolute_intervals), *args, increasing=increasing, **kwargs)

    def absolute_intervals(self):
        yield from self._absolute_intervals

    def relative_intervals(self, assume_implicit_zero=True):
        unison = self.interval_type.unison()
        assert self._absolute_intervals[0] == unison
        for lower, higher in pairwise(self._absolute_intervals):
            yield higher - lower

    def from_note(self, note: AbstractNote):
        for absolute_interval in self._absolute_intervals:
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

    def __hash__(self):
        return hash(frozenset())        

@dataclass(frozen=True)
class IntervalList(AbstractIntervalList[Interval]):
    interval_type: ClassVar[Type[Interval]] = Interval

    def get_chromatic(self):
        return ChromaticIntervalList(FrozenList([interval.get_chromatic() for interval in self.absolute_chromatic()]), increasing=self.increasing)


@dataclass(frozen=True)
class ChromaticIntervalList(AbstractIntervalList[ChromaticInterval]):
    interval_type: ClassVar[Type[ChromaticInterval]] = ChromaticInterval
