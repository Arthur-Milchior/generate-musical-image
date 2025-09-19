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
    type_t: ClassVar[Type] = String
    type_ts: ClassVar[Type] = Strings

    @classmethod
    def max_t(cls, instrument:FrettedInstrument) -> int:
        return instrument.number_of_strings()
    @classmethod
    def create_T(cls, instrument: FrettedInstrument, i: int, original: String) -> String:
        return instrument.string(i)

    @classmethod
    def create_Ts(cls, instrument: FrettedInstrument, min_string: String, max_string: String, original: String) -> Strings:
        return Strings.make_interval(instrument, min_string, max_string)
    
    @classmethod
    def create_empty_ts(cls):
        return Strings.make([])
    
    #pragma mark - public

    @staticmethod
    def SAME_STRING_ONLY(instrument: "FrettedInstrument"):
        return StringDelta((0, 0))
    
    @staticmethod
    def SAME_OR_NEXT_STRING(instrument: "FrettedInstrument"):
        return StringDelta((0, 1))
    
    @staticmethod
    def NEXT_STRING_ONLY(instrument: "FrettedInstrument"):
        return StringDelta((1, 1))
    
    @staticmethod
    def NEXT_STRING_OR_GREATER(instrument: "FrettedInstrument"):
        return StringDelta((1, None))
    
    @staticmethod
    def SAME_STRING_OR_GREATER(instrument: "FrettedInstrument"):
        return StringDelta((0, None))
    
    @staticmethod
    def ANY_STRING(instrument: "FrettedInstrument"):
        return StringDelta((None, None))
