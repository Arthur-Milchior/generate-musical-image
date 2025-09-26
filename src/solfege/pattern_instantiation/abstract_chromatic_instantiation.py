
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.set.interval_list_pattern import AbstractIntervalListPattern, ChromaticIntervalListPattern
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.easyness import KeyType
from utils.frozenlist import FrozenList
from utils.util import T, assert_typing


@dataclass(frozen=True, eq=True)
class AbstractChromaticInstantiation(AbstractPatternInstantiation[T, ChromaticNote, ChromaticInterval, KeyType], Generic[T, KeyType]):
    note_type: ClassVar[AbstractNote] = ChromaticNote
    interval_type: ClassVar[AbstractInterval] = ChromaticInterval
    interval_list_type: ClassVar[FrozenList[IntervalType]] = ChromaticIntervalListPattern
    note_list_type: ClassVar[FrozenList[NoteType]] = ChromaticNoteList


    def get_intervals(self) -> AbstractIntervalListPattern[ChromaticInterval]:
        return self.pattern.get_interval_list().get_chromatic_interval_list()