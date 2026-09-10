from dataclasses import dataclass
from typing import Callable, ClassVar, Dict, Generic, Iterable, List, Self, Tuple, Type, TypeVar, Union

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.set.abstract_interval_list_pattern import AbstractIntervalListPattern
from utils.util import assert_iterable_typing, assert_typing, sorted_unique


@dataclass(frozen=True, unsafe_hash=True, repr=False)
class ChromaticIntervalListPattern(AbstractIntervalListPattern[ChromaticInterval]):
    """An `AbstractIntervalListPattern` holding only chromatic intervals, used when diatonic spelling
    doesn't matter (e.g. `IntervalList.get_chromatic_interval_list`)."""
    interval_type: ClassVar[Type[ChromaticInterval]] = ChromaticInterval
    """Intervals in this list are `ChromaticInterval`s."""
    note_list_type: ClassVar[Type]
    """The note-list class this pattern instantiates into (see `_note_list_constructor`)."""
    _frozen_list_type: ClassVar[Type] = ChromaticIntervalFrozenList
    """Storage type for `_absolute_intervals`."""

    @classmethod
    def _note_list_constructor(cls) -> Callable[["NoteType"], "AbstractNoteList"]:
        """Return `ChromaticNoteList`, the note-list type matching purely chromatic intervals."""
        from solfege.value.note.set.note_list import ChromaticNoteList
        return ChromaticNoteList

    @staticmethod
    def interval_repr(interval: ChromaticInterval) -> str:
        "How to display the interval in make."
        return str(interval.value)