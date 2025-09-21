from dataclasses import dataclass
from itertools import pairwise
from typing import Callable, ClassVar, Dict, Generic, Iterable, List, Self, Tuple, Type, TypeVar, Union

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.abstract_interval_ilst_pattern import AbstractIntervalListPattern
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern
from utils.frozenlist import FrozenList
from utils.util import assert_iterable_typing, assert_typing, sorted_unique

@dataclass(frozen=True, unsafe_hash=True, repr=False)
class IntervalListPattern(AbstractIntervalListPattern[Interval]):
    interval_type: ClassVar[Type[Interval]] = Interval
    _frozen_list_type: ClassVar[Type] = IntervalFrozenList

    @classmethod
    def _note_list_constructor(cls):
        from solfege.value.note.set.note_list import NoteList
        return NoteList
    
    @staticmethod
    def interval_repr(interval: Interval) -> str:
        "How to display the interval in make."
        return f"""({interval._chromatic.value}, {interval._diatonic.value})"""

    def get_chromatic_interval_list(self) -> ChromaticIntervalListPattern:
        chromatic_interval_list = ChromaticIntervalListPattern.make_absolute([interval.get_chromatic() for interval in self._absolute_intervals], increasing=self.increasing)
        assert_typing(chromatic_interval_list, ChromaticIntervalListPattern)
        return chromatic_interval_list

    def get_interval_list(self) -> "IntervalListPattern":
        return IntervalListPattern(self._absolute_intervals, self.increasing)

    def best_enharmonic_starting_note(self, chromatic_note: "ChromaticNote"):
        """The chord with a note with this chromatic."""
        from solfege.value.note.chromatic_note import ChromaticNote
        from solfege.value.note.note import Note
        return min(Note.all_from_chromatic(chromatic_note), key = lambda note: self.from_note(note).easy_key())

class IntervalListFrozenList(FrozenList[IntervalListPattern]):
    type = IntervalListPattern
