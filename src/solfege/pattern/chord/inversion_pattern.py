

from dataclasses import dataclass
from typing import ClassVar, Dict, List
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import DataClassWithDefaultArgument, IntervalList
from utils.util import assert_typing


@dataclass(frozen=True)
class InversionPattern(PatternWithIntervalList["IntervalListToInversion"], DataClassWithDefaultArgument):
    """Order is considering not inversion first. Then with fifth. Then base."""
    inversion: int
    interval_list: IntervalList
    base: ChordPattern
    fifth_omitted: bool

    """For a scale whose lowest note is n, you get the position of the tonic with n+position_of_lowest_interval_in_base_octave."""
    position_of_lowest_interval_in_base_octave: Interval

    @classmethod
    def _new_record_keeper(cls):
        from solfege.pattern.chord.interval_list_to_inversion_pattern import IntervalListToInversionPattern
        return IntervalListToInversionPattern.make()

    @classmethod
    def _default_arguments_for_constructor(cls):
        default_dict = super()._default_arguments_for_constructor()
        default_dict["fifth_omitted"] = False
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        cls.arg_to_kwargs(args, kwargs, "inversion")
        def clean_absolute_intervals(intervals):
            if not isinstance(intervals, IntervalList):
                return IntervalList.make_absolute(intervals)
            return intervals
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "interval_list", clean_absolute_intervals)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "base")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "fifth_omitted")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def newPatternWithChromaticIntervalList(self):
        from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
        return ChromaticIntervalListAndItsInversions(self.interval_list.get_chromatic_interval_list())
    
    def get_interval_list(self) -> IntervalList:
        iv = self.interval_list
        assert_typing(iv, IntervalList, exact=True)
        return iv
    
    def name(self):
        if self.inversion == 0:
            suffix = ""
        elif self.inversion == 1:
            suffix = " first inversion"
        elif self.inversion == 2:
            suffix = " second inversion"
        elif self.inversion == 3:
            suffix = " third inversion"
        else:
            assert self.inversion < 10
            suffix = f" {self.inversion}th inversion"
        return f"""{self.base.first_of_the_names()}{suffix}"""
    
    def __lt__(self, other: "InversionPattern"):
        return (self.inversion, not self.fifth_omitted, self.base) < (other.inversion, not other.fifth_omitted, other.base)
    