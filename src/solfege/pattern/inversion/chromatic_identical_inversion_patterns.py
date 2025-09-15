
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, List, Type, TypeVar
from solfege.pattern.inversion.abstract_identical_inversion_patterns import AbstractIdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern

class ChromaticIdenticalInversionPatternGetter(ABC):
    @abstractmethod
    def get_identical_inversion_pattern(self) -> "IdenticalInversionPattern":
        return NotImplemented
    
ChromaticIdenticalInversionPatternGetterType = TypeVar("ChromaticIdenticalInversionPatternGetterType", bound=ChromaticIdenticalInversionPatternGetter)

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIdenticalInversionPatterns(AbstractIdenticalInversionPatterns[ChromaticIntervalListPattern]):
    """A chromatic interval list and all chord inversion associated to it.
    
    It is the data entry for ChromaticIntervalListToInversion
    """
    interval_list_type: ClassVar[Type] = ChromaticIntervalListPattern

    def get_identical_inversion_pattern(self):
        return self

    @classmethod
    def get_interval_list_from_inversion(cls, inversion: InversionPattern):
        return inversion.get_interval_list().get_chromatic_interval_list()