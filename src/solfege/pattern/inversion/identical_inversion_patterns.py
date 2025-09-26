
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, List, Type, TypeVar
from solfege.pattern.inversion.abstract_identical_inversion_patterns import AbstractIdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from utils.easyness import ClassWithEasyness
from utils.util import assert_iterable_typing, assert_typing



class IdenticalInversionPatternsGetter(ClassWithEasyness, ABC):
    @abstractmethod
    def get_identical_inversion_pattern(self) -> "IdenticalInversionPatterns":...    
IdenticalInversionPatternsGetterType = TypeVar("IdenticalInversionPatternGetterType", bound=IdenticalInversionPatternsGetter)

@dataclass(frozen=True, unsafe_hash=True)
class IdenticalInversionPatterns(AbstractIdenticalInversionPatterns[IntervalListPattern], IdenticalInversionPatternsGetter):
    """A interval list and all chord inversion associated to it.
    """
    interval_list_type: ClassVar[Type] = IntervalListPattern

    @classmethod
    def get_interval_list_from_inversion(cls, inversion: InversionPattern):
        return inversion.get_interval_list()
    
    #pragma mark - IdenticalInversionPatternsGetter

    def get_identical_inversion_pattern(self):
        return self