

from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.pattern_with_interval_list import PatternType
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from utils.recordable import ChromaticRecordedContainerType, RecordKeeper
from utils.util import assert_dict_typing, assert_typing, assert_iterable_typing


@dataclass(frozen=True)
class ChromaticIntervalListToPatterns(RecordKeeper[ChromaticIntervalListPattern, PatternType, List[PatternType]], Generic[PatternType, ChromaticRecordedContainerType]):
    """Allows to associate a ChromaticIntervalList to `PatternType` saved in a list.
    
    This is usually associated to a IntervalListToPattern with the same content.
    """


    """Same as RecordedType"""
    _recorded_type: ClassVar[Type]
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIntervalListPattern
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticRecordedContainerType

    def get_easiest_pattern_from_chromatic_interval(self, chromatic_interval_list: ChromaticIntervalListPattern) -> Optional[PatternType]:
        """Given a set of interval, return the object having this set of intervals."""
        assert_typing(chromatic_interval_list, ChromaticIntervalListPattern, exact=True)
        patterns = self.get_recorded_container(chromatic_interval_list)
        if patterns:
            return min(patterns)
        return None