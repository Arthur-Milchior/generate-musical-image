from dataclasses import dataclass, field
import sys
from typing import ClassVar, Dict, Generic, List, Optional, Self, Type, TypeVar, Union

from solfege.value.interval.set.interval_list import ChromaticIntervalList, DataClassWithDefaultArgument, IntervalList
from utils.recordable import RecordKeeperType, Recordable
from utils.util import assert_iterable_typing, assert_typing
from solfege.value.key.key import nor_flat_nor_sharp



@dataclass(frozen=True)
class PatternWithIntervalList(Recordable[IntervalList, RecordKeeperType], Generic[RecordKeeperType], DataClassWithDefaultArgument):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """Associate a interval list to its patterns"""

    """Whether to record this pattern in the list of patterns."""
    _record_keeper: ClassVar[RecordKeeperType]
    _record_keeper_type: ClassVar[Type]
    _key_type: ClassVar[Type] = IntervalList

    @classmethod
    def _default_arguments_for_constructor(cls):
        defaut_dict = super()._default_arguments_for_constructor()
        defaut_dict["record"] = True
        return defaut_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "record")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.record, bool)
        super().__post_init__()
        if self.record:
            self._associate_keys_to_self()
    
    def get_interval_list(self) -> IntervalList:
        return NotImplemented

    def interval_lists(self) -> List[IntervalList]:
        return [self.get_interval_list()]
    
    def chromatic_interval_lists(self) -> ChromaticIntervalList:
        return [interval.get_chromatic_interval_list() for interval in self.interval_lists()]