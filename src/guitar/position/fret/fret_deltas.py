from dataclasses import dataclass
from typing import ClassVar, Optional
from guitar.position.abstract_delta import AbstractDelta
from guitar.position.fret.fret import Fret
from guitar.position.fret.frets import EMPTY_FRETS, Frets
from utils.util import assert_optional_typing


@dataclass(frozen=True)
class FretDeltas(AbstractDelta[Frets, Fret]):
    """Represents a way to compute frets given a current fret.
     For example, restricting a search of position to the current note, or fret not far away, or only a different fret."""
    min_t: ClassVar[int] = 1
    max_t: ClassVar[int] = 24

    @classmethod
    def create_T(cls, i: int) -> Fret:
        return Fret(i)

    @classmethod
    def create_Ts(cls, min_fret: Fret, max_fret: Fret) -> Frets:
        return Frets(min_fret, max_fret, False, False)
    
    @classmethod
    def create_empty_ts(cls):
        return EMPTY_FRETS