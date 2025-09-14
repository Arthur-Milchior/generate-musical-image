from dataclasses import dataclass
from typing import Dict, List

from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern.pattern_with_name import PatternWithName
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import DataClassWithDefaultArgument, IntervalListPattern
from utils.util import assert_typing
from solfege.value.key.keys import nor_flat_nor_sharp


@dataclass(frozen=True)
class SolfegePattern(IntervalListPattern, PatternWithName, PatternWithIntervalList, DataClassWithDefaultArgument):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """The interval between the signature for this scale and the signature for the major scale with the same key.
    E.g. for minor, use three_flats"""
    interval_for_signature: Interval

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["interval_for_signature"] = nor_flat_nor_sharp
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "interval_for_signature")
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        assert_typing(self.interval_for_signature, Interval)
        super().__post_init__()