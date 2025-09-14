
from dataclasses import dataclass
from typing import ClassVar, Generic

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType


@dataclass(frozen=True)
class AbstractInversion(AbstractPatternInstantiation[ChordPattern, NoteType, IntervalType],  Generic[NoteType, IntervalType]): 
    pattern_type: ClassVar[PatternWithIntervalList] = InversionPattern
