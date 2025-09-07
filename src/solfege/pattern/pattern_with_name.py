from dataclasses import dataclass, field
import sys
from typing import ClassVar, Dict, List, Optional, Self, Tuple, Union

from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import ChromaticIntervalList, DataClassWithDefaultArgument, IntervalList
from utils.frozenlist import FrozenList
from utils.util import assert_all_same_class, assert_iterable_typing, assert_optional_typing, assert_typing, traceback_str
from solfege.value.key.key import nor_flat_nor_sharp


@dataclass(frozen=True)
class PatternWithName(DataClassWithDefaultArgument):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """Associate a name to its pattern"""
    name_to_pattern: ClassVar[Dict[str, "PatternWithName"]]
    """associate to each class the list of all instances of this class"""
    all_patterns: ClassVar[List['PatternWithName']]

    names: FrozenList[str]
    notation: Optional[str]
    """Whether to record this pattern in the list of patterns."""
    record: bool = field(compare=False)

    @classmethod
    def _default_arguments_for_constructor(cls):
        default_dict = super()._default_arguments_for_constructor()
        default_dict["record"] = True
        default_dict["notation"] = None
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "names", FrozenList)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notation")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "record")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.interval_for_signature, Interval)
        assert_typing(self.names, FrozenList)
        assert_typing(self.record, bool)
        assert_optional_typing(self.notation, str)
        assert_iterable_typing(self.names, str)
        if not self.record:
            return
        cls = self.__class__
        cls.all_patterns.append(self)
        for name in self.names:
            assert name not in cls.name_to_pattern, f""" "{name}" added twice in {cls}. Check for error above that would cause the definition of {name} to be imported twice."""
            cls.name_to_pattern[name] = self
        super().__post_init__()


    def first_of_the_names(self, for_file= False) -> str:
        """The first of all the names associated to this pattern. Hopefully the most canonical one"""
        name = self.names[0] 
        if for_file:
            return name.replace(" ", "_")
        return name

    def get_names(self):
        """All the names associated to this pattern"""
        return self.names

    @classmethod
    def get_all_instances(cls):
        return cls.all_patterns

    @classmethod
    def get_from_name(cls, name: str):
        return cls.name_to_pattern.get(name)
