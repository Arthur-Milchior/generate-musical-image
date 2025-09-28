
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns, PatternType
from solfege.pattern.pattern_with_interval_lists import PatternWithIntervalLists
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.recording.record_keeper import RecordKeeper
from utils.recording.recorded_container import ChromaticRecordedContainerType, RecordedContainerType
from utils.recording.singleton_container import SingletonContainer
from utils.util import assert_dict_typing, assert_optional_typing, assert_typing, assert_iterable_typing


@dataclass(frozen=True)
class IntervalListToPattern(RecordKeeper[IntervalList, PatternType, SingletonContainer[PatternType]], ABC, Generic[PatternType]):
    """Associate a Interval list to a list of PatternType stored in RecordedContainerType.

    Registering in this record keeper also register to the associated record keeper with interval keys.
    """


    """Same but for chromatic interval as key"""
    chromatic: ChromaticIntervalListToPatterns[PatternType]

    #Must be implemented by subclasses
    """Same as KeyType"""
    _key_type: ClassVar[Type] = IntervalList
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type]

    _recorded_container_type: ClassVar[Type] = SingletonContainer

    @classmethod
    @abstractmethod
    def make_chromatic_record_keeper(self) -> ChromaticIntervalListToPatterns[PatternType]:...    
    #public

    def get_easiest_pattern_from_chromatic_interval(self, chromatic_interval_list: ChromaticIntervalListPattern):
        return self.chromatic.get_pattern_from_chromatic_interval(chromatic_interval_list)
    
    def register(self, key: IntervalList, recorded: PatternType):
        super().register(key, recorded)
        self.chromatic.register(key.get_chromatic_interval_list(), recorded)

    def get_from_interval_list(self, key: IntervalList) -> Optional[RecordedContainerType]:
        container = self.get_recorded_container(key)
        assert_optional_typing(container, self._recorded_container_type)
        return container

    def get_from_chromatic_interval_list(self, key: ChromaticIntervalListPattern) -> Optional[ChromaticRecordedContainerType]:
        assert_typing(key, ChromaticIntervalListPattern)
        container = self.chromatic.get_recorded_container(key)
        assert_optional_typing(container, SingletonContainer)
        return container
    
    #pragma mark - DataClassWithDefaultArgument
    
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        chromatic = cls.make_chromatic_record_keeper()
        assert_typing(chromatic, ChromaticIntervalListToPatterns)
        default["chromatic"] = chromatic
        return default

    def __post_init__(self):
        assert_typing(self.chromatic, ChromaticIntervalListToPatterns)
        super().__post_init__()


PatternWithIntervalLists._record_keeper_type = IntervalListToPattern