
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns, PatternType
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList
from utils.recordable import ChromaticRecordedContainerType, RecordKeeper, RecordedContainerType
from utils.util import assert_dict_typing, assert_optional_typing, assert_typing, assert_iterable_typing


@dataclass(frozen=True)
class IntervalListToPatterns(RecordKeeper[IntervalList, PatternType, RecordedContainerType], Generic[PatternType, RecordedContainerType, ChromaticRecordedContainerType]):
    """Associate a Interval list to a list of PatternType stored in RecordedContainerType.

    Registering in this record keeper also register to the associated record keeper with interval keys.
    """


    """Same but for chromatic interval as key"""
    chromatic: ChromaticIntervalListToPatterns[PatternType, ChromaticRecordedContainerType]
    """Same as KeyType"""
    _key_type: ClassVar[Type] = IntervalList
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type]
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type]
    _chromatic_recorded_container_type: ClassVar[Type]

    def is_key_valid(self, key: IntervalList):
        return NotImplemented
    
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["chromatic"] = cls.make_chromatic_container()
        return default
    
    @classmethod
    def make_chromatic_container(self) -> ChromaticIntervalListToPatterns[PatternType, ChromaticRecordedContainerType]:
        return NotImplemented

    def __post_init__(self):
        assert_typing(self.chromatic, ChromaticIntervalListToPatterns)

    def get_easiest_pattern_from_chromatic_interval(self, chromatic_interval_list: ChromaticIntervalList):
        return self.chromatic.get_easiest_pattern_from_chromatic_interval(chromatic_interval_list)
    
    def register(self, key: IntervalList, recorded: PatternType):
        super().register(key, recorded)
        self.chromatic.register(key.get_chromatic_interval_list(), recorded)

    def get_from_interval_list(self, key: IntervalList) -> Optional[RecordedContainerType]:
        container = self.get_recorded_container(key)
        assert_optional_typing(container, self._recorded_container_type)
        return container

    def get_from_chromatic_interval_list(self, key: ChromaticIntervalList) -> Optional[ChromaticRecordedContainerType]:
        assert_typing(key, ChromaticIntervalList)
        container = self.chromatic.get_recorded_container(key)
        assert_optional_typing(container, self._chromatic_recorded_container_type)
        return container


PatternWithIntervalList._record_keeper_type = IntervalListToPatterns