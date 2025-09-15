from dataclasses import dataclass
from typing import Callable, ClassVar, Dict, Generic, Iterable, List, Self, Tuple, Type, TypeVar, Union

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.set.abstract_interval_ilst_pattern import AbstractIntervalListPattern
from utils.util import assert_iterable_typing, assert_typing, sorted_unique


@dataclass(frozen=True, unsafe_hash=True, repr=False)
class ChromaticIntervalListPattern(AbstractIntervalListPattern[ChromaticInterval]):
    interval_type: ClassVar[Type[ChromaticInterval]] = ChromaticInterval
    note_list_type: ClassVar[Type]
    _frozen_list_type: ClassVar[Type] = ChromaticIntervalFrozenList

    @classmethod
    def _note_list_constructor(cls):
        from solfege.value.note.set.note_list import ChromaticNoteList
        return ChromaticNoteList
    
    @staticmethod
    def interval_repr(interval: ChromaticInterval) -> str:
        "How to display the interval in make."
        return str(interval.value)