
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Generator, Generic, List, Tuple, Type

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.set.abstract_interval_ilst_pattern import AbstractIntervalListPattern, IntervalListPatternType
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness
from utils.recordable import RecordedContainer
from utils.util import assert_iterable_typing, assert_typing


@dataclass(frozen=True, unsafe_hash=True)
class AbstractIdenticalInversionPatterns(RecordedContainer[InversionPattern], 
                                 DataClassWithDefaultArgument, ClassWithEasyness[Tuple[int, int]],
                                 ABC, Generic[IntervalListPatternType]):
    """A (chromatic) interval list and all chord inversion associated to it.
    """

    #must be implemented by subclasses

    "Same as IntervalListPatternType"
    interval_list_type: ClassVar[Type]

    #public
    intervals: AbstractIntervalListPattern[IntervalType]
    inversion_patterns: List[InversionPattern] = field(default_factory=list, hash=False)

    def __len__(self):
        return len(self.inversion_patterns)

    def append(self, inversion: InversionPattern):
        expected = self.intervals
        actuals = self.get_interval_list_from_inversion(inversion)
        assert expected == actuals, f"{expected} != {actuals}"
        self.inversion_patterns.append(inversion)
        self.inversion_patterns.sort(key = lambda inversion_pattern: inversion_pattern.easy_key())

    def easiest_inversion(self):
        return min(self.inversion_patterns)
    
    def easiest_name(self):
        return self.easiest_inversion().name()
    
    def alternative_names(self):
        return ",".join(inversion.name() for inversion in self.inversion_patterns[1:])
    
    def __iter__(self):
        return iter(self.inversion_patterns)
    
    # Must be implemented by subclasses
    @classmethod
    @abstractmethod
    def get_interval_list_from_inversion(cls, inversion: InversionPattern):...    
    #pragma mark - ClassWithEasyness

    def easy_key(self) -> Tuple[int, int]:
        return self.inversion_patterns[0].easy_key()
    
    # pragma mark - DataClassWithDefaultArgument
    def __post_init__(self):
        assert_typing(self.intervals, self.interval_list_type)
        assert_iterable_typing(self.inversion_patterns, InversionPattern)
        super().__post_init__()
