from typing import Tuple
import unittest

from solfege.value.interval.interval import Interval
from utils.frozenlist import FrozenList

from solfege.pattern.interval_to_pattern import *

second_major = IntervalList.make_relative([(2, 1)])
tone = ChromaticIntervalList.make_relative([2])

@dataclass(frozen=True, eq = True)
class FakePattern(PatternWithIntervalList):
    _relative_intervals: FrozenList[IntervalList]

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_intervals(intervals):
            return FrozenList([Interval.make_single_argument(interval) for interval in intervals])
        
        args, kwargs = cls.maybe_arg_to_kwargs(args, kwargs, "_relative_intervals", clean_intervals)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def get_interval_list(self) -> IntervalList:
        return IntervalList.make_relative(self._relative_intervals)
    
fake_pattern_second_major = FakePattern.make([(2,1)])
fake_pattern_third_major = FakePattern.make([(4,2)])

class TestIntervalToPattern(unittest.TestCase):
    def test_add_retrieve(self):
        itp = IntervalToPattern(FakePattern)
        itp.register(fake_pattern_second_major,  itp.get_easiest_pattern_from_chromatic_interval(tone))
        self.assertEqual([fake_pattern_second_major], itp.get_patterns_from_chromatic_interval(tone))
        self.assertEqual([fake_pattern_second_major], itp.get_patterns_from_interval(second_major))
        self.assertEqual(fake_pattern_second_major, itp.get_easiest_pattern_from_chromatic_interval(tone))
