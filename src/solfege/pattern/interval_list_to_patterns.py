
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns, PatternType
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.value.interval.set.list import ChromaticIntervalList, IntervalList
from utils.recordable import RecordKeeper
from utils.util import assert_dict_typing, assert_typing, assert_list_typing


@dataclass(frozen=True)
class IntervalListToPatterns(RecordKeeper[IntervalList, PatternType, List[PatternType]], Generic[PatternType]):
    """Same but for chromatic interval as key"""
    chromatic: ChromaticIntervalListToPatterns[PatternType]
    """Same as KeyType"""
    _key_type: ClassVar[Type] = IntervalList
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type]
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = List


    @classmethod
    def _default_arguments_for_constructor(cls):
        kwargs = super()._default_arguments_for_constructor()
        kwargs["chromatic"] = cls.make_chromatic_container()
        return kwargs
    
    @classmethod
    def make_chromatic_container(self):
        return NotImplemented

    def __post_init__(self):
        assert_typing(self.chromatic, ChromaticIntervalListToPatterns)

    def get_easiest_pattern_from_chromatic_interval(self, chromatic_interval_list: ChromaticIntervalList):
        return self.chromatic.get_easiest_pattern_from_chromatic_interval(chromatic_interval_list)
    
    def register(self, key: IntervalList, recorded: PatternType):
        super().register(key, recorded)
        self.chromatic.register(key.get_chromatic(), recorded)

    def get_from_interval_list(self, key: IntervalList):
        return self.get_recorded_container(key)

    def get_from_chromatic_interval_list(self, key: ChromaticIntervalList):
        return self.chromatic.get_recorded_container(key)


PatternWithIntervalList._record_keeper_type = IntervalListToPatterns