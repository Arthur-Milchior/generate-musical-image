from typing import Tuple
import unittest

from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalListFrozenList
from utils.frozenlist import FrozenList

from solfege.pattern.interval_list_to_patterns import *

second_major = IntervalList.make_relative([(2, 1)])
tone = ChromaticIntervalList.make_relative([2])

@dataclass(frozen=True, eq = True)
class FakePattern(PatternWithIntervalList["FakeIntervalListToFakePatterns"]):
    _relative_intervals: IntervalListFrozenList

    @classmethod
    def _new_record_keeper(cls):
        return FakeIntervalListToFakePatterns.make()

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_intervals(intervals):
            return IntervalFrozenList([Interval.make_single_argument(interval) for interval in intervals])
        
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_relative_intervals", clean_intervals)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def get_interval_list(self) -> IntervalList:
        return IntervalList.make_relative(self._relative_intervals)
    
class FakeChromaticIntervalListToFakePatterns(ChromaticIntervalListToPatterns[FakePattern, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = FakePattern
    _recorded_container_type: ClassVar[Type] = list
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[FakePattern]:
        return list()

class FakeIntervalListToFakePatterns(IntervalListToPatterns[FakePattern, List, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = FakePattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = list
    
    @classmethod
    def make_chromatic_container(self):
        return FakeChromaticIntervalListToFakePatterns.make()
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[FakePattern]:
        return list()

    
fake_pattern_second_major = FakePattern.make([(2,1)])
fake_pattern_third_major = FakePattern.make([(4,2)])

class TestIntervalToPattern(unittest.TestCase):
    def test_add_retrieve(self):
        itp = FakeIntervalListToFakePatterns.make()
        itp.register(second_major, fake_pattern_second_major)
        self.assertEqual([fake_pattern_second_major], itp.get_from_chromatic_interval_list(tone))
        self.assertEqual([fake_pattern_second_major], itp.get_from_interval_list(second_major))
        self.assertEqual(fake_pattern_second_major, itp.get_easiest_pattern_from_chromatic_interval(tone))
