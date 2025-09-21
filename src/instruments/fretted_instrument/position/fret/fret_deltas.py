from dataclasses import dataclass
from typing import ClassVar, Optional, Type
#from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.abstract_delta import AbstractDelta
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fret.frets import Frets
from utils.util import assert_optional_typing, assert_typing


@dataclass(frozen=True)
class FretDelta(AbstractDelta[Frets, Fret]):
    """Represents a way to compute frets given a current fret.
     For example, restricting a search of position to the current note, or fret not far away, or only a different fret."""
    #pragma mark - AbstractDelta

    min_t: ClassVar[int] = 1
    type_t: ClassVar[Type] = Fret
    type_ts: ClassVar[Type] = Frets


    @classmethod
    def max_t(cls, instrument: "FrettedInstrument") -> int:
        return instrument.number_of_frets

    @classmethod
    def create_T(cls, instrument: "FrettedInstrument", i: int, origine: Fret) -> Fret:
        assert_typing(origine, Fret)
        return Fret.make(i, origine.absolute)

    @classmethod
    def create_Ts(cls, instrument: "FrettedInstrument", min_t: Fret, max_t: Fret, origine: Fret) -> Frets:
        return Frets.make(closed_fret_interval=(min_t, max_t), allow_open=False, allow_not_played=False, absolute=origine.absolute)
    
    @classmethod
    def create_empty_ts(cls):
        return Frets.empty()