
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional, Type, TypeVar

from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern.pattern_with_interval_list_list import PatternWithIntervalListList
from solfege.value.interval.set.list import ChromaticIntervalList, IntervalList
from utils.util import assert_dict_typing, assert_typing, assert_list_typing


PatternType = TypeVar("PatternType", bound=PatternWithIntervalList)

@dataclass
class IntervalToPattern(Generic[PatternType]):
    _pattern_type: Type
    _pattern_with_interval_type: Type = list
    _pattern_with_chromatic_interval_type: Type = list
    _interval_to_patterns: Dict[IntervalList, PatternType] = field(default_factory=dict)
    _chromatic_interval_to_patterns: Dict[ChromaticIntervalList, PatternType] = field(default_factory=dict)

    def __post__init__(self):
        assert_typing(self._pattern_type, type)
        assert_typing(self._pattern_with_chromatic_interval_type, type)
        assert_typing(self._pattern_with_interval_type, type)
    
    def newPatternWithIntervalListList(self) -> PatternWithIntervalListList:
        return list()
    
    def newPatternWithChromaticIntervalListList(self) -> PatternWithIntervalListList:
        return list()
    
    def register(self, pattern: PatternType, interval_list: IntervalList):
        assert_typing(pattern, self._pattern_type, exact=True)
        intervals = interval_list if interval_list is not None else pattern.get_interval_list()
        assert_typing(intervals, IntervalList, exact=True)
        if intervals not in self._interval_to_patterns:
            self._interval_to_patterns[intervals] = self.newPatternWithIntervalListList()
        self._interval_to_patterns[intervals].append(pattern)

        chromatic_intervals = intervals.get_chromatic()
        assert_typing(chromatic_intervals, ChromaticIntervalList, exact=True)
        if chromatic_intervals not in self._chromatic_interval_to_patterns:
            self._chromatic_interval_to_patterns[chromatic_intervals] = self.newPatternWithChromaticIntervalListList()
        self._chromatic_interval_to_patterns[chromatic_intervals].append(pattern)

    def get_patterns_from_interval(self, intervals: IntervalList) -> PatternWithIntervalListList:
        """Given a set of interval, return the object having this set of intervals."""
        assert_typing(intervals, IntervalList, exact=True)
        assert_dict_typing(self._interval_to_patterns, IntervalList, self._pattern_with_interval_type)
        if intervals in self._interval_to_patterns:
            pattern = self._interval_to_patterns[intervals]
            assert_list_typing(pattern, self._pattern_type)
            return pattern
        return self.newPatternWithIntervalListList()

    def get_patterns_from_chromatic_interval(self, chromatic_intervals: ChromaticIntervalList) -> PatternWithIntervalListList:
        """Given a set of interval, return the object having this set of intervals."""
        assert_typing(chromatic_intervals, ChromaticIntervalList, exact=True)
        assert_dict_typing(self._chromatic_interval_to_patterns, ChromaticIntervalList, self._pattern_with_chromatic_interval_type)
        if chromatic_intervals in self._chromatic_interval_to_patterns:
            pattern = self._chromatic_interval_to_patterns[chromatic_intervals]
            assert_list_typing(pattern, self._pattern_type)
            return pattern
        return self.newPatternWithChromaticIntervalListList()    
    
    def get_easiest_pattern_from_chromatic_interval(self, chromatic_intervals: ChromaticIntervalList) -> Optional[PatternType]:
        """Given a set of interval, return the object having this set of intervals."""
        assert_typing(chromatic_intervals, ChromaticIntervalList, exact=True)
        patterns = self.get_patterns_from_chromatic_interval(chromatic_intervals)
        if patterns:
            return min (patterns)
        return None