from __future__ import annotations

from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import Dict, List, Optional, Self, Tuple, TypeVar, Union

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fret.fret_delta import FretDelta
from instruments.fretted_instrument.position.fret.frets import Frets
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from instruments.fretted_instrument.position.string.strings import Strings
from instruments.fretted_instrument.position.string.string import String
from instruments.fretted_instrument.position.positions_consts import *
from instruments.fretted_instrument.position.string.string_deltas import StringDelta
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList, MakeableWithSingleArgument
from utils.util import assert_typing

string_number_to_note_played_when_free = {
    1: ChromaticNote(-8),
    2: ChromaticNote(-3),
    3: ChromaticNote(2),
    4: ChromaticNote(7),
    5: ChromaticNote(11),
    6: ChromaticNote(16),
}
"""The chromatic note sounded by each string number (1-indexed) when played open (fret 0), for a standard-tuned
6-string guitar-like instrument."""


@dataclass(frozen=True)
class PositionOnFrettedInstrument(MakeableWithSingleArgument, DataClassWithDefaultArgument):
    """A position on the fretted_instrument, that is, a string and a fret.
    Fret 0 is open. Fret None is not played.

    Order is the same as its chromatic note, and in case of equality the string. Not played notes is maximal. This ensure that the minimal of a chord is its lowest note."""
    string: String
    """The string this position is on."""
    fret: Fret
    """The fret this position is on (0 for open, `None`/not-played encoded via `Fret.is_not_played()`)."""

    @staticmethod
    def from_chromatic(instrument: FrettedInstrument, note:ChromaticNote, absolute: bool, strings: Optional[Strings] = None, frets: Optional[Frets] = None) -> List[PositionOnFrettedInstrument]:
        """Return every position playing `note` on `instrument`, restricted to `strings` (default: all strings)
        and `frets` (default: all playable frets). `absolute` is passed through to `String.position_for_note`
        to control whether the resulting fret is expressed as an absolute fret number or relative to some origin."""
        assert_typing(instrument, FrettedInstrument)
        if frets is None:
            frets = Frets.all_played(instrument=instrument)
        if strings is None:
            strings = instrument.strings()
        assert_typing(note, ChromaticNote)
        positions: List[PositionOnFrettedInstrument] = []
        for string in strings:
            pos = string.position_for_note(instrument, note, absolute)
            if pos is None or pos.fret not in frets:
                continue
            positions.append(pos)
        return positions
    
    def positions_for_interval_with_restrictions(self,
                                                 instrument: FrettedInstrument,
                                                 interval: ChromaticInterval, 
                                                 strings: Optional[Union[StringDelta, Strings]] = None, 
                                                 frets: Optional[Union[FretDelta, Frets]]=None) -> List[PositionOnFrettedInstrument]:
        """All positions reachable by moving `interval` away from `self`, restricted to the given `strings`/`frets`.

        `strings`/`frets` may each be given either as an already-resolved `Strings`/`Frets` range, or as a
        `StringDelta`/`FretDelta` (a relative offset from `self.string`/`self.fret`), which is resolved to a
        concrete range before searching. Defaults to any string and any playable fret."""
        assert_typing(instrument, FrettedInstrument)
        if strings is None:
            strings = StringDelta.ANY_STRING(instrument)
        if frets is None:
            frets = Frets.all_played(instrument)
        if isinstance(strings, StringDelta):
            strings = strings.range(instrument, self.string)
        if isinstance(frets, FretDelta):
            frets = frets.range(instrument, self.fret)
        chromatic_note = self.get_chromatic() + interval
        return PositionOnFrettedInstrument.from_chromatic(instrument, chromatic_note, self.fret.absolute, strings, frets)

    def __eq__(self, other: PositionOnFrettedInstrument) -> bool:
        """Two positions are equal iff they share the same string and fret."""
        assert_typing(other, PositionOnFrettedInstrument)
        return isinstance(other, PositionOnFrettedInstrument) and self.fret == other.fret and self.string == other.string

    def __lt__(self, other: PositionOnFrettedInstrument) -> bool:
        """Order by chromatic pitch, then by string (see class docstring). A not-played position (no chromatic
        note) sorts as maximal, i.e. never less than anything."""
        if self.get_chromatic() is None:
            return False
        if other.get_chromatic() is None:
            return True
        return (self.get_chromatic(), self.string) < (other.get_chromatic(), other.string)

    def __le__(self, other: PositionOnFrettedInstrument) -> bool:
        """`self == other or self < other`."""
        return self == other or self<other

    def __hash__(self) -> int:
        """Hash consistent with `__eq__`: based on `(fret, string)`."""
        return hash((self.fret, self.string))

    def __repr__(self) -> str:
        """A `.make(...)` call that reconstructs this position, e.g. `PositionOnFrettedInstrument.make(1, 0)`."""
        return f"{self.__class__.__name__}.make({self.string.value}, {self.fret.value})"

    def __sub__(self, other: PositionOnFrettedInstrument) -> ChromaticInterval:
        """The chromatic interval from `other`'s note to `self`'s note."""
        assert isinstance(other, PositionOnFrettedInstrument)
        return self.get_chromatic() - other.get_chromatic()

    def singleton_diagram_svg_name(self, instrument: FrettedInstrument) -> str:
        """A unique filename for the diagram containing only this note."""
        assert_typing(instrument, FrettedInstrument)
        return f"""{self.singleton_diagram_key(instrument)}.svg"""

    def singleton_diagram_key(self, instrument: FrettedInstrument) -> str:
        """A unique name short name for this position."""
        assert_typing(instrument, FrettedInstrument)
        return f"""{instrument.get_name()}_{self.string.value}_{self.fret.value}"""

    def singleton_diagram_svg(self, instrument: FrettedInstrument, fretted_position_maker: "FrettedPositionMaker") -> str:
        """The svg for a diagram with only this note"""
        assert_typing(instrument, FrettedInstrument)
        from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument
        return SetOfPositionOnFrettedInstrument.make({self}, absolute=True).svg(instrument=instrument, absolute=True, fretted_position_maker = fretted_position_maker)

    def transpose_same_string(self, transpose: int, transpose_open: bool, transpose_not_played: bool) -> Self:
        """Return `self` with the fret shifted by `transpose` half-steps on the same string.
        `transpose_open`/`transpose_not_played` control whether an open/not-played fret is itself shifted
        (see `Fret.transpose`) or left as-is."""
        return dataclasses.replace(self, fret=self.fret.transpose(transpose, transpose_open, transpose_not_played))

    #pragma mark - MakeableWithSingleArgument

    def repr_single_argument(self) -> str:
        """The `(string_value, fret_value)` tuple, as a string, used by `MakeableWithSingleArgument`'s repr machinery."""
        return f"""{(self.string.value, self.fret.value)}"""

    @classmethod
    def _make_single_argument(cls, arg: Tuple[FrettedInstrument, Union[String, int], Union[Fret, int]]) -> Self:
        """Build an instance from a `(string, fret)` pair, as required by `MakeableWithSingleArgument`."""
        string, fret = arg
        return cls.make(string= string, fret=fret)

    #pragma mark - ChromaticGetter

    def get_chromatic(self) -> Optional[ChromaticNote]:
        """The chromatic note sounded at this position, or `None` if the string is not played (see `Fret.is_not_played`)."""
        if self.fret.is_not_played():
            return None
        return self.string.note_open + ChromaticInterval.make(self.fret.value)

    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self) -> None:
        """Validate that `fret` and `string` have the expected types."""
        assert_typing(self.fret, Fret)
        assert_typing(self.string, String)

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Normalize constructor arguments: positional `string`/`fret` become keyword arguments, and `fret` is
        additionally passed through `Fret.make_single_argument` so it may be given as a raw int/tuple."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fret", Fret.make_single_argument)
        return args, kwargs

PositionOnFrettedInstrumentType = TypeVar("PositionOnFrettedInstrumentType", bound=PositionOnFrettedInstrument)
"""Generic type variable bound to `PositionOnFrettedInstrument`, used by generic containers/mixins that must stay
parametrized over the concrete position subclass (e.g. `PositionOnFrettedInstrumentWithFingers`)."""

class PositionOnFrettedInstrumentFrozenList(FrozenList[PositionOnFrettedInstrument]):
    """An immutable list of `PositionOnFrettedInstrument`."""
    type = PositionOnFrettedInstrument
    """The element type enforced by this `FrozenList`."""