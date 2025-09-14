
from dataclasses import dataclass
from typing import Callable, ClassVar, Generic, Type, TypeVar

from solfege.pattern.inversion.inversion_pattern import InversionPattern, InversionPatternGetter
from solfege.pattern.pattern_with_interval_list import PatternType
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.interval_list_pattern import AbstractIntervalListPattern, IntervalListPattern
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note, NoteFrozenList
from utils.frozenlist import FrozenList
from utils.util import assert_typing


class AbstractPairInstantiation(InversionPatternGetter, AbstractPatternInstantiation[PatternType, Note, Interval], Generic[PatternType]):
    note_type: ClassVar[AbstractNote] = Note
    interval_type: ClassVar[AbstractInterval] = Interval
    interval_list_type: ClassVar[FrozenList[IntervalType]] = IntervalListPattern
    note_list_type: ClassVar[FrozenList[NoteType]] = NoteFrozenList
    chromatic_instantiation_type: ClassVar[Type[AbstractChromaticInstantiation]]

    related_chromatic_type: ClassVar[AbstractChromaticInstantiation[PatternType]]

    def get_intervals(self) -> AbstractIntervalListPattern[Interval]:
        return self.pattern.get_interval_list()
    
    def get_chromatic_instantiation(self) -> AbstractChromaticInstantiation[PatternType]:
        # Note that for c4-flat, and c4-double flat, `self` is in base octave but the returned value is not.
        return self.chromatic_instantiation_type(self.pattern, self.lowest_note.get_chromatic())

    def get_inversion_pattern(self) -> InversionPattern:
        return self.pattern