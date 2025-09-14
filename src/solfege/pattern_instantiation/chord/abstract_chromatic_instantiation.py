
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern.pattern_with_interval_list import PatternType
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalListType, NoteListType
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from utils.frozenlist import FrozenList
from utils.util import assert_typing


class AbstractChromaticInstantiation(AbstractPatternInstantiation[PatternType, ChromaticNote, ChromaticInterval, ChromaticNoteFrozenList, ChromaticIntervalList], Generic[PatternType]):
    note_type: ClassVar[AbstractNote] = ChromaticNote
    interval_type: ClassVar[AbstractInterval] = ChromaticInterval
    interval_list_type: ClassVar[FrozenList[IntervalType]] = ChromaticIntervalList
    note_list_type: ClassVar[FrozenList[NoteType]] = ChromaticNoteFrozenList


    def get_intervals(self) -> ChromaticIntervalList:
        return self.pattern.get_interval_list().get_chromatic_interval_list()