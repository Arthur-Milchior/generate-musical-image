
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern.pattern_with_interval_list import PatternType
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalListType, NoteListType
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.interval_list import IntervalList
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.frozenlist import FrozenList
from utils.util import assert_typing


class AbstractPairInstantiation(AbstractPatternInstantiation[PatternType, Note, Interval, NoteFrozenList, IntervalList], Generic[PatternType]):
    note_type: ClassVar[AbstractNote] = Note
    interval_type: ClassVar[AbstractInterval] = Interval
    interval_list_type: ClassVar[FrozenList[IntervalType]] = IntervalList
    note_list_type: ClassVar[FrozenList[NoteType]] = NoteFrozenList

    def get_intervals(self) -> IntervalList:
        return self.pattern.get_interval_list()