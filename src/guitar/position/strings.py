from dataclasses import dataclass
from typing import List

from guitar.position.string import String, strings
from utils.util import assert_typing

@dataclass(frozen=True, eq=True)
class Strings:
    """Represents a set of string of the guitar."""
    strings: List[String]

    def __post_init__(self):
        assert_typing(self.strings, list)
        for string in strings:
            assert_typing(string, String)

    def __iter__(self):
        yield from self.strings

    def __lt__(self, other: "Strings"):
        return self.strings < other.strings
    
    def __eq__(self, other: "Strings"):
        assert_typing(other, Strings)
        return self.strings == other.strings
    

class StringsInterval(Strings):
    """Represents a set of string that is an interval."""
    def __init__(self, min: String, max:String):
        super().__init__([strings[s-1] for s in range(min.value, max.value + 1)])

    
ALL_STRINGS = Strings(strings)
NO_STRINGS = Strings([])