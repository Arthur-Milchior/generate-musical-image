

from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.string.string import String, StringFrozenList
from fretted_instrument.position.string.strings import Strings
from utils.util import assert_typing


class StringsInterval(Strings):
    """Represents a set of string that is an interval."""
    def __init__(self, instrument: FrettedInstrument, min: String, max:String):
        assert_typing(instrument, FrettedInstrument)
        super().__init__(instrument, StringFrozenList([instrument.string(s) for s in range(min.value, max.value + 1)]))