from dataclasses import dataclass
from typing import ClassVar, Optional
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.abstract_delta import AbstractDelta
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.fret.frets import Frets
from utils.util import assert_optional_typing


@dataclass(frozen=True)
class FretDelta(AbstractDelta[Frets, Fret]):
    """Represents a way to compute frets given a current fret.
     For example, restricting a search of position to the current note, or fret not far away, or only a different fret."""
    min_t: ClassVar[int] = 1
    max_t: ClassVar[int] = 24

    @classmethod
    def create_T(cls, instrument: FrettedInstrument, i: int) -> Fret:
        return instrument.fret(i)

    @classmethod
    def create_Ts(cls, instrument: FrettedInstrument, min_t: Fret, max_t: Fret) -> Frets:
        return Frets.make(instrument, (min_t, max_t), False, False)
    
    @classmethod
    def create_empty_ts(cls, instrument: FrettedInstrument):
        return Frets.empty(instrument)