from dataclasses import dataclass, field
import sys
from typing import ClassVar, Dict, List, Optional, Self, Type, Union

from solfege.value.interval.set.list import ChromaticIntervalList, DataClassWithDefaultArgument, IntervalList
from utils.util import assert_list_typing, assert_typing
from solfege.value.key.key import nor_flat_nor_sharp



@dataclass(frozen=True)
class PatternWithIntervalList(DataClassWithDefaultArgument):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """Associate a interval list to its patterns"""

    """Whether to record this pattern in the list of patterns."""
    record: bool = field(compare=False)
    _interval_to_patterns: ClassVar["IntervalToPattern"]

    @classmethod
    def interval_to_patterns(cls) -> Type["IntervalToPattern"]:
        try:
            interval_to_patterns = cls._interval_to_patterns
        except:
            from solfege.pattern.interval_to_pattern import IntervalToPattern
            interval_to_patterns = cls._interval_to_patterns = IntervalToPattern[Self](cls)
        return interval_to_patterns

    @classmethod
    def _default_arguments_for_constructor(cls):
        defaut_dict = super()._default_arguments_for_constructor()
        defaut_dict["record"] = True
        return defaut_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.maybe_arg_to_kwargs(args, kwargs, "record")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.record, bool)
        super().__post_init__()
        if self.record:
            self._associate_intervals_to_self()

    def _associate_intervals_to_self(self,
                                     interval_lists: Optional[Union[List[IntervalList], IntervalList]] = None,
                                     interval_to_pattern: Optional["IntervalToPattern"]=None):
        from solfege.pattern.interval_to_pattern import IntervalToPattern
        interval_to_pattern_: IntervalToPattern
        if interval_to_pattern is None:
            interval_to_pattern_ = self.interval_to_patterns()
        else:
            interval_to_pattern_ = interval_to_pattern
        assert_typing(interval_to_pattern_, IntervalToPattern)
        if interval_lists is None:
            interval_lists = self.interval_lists()
        if isinstance(interval_lists, IntervalList):
            interval_lists = [interval_lists]
        assert_list_typing(interval_lists, IntervalList)
        for interval_list in interval_lists:
            assert_typing(interval_list, IntervalList)
            interval_to_pattern_.register(self, interval_list=interval_list)
    
    def get_interval_list(self) -> IntervalList:
        return NotImplemented

    def interval_lists(self) -> List[IntervalList]:
        return [self.get_interval_list()]
    
    def chromatic_interval_lists(self) -> ChromaticIntervalList:
        return [interval.get_chromatic() for interval in self.interval_lists()]