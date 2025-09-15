
from dataclasses import dataclass
from typing import ClassVar, Generic

from solfege.pattern.inversion.identical_inversion_patterns import IdentiticalInversionPatterns
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType


@dataclass(frozen=True)
class AbstractIdenticalInversion(AbstractPatternInstantiation[IdentiticalInversionPatterns, NoteType, IntervalType],  Generic[NoteType, IntervalType]): 
    pattern_type: ClassVar[PatternWithIntervalList] = IdentiticalInversionPatterns
