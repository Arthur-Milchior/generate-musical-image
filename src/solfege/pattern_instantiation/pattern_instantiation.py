from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.note.abstract_note import AbstractNote, NoteType
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from solfege.pattern.pattern_with_interval_list import PatternType, PatternWithIntervalList
from utils.util import T, assert_typing


NoteFrozenListType= TypeVar("NoteFrozenListType", bound = FrozenList)
IntervalFrozenListType= TypeVar("IntervalFrozenListType", bound = FrozenList)

@dataclass(frozen=True, eq=True)
class AbstractPatternInstantiation(DataClassWithDefaultArgument, ABC, Generic[PatternType, NoteType, IntervalType]):
    pattern: PatternType
    lowest_note: NoteType

    pattern_type: ClassVar[PatternWithIntervalList]
    note_type: ClassVar[AbstractNote]
    interval_type: ClassVar[AbstractInterval]
    interval_list_type: ClassVar[FrozenList[IntervalType]]
    note_list_type: ClassVar[FrozenList[NoteType]]

    def __post_init__(self):
        assert_typing(self.lowest_note, self.note_type)
        assert_typing(self.pattern, self.pattern_type)
        assert self.lowest_note.is_in_base_octave(accepting_octave=False)
        super().__post_init__()

    @abstractmethod
    def get_intervals(self) -> IntervalFrozenListType:
        return NotImplemented

    def get_absolute_intervals(self) -> FrozenList[IntervalType]:
        return self.get_intervals().absolute_intervals()
    
    def get_notes(self) -> NoteFrozenListType:
        l =  []
        for interval in self.get_absolute_intervals():
            l.append(self.lowest_note + interval)
        return self.note_list_type(l)