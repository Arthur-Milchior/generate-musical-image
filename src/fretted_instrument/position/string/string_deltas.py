from dataclasses import dataclass
from typing import ClassVar, Optional
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.abstract_delta import AbstractDelta
from fretted_instrument.position.string.string import String
from fretted_instrument.position.string.strings import Strings
from fretted_instrument.position.string.strings_intervals import StringsInterval
from utils.util import assert_optional_typing


@dataclass(frozen=True)
class StringDelta(AbstractDelta[Strings, String]):
    """Represents a way to compute strings given a current string.
     For example, restricting a search of position to the current note, or string not far away, or only a different string."""
    min_t: ClassVar[int] = 1
    max_t: ClassVar[int] = 6

    @classmethod
    def create_T(cls, instrument: FrettedInstrument, i: int) -> String:
        return instrument.string(i)

    @classmethod
    def create_Ts(cls, instrument: FrettedInstrument, min_string: String, max_string: String) -> Strings:
        return StringsInterval(instrument, min_string, max_string)
    
    @classmethod
    def create_empty_ts(cls, instrument: FrettedInstrument):
        return StringDelta(instrument, [])

    @staticmethod
    def SAME_STRING_ONLY(instrument:FrettedInstrument):
        return StringDelta(instrument, 0, 0)
    
    @staticmethod
    def SAME_OR_NEXT_STRING(instrument:FrettedInstrument):
        return StringDelta(instrument, 0, 1)
    
    @staticmethod
    def NEXT_STRING_ONLY(instrument:FrettedInstrument):
        return StringDelta(instrument, 1, 1)
    
    @staticmethod
    def NEXT_STRING_OR_GREATER(instrument:FrettedInstrument):
        return StringDelta(instrument, 1)
    
    @staticmethod
    def SAME_STRING_OR_GREATER(instrument:FrettedInstrument):
        return StringDelta(instrument, 0)
    
    @staticmethod
    def ANY_STRING(instrument:FrettedInstrument):
        return StringDelta(instrument)