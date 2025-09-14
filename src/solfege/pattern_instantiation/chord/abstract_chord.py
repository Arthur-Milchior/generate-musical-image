
from dataclasses import dataclass
from typing import ClassVar, Generic

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalListType, NoteListType
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType


@dataclass(frozen=True)
class AbstractChord(AbstractPatternInstantiation[ChordPattern, NoteType, IntervalType, NoteListType, IntervalListType],  Generic[NoteType, IntervalType, NoteListType, IntervalListType]): 
    pattern_type: ClassVar[PatternWithIntervalList] = ChordPattern
