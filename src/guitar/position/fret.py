from dataclasses import dataclass
from typing import Optional, Union

from solfege.interval.chromatic import ChromaticInterval
from utils.util import assert_optional_type, assert_typing


@dataclass(frozen=True, eq=True)
class Fret(ChromaticInterval):
    """
    Represents one of the fret of the guitar.

    None represents a string that is not played and is assumed to be greater than any played string."""
    value: Optional[int]

    def __post_init__(self):
        assert_optional_type(self.value, int)

    def __add__(self, other: Union[ChromaticInterval, int]):
        if self.value is None:
            return self
        if isinstance(other, ChromaticInterval):
            other = other.value
        value = self.value + other
        if value < 0:
            return None
        fret = Fret(value)
        if fret > HIGHEST_FRET:
            return None
        return fret
    
    def __lt__(self, other: "Fret"):
        if self.value is None:
            return False
        if other.value is None:
            return True
        return self.value < other.value
    
    def __eq__(self, other: "Fret"):
        assert_typing(other, Fret)
        return self.value == other.value

NOT_PLAYED = Fret(None)
OPEN_FRET = Fret(0)
HIGHEST_FRET = Fret(24)