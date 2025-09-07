from dataclasses import dataclass
from typing import ClassVar, Optional
from guitar.position.abstract_delta import AbstractDelta
from guitar.position.string.string import String, strings
from guitar.position.string.strings import Strings, NO_STRINGS, StringsInterval
from utils.util import assert_optional_typing


@dataclass(frozen=True)
class StringDelta(AbstractDelta[Strings, String]):
    """Represents a way to compute strings given a current string.
     For example, restricting a search of position to the current note, or string not far away, or only a different string."""
    min_t: ClassVar[int] = 1
    max_t: ClassVar[int] = 6

    @classmethod
    def create_T(cls, i: int) -> String:
        return strings[i-1]

    @classmethod
    def create_Ts(cls, min_string: String, max_string: String) -> Strings:
        return StringsInterval(min_string, max_string)
    
    @classmethod
    def create_empty_ts(cls):
        return NO_STRINGS


SAME_STRING_ONLY = StringDelta(0, 0)
SAME_OR_NEXT_STRING = StringDelta(0, 1)
NEXT_STRING_ONLY = StringDelta(1, 1)
NEXT_STRING_OR_GREATER = StringDelta(1)
SAME_STRING_OR_GREATER = StringDelta(0)
ANY_STRING = StringDelta()