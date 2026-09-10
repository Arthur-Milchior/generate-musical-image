from dataclasses import dataclass, field
import sys
from typing import ClassVar, Dict, List, Optional, Self, Tuple, Union

from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList, StrFrozenList
from utils.util import assert_iterable_typing, assert_optional_typing, assert_typing


@dataclass(frozen=True)
class PatternWithName(DataClassWithDefaultArgument):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    name_to_pattern: ClassVar[Dict[str, "PatternWithName"]]
    """Associate a name to its pattern"""
    all_patterns: ClassVar[List['PatternWithName']]
    """associate to each class the list of all instances of this class"""

    names: StrFrozenList
    """All the names/aliases this pattern is known by; the first is the canonical one (see
    `first_of_the_names()`)."""

    notation: Optional[str]
    """A short symbolic notation for this pattern (e.g. "M" for a major chord), or None if it has none."""

    record: bool = field(compare=False)
    """Whether to record this pattern in the list of patterns."""


    def first_of_the_names(self, for_file: bool = False) -> str:
        """The first of all the names associated to this pattern. Hopefully the most canonical one"""
        name = self.names[0] 
        if for_file:
            return name.replace(" ", "_")
        return name

    def get_names(self) -> StrFrozenList:
        """All the names associated to this pattern"""
        return self.names

    @classmethod
    def get_all_instances(cls) -> List["PatternWithName"]:
        """All recorded instances of this concrete pattern class, in creation order."""
        return cls.all_patterns

    @classmethod
    def get_from_name(cls, name: str) -> Optional["PatternWithName"]:
        """The recorded instance of this class registered under `name`, or None if there is none."""
        return cls.name_to_pattern.get(name)


    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Dict:
        """Default `record` to True (register on construction) and `notation` to None (no symbolic notation)."""
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["record"] = True
        default_dict["notation"] = None
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Coerce `names` into a `StrFrozenList` and pass `notation`/`record` through positional-to-keyword
        normalization."""
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "names", StrFrozenList)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notation")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "record")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self) -> None:
        """Validate field types, then, when `record` is True, register `self` into `all_patterns` and
        `name_to_pattern` under every one of `names` -- asserting each name isn't already taken (the usual
        cause of that assertion firing is a module being imported twice)."""
        assert_typing(self.interval_for_signature, Interval)
        assert_typing(self.names, StrFrozenList)
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