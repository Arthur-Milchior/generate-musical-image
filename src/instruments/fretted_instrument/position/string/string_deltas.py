from dataclasses import dataclass
from typing import ClassVar, Optional, Type
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.abstract_delta import AbstractDelta
from instruments.fretted_instrument.position.string.string import String
from instruments.fretted_instrument.position.string.strings import Strings
from utils.util import assert_optional_typing


@dataclass(frozen=True)
class StringDelta(AbstractDelta[Strings, String]):
    """Represents a way to compute strings given a current string.
     For example, restricting a search of position to the current note, or string not far away, or only a different string."""

    #pragma mark - AbstractDelta
    min_t: ClassVar[int] = 1
    """The smallest raw string number: strings are 1-indexed."""
    type_t: ClassVar[Type] = String
    """A `StringDelta` is applied to/from a single `String`."""
    type_ts: ClassVar[Type] = Strings
    """A `StringDelta` resolves to a `Strings` range."""

    @classmethod
    def max_t(cls, instrument:FrettedInstrument) -> int:
        """The number of strings on `instrument` (the largest valid string number)."""
        return instrument.number_of_strings()
    @classmethod
    def create_T(cls, instrument: FrettedInstrument, i: int, origine: String) -> String:
        """The string numbered `i` on `instrument`."""
        return instrument.string(i)

    @classmethod
    def create_Ts(cls, instrument: FrettedInstrument, min_string: String, max_string: String, origine: String) -> Strings:
        """Every string on `instrument` between `min_string` and `max_string` (inclusive)."""
        return Strings.make_interval(instrument, min_string, max_string)

    @classmethod
    def create_empty_ts(cls) -> Strings:
        """The empty `Strings` set."""
        return Strings.make([])

    #pragma mark - public

    @staticmethod
    def SAME_STRING_ONLY(instrument: "FrettedInstrument") -> "StringDelta":
        """A delta matching only the reference string itself (offset 0)."""
        return StringDelta((0, 0))

    @staticmethod
    def SAME_OR_NEXT_STRING(instrument: "FrettedInstrument") -> "StringDelta":
        """A delta matching the reference string or the very next one (offsets 0 to 1)."""
        return StringDelta((0, 1))

    @staticmethod
    def NEXT_STRING_ONLY(instrument: "FrettedInstrument") -> "StringDelta":
        """A delta matching only the string right after the reference one (offset 1)."""
        return StringDelta((1, 1))

    @staticmethod
    def NEXT_STRING_OR_GREATER(instrument: "FrettedInstrument") -> "StringDelta":
        """A delta matching the next string and anything beyond (offset 1 to unbounded)."""
        return StringDelta((1, None))

    @staticmethod
    def SAME_STRING_OR_GREATER(instrument: "FrettedInstrument") -> "StringDelta":
        """A delta matching the reference string and anything beyond (offset 0 to unbounded)."""
        return StringDelta((0, None))

    @staticmethod
    def ANY_STRING(instrument: "FrettedInstrument") -> "StringDelta":
        """A delta matching any string, with no restriction (offset unbounded on both sides)."""
        return StringDelta((None, None))
