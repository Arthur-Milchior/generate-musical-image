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
    """The smallest raw fret number a `FretDelta` can resolve to (fret 0, the open string, is handled separately
    and never produced through this delta)."""
    type_t: ClassVar[Type] = Fret
    """A `FretDelta` is applied to/from a single `Fret`."""
    type_ts: ClassVar[Type] = Frets
    """A `FretDelta` resolves to a `Frets` range."""


    @classmethod
    def max_t(cls, instrument: "FrettedInstrument") -> int:
        """The largest playable fret number on `instrument`."""
        return instrument.number_of_frets()

    @classmethod
    def create_T(cls, instrument: "FrettedInstrument", i: int, origine: Fret) -> Fret:
        """Build the `Fret` with raw value `i`, sharing `origine`'s `absolute` flag."""
        assert_typing(origine, Fret)
        return Fret.make(i, origine.absolute)

    @classmethod
    def create_Ts(cls, instrument: "FrettedInstrument", min_t: Fret, max_t: Fret, origine: Fret) -> Frets:
        """Build the closed `Frets` range `[min_t, max_t]`, excluding the open string and not-played, sharing
        `origine`'s `absolute` flag."""
        return Frets.make(closed_fret_interval=(min_t, max_t), allow_open=False, allow_not_played=False, absolute=origine.absolute)

    @classmethod
    def create_empty_ts(cls):
        """The empty `Frets` range."""
        return Frets.empty()