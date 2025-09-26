
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, Tuple, TypeVar

from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatterns
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns, IdenticalInversionPatternsGetter
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType


@dataclass(frozen=True)
class AbstractIdenticalInversion(AbstractPatternInstantiation[IdenticalInversionPatterns, NoteType, IntervalType, Tuple[int, int]],  IdenticalInversionPatternsGetter, Generic[NoteType, IntervalType]):
    """
    A pair where the pattern is a set of equivalent inversion
    """

    pattern_type: ClassVar[PatternWithIntervalList] = ChromaticIdenticalInversionPatterns

    def get_identical_inversion_pattern(self) -> ChromaticIdenticalInversionPatterns:
        return self.pattern
    
AbstractIdenticalInversionType = TypeVar("AbstractIdenticalInversionType", bound=AbstractIdenticalInversion)