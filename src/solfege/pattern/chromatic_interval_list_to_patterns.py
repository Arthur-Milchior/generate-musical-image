

from dataclasses import dataclass, field
from re import Pattern
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.pattern_with_interval_lists import PatternType
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern
from utils.recording.record_keeper import RecordKeeper
from utils.recording.recorded_container import ChromaticRecordedContainerType
from utils.recording.singleton_container import SingletonContainer
from utils.util import assert_dict_typing, assert_typing, assert_iterable_typing


@dataclass(frozen=True)
class ChromaticIntervalListToPatterns(RecordKeeper[ChromaticIntervalListPattern, PatternType, SingletonContainer[PatternType]], Generic[PatternType]):
    """Allows to associate a ChromaticIntervalList to `PatternType` saved in a list.
    
    This is usually associated to a IntervalListToPattern with the same content.
    """


    """Same as RecordedType"""
    _recorded_type: ClassVar[Type]
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIntervalListPattern
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = SingletonContainer
    

    def get_pattern_from_chromatic_interval(self, chromatic_interval_list: ChromaticIntervalListPattern) -> Optional[PatternType]:
        """Given a set of interval, return the object having this set of intervals."""
        assert_typing(chromatic_interval_list, ChromaticIntervalListPattern, exact=True)
        return self.get_recorded_container(chromatic_interval_list).recorded_value
