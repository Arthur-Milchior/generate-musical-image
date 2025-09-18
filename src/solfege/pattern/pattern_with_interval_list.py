from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import sys
from typing import ClassVar, Dict, Generic, List, Optional, Self, Type, TypeVar, Union

from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness, KeyType
from utils.recordable import RecordKeeperType, Recordable
from utils.util import assert_iterable_typing, assert_typing


@dataclass(frozen=True)
class PatternWithIntervalList(Recordable[IntervalListPattern, RecordKeeperType], ClassWithEasyness[KeyType], DataClassWithDefaultArgument, ABC, Generic[RecordKeeperType, KeyType]):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """Associate a interval list to its patterns"""

    """Whether to record this pattern in the list of patterns."""

    #Must be implemented by subtype
    
    @abstractmethod
    def get_interval_list(self) -> IntervalListPattern:
        return NotImplemented

    @classmethod
    @abstractmethod
    def _get_instantiation_type(cls) -> Type["AbstractPairInsantiation[Self]"]:
        return NotImplemented

    # public

    def interval_lists(self) -> List[IntervalListPattern]:
        return [self.get_interval_list()]
    
    def chromatic_interval_lists(self) -> ChromaticIntervalListPattern:
        return [interval.get_chromatic_interval_list() for interval in self.interval_lists()]

    def get_chromatic_instantiation(self, lowest_chromatic_note: ChromaticNote) -> "AbstractChromaticInstantiation[Self]":
        return self._get_instantiation_type.related_chromatic_type(lowest_chromatic_note)
    
    def get_instantiation(self, lowest_note: Note) -> "AbstractPairInstantiation[Self]":
        return self._get_instantiation_type(lowest_note)
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        defaut_dict = super()._default_arguments_for_constructor(args, kwargs)
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
    

PatternType = TypeVar("PatternType", bound=PatternWithIntervalList)