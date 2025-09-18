
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, List, Type, TypeVar
from solfege.pattern.inversion.abstract_identical_inversion_patterns import AbstractIdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote
from utils.easyness import ClassWithEasyness


class MinimalChordDecompositionInput(ClassWithEasyness, ABC):
    @abstractmethod
    def get_tonic_minus_lowest_note(self) -> ChromaticInterval:
        return NotImplemented

    def get_tonic(self, lowest_note) -> ChromaticInterval:
        return lowest_note - self.get_tonic_minus_lowest_note()
    
    @abstractmethod
    def notations(self) -> List[str]:
        return NotImplemented
    
    @abstractmethod
    def get_inversion_patterns(self) -> List[InversionPattern]:
        return NotImplemented

class ChromaticIdenticalInversionPatternGetter(ABC):
    @abstractmethod
    def get_identical_inversion_pattern(self) -> "IdenticalInversionPattern":
        return NotImplemented
    
ChromaticIdenticalInversionPatternGetterType = TypeVar("ChromaticIdenticalInversionPatternGetterType", bound=ChromaticIdenticalInversionPatternGetter)

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIdenticalInversionPatterns(AbstractIdenticalInversionPatterns[ChromaticIntervalListPattern], MinimalChordDecompositionInput):
    """A chromatic interval list and all chord inversion associated to it.
    
    It is the data entry for ChromaticIntervalListToInversion
    """
    interval_list_type: ClassVar[Type] = ChromaticIntervalListPattern

    def get_identical_inversion_pattern(self):
        return self

    @classmethod
    def get_interval_list_from_inversion(cls, inversion: InversionPattern):
        return inversion.get_interval_list().get_chromatic_interval_list()
    
    #pragma mark - MinimalChordDecompositionInput

    def get_tonic_minus_lowest_note(self) -> ChromaticInterval:
        return self.inversion_patterns[0].tonic_minus_lowest_note
    
    def notations(self) -> List[str]:
        return [inversion_pattern.notation() for inversion_pattern in self.inversion_patterns]
    
    def get_inversion_patterns(self) -> List[InversionPattern]:
        return self.inversion_patterns