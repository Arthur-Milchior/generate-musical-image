from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Generic, Self, TypeVar
from solfege.list_order import ListOrder
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.set.abstract_interval_ilst_pattern import AbstractIntervalListPattern
from solfege.value.key.key import Key
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.set.abstract_note_list import AbstractNoteList
from solfege.value.note.set.note_list import NoteList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import KeyType
from utils.frozenlist import FrozenList
from solfege.pattern.pattern_with_interval_list import PatternType, PatternWithIntervalList
from utils.util import T, assert_typing


NoteFrozenListType= TypeVar("NoteFrozenListType", bound = FrozenList)
IntervalFrozenListType= TypeVar("IntervalFrozenListType", bound = FrozenList)

@dataclass(frozen=True, eq=True)
class AbstractPatternInstantiation(DataClassWithDefaultArgument, ABC, Generic[PatternType, NoteType, IntervalType, KeyType]):
    pattern: PatternType
    lowest_note: NoteType

    pattern_type: ClassVar[PatternWithIntervalList]
    note_type: ClassVar[AbstractNote]
    interval_type: ClassVar[AbstractInterval]
    interval_list_type: ClassVar[FrozenList[IntervalType]]
    note_list_type: ClassVar[AbstractNoteList[NoteType, IntervalType, PatternWithIntervalList]]

    def __post_init__(self):
        assert_typing(self.lowest_note, self.note_type)
        assert_typing(self.pattern, self.pattern_type)
        assert self.lowest_note.is_in_base_octave(accepting_octave=False)
        super().__post_init__()

    def get_absolute_intervals(self) -> FrozenList[IntervalType]:
        return self.get_intervals().absolute_intervals()
    
    def get_notes(self) -> AbstractNoteList[NoteType, IntervalType, PatternWithIntervalList]:
        l =  []
        for interval in self.get_absolute_intervals():
            l.append(self.lowest_note + interval)
        return self.note_list_type.make(l, list_order=ListOrder.INCREASING)

    def key(self)->Key:
        """The key. Assuming notes are not diatonic"""
        return Key.from_note(self.lowest_note + self.pattern.interval_for_signature)

    def all_blacks(self):
        """Whether all notes are black on a piano. assert if note is diatonic."""
        return all(note.is_black_key_on_piano() for note in self.get_notes())
    
    def add_octave(self, nb_octave: int) -> Self:
        return dataclasses.replace(self, lowest_note= self.lowest_note.add_octave(nb_octave))
    
    # must be implemented by subclasses

    @abstractmethod
    def get_intervals(self) -> AbstractIntervalListPattern[IntervalType]:...

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> KeyType:
        # Defined only if the pattern defines it.
        return self.pattern.easy_key()