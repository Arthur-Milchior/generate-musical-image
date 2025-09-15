
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns, IdenticalInversionPatternsGetterType
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern_instantiation.inversion.identical_inversions import IdenticalInversion
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType


@dataclass(frozen=True)
class AbstractIdenticalInversion(AbstractPatternInstantiation[IdenticalInversionPatterns, NoteType, IntervalType],  IdenticalInversionPatternsGetterType, Generic[NoteType, IntervalType]): 
    pattern_type: ClassVar[PatternWithIntervalList] = IdenticalInversionPatterns

    @abstractmethod
    def get_identical_inversion_pattern(self) -> IdenticalInversionPatterns:
        return self.pattern
    
AbstractIdenticalInversionType = TypeVar("AbstractIdenticalInversionType", bound=AbstractIdenticalInversion)