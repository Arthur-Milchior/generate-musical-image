from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Self, Type

from solfege.pattern.pattern_with_interval_lists import PatternWithIntervalLists
from solfege.pattern.pattern_with_name import PatternWithName
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import IntervalList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness
from utils.frozenlist import StrFrozenList
from utils.util import assert_iterable_typing, assert_typing
from solfege.value.key.keys import nor_flat_nor_sharp


@dataclass(frozen=True)
class SolfegePattern(PatternWithName, PatternWithIntervalLists, ClassWithEasyness[int], DataClassWithDefaultArgument):
    """To be inherited by classes implementing a specific kind of pattern (scale, chord), that can be retrieved by
    name or iterated upon all patterns"""

    """The interval between the signature for this scale and the signature for the major scale with the same key.
    E.g. for minor, use three_flats"""

    interval_for_signature: Interval

    """A unique id, in order of creations. For values of the same class, the smallest index is the first pattern to learn."""
    _pattern_index: int = field(compare=False, hash=False)

    """The English Wikipedia page(s) (or other reference) documenting this pattern. See src/solfege/pattern/multi_octave_patterns.md
    for how patterns whose real-world span exceeds one octave are represented here."""
    source: StrFrozenList = field(compare=False, hash=False)

    """A short explanation of what is notable about this pattern: how its name/notation came to be, how it is
    constructed, or anything else that helps make sense of it."""
    description: str = field(compare=False, hash=False)

    _is_chord_pattern: bool


    def __lt__(self, other: Self):
        assert_typing(other, self.__class__)
        return self._pattern_index < other._pattern_index
    
    def __le__(self, other: Self):
        assert_typing(other, self.__class__)
        return self._pattern_index <= other._pattern_index
    
    #pragma mark - ClassWithEasyness

    def easy_key(self) -> int:
        """A hard coded easyness number for this pattern."""
        return self._pattern_index
    
    #pragma mark - Recordable
    _key_type: ClassVar[Type] = IntervalList

    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["interval_for_signature"] = nor_flat_nor_sharp
        default_dict["source"] = StrFrozenList()
        default_dict["description"] = ""
        default_dict["_is_chord_pattern"] = False
        SolfegePattern.max_index += 1
        default_dict["_pattern_index"] = SolfegePattern.max_index
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_source(source):
            if isinstance(source, str):
                source = [source]
            return StrFrozenList(source)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "interval_for_signature")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "source", clean_source)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "description")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.interval_for_signature, Interval)
        assert_typing(self.source, StrFrozenList)
        assert_iterable_typing(self.source, str)
        assert_typing(self.description, str)
        super().__post_init__()