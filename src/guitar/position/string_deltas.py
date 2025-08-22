

from dataclasses import dataclass
from typing import Optional
from guitar.position import strings
from guitar.position.string import String, strings
from guitar.position.strings import Strings, NO_STRINGS, StringsInterval
from utils.util import assert_optional_type


@dataclass(frozen=True, eq=True)
class StringDeltas:
    """Represents a way to compute strings given a current string. For example, restricting a search of position to the current note, or string not far away, or only a different string."""
    min_string_delta: Optional[int]= None
    max_string_delta: Optional[int]= None

    def __post_init__(self):
        assert_optional_type(self.min_string_delta, int)
        assert_optional_type(self.max_string_delta, int)

    def min_string(self, string: String) -> Optional[String]:
        if self.min_string_delta is None:
            return strings[0]
        s = string.value + self.min_string_delta
        if s > 6:
            return None
        return strings[max(1, s)-1]

    def max_string(self, string: String) -> Optional[String]:
        if self.max_string_delta is None:
            return strings[5]
        s = string.value + self.max_string_delta
        if s < 1:
            return None
        return strings[min(6, s)-1]
    
    def strings(self, string: String) -> Strings:
        min_string = self.min_string(string)
        max_string = self.max_string(string)
        if min_string is None or max_string is None:
            return NO_STRINGS
        return StringsInterval(min_string, max_string)

SAME_STRING_ONLY = StringDeltas(0, 0)
SAME_OR_NEXT_STRING = StringDeltas(0, 1)
NEXT_STRING_ONLY = StringDeltas(1, 1)
NEXT_STRING_OR_GREATER = StringDeltas(1)
SAME_STRING_OR_GREATER = StringDeltas(0)
ANY_STRING = StringDeltas()