from __future__ import annotations

from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import Dict, List, Optional, Tuple, TypeVar, Union

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fret.fret_deltas import FretDelta
from instruments.fretted_instrument.position.fret.frets import Frets
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from instruments.fretted_instrument.position.string.strings import Strings
from instruments.fretted_instrument.position.string.string import String
from instruments.fretted_instrument.position.consts import *
from instruments.fretted_instrument.position.string.string_deltas import StringDelta
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList, MakeableWithSingleArgument
from utils.util import assert_typing

# The 1-th string played free
string_number_to_note_played_when_free = {
    1: ChromaticNote(-8),
    2: ChromaticNote(-3),
    3: ChromaticNote(2),
    4: ChromaticNote(7),
    5: ChromaticNote(11),
    6: ChromaticNote(16),
}
@dataclass(frozen=True)
class PositionOnFrettedInstrument(MakeableWithSingleArgument, DataClassWithDefaultArgument):
    """A position on the fretted_instrument, that is, a string and a fret.
    Fret 0 is open. Fret None is not played.

    Order is the same as its chromatic note, and in case of equality the string. Not played notes is maximal. This ensure that the minimal of a chord is its lowest note."""
    string: String
    fret: Fret

    @staticmethod
    def from_chromatic(instrument: FrettedInstrument, note:ChromaticNote, absolute: bool, strings: Optional[Strings] = None, frets: Optional[Frets] = None):
        assert_typing(instrument, FrettedInstrument)
        """Return all the position for `note` in `frets` and `strings`"""
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

    def __eq__(self, other: PositionOnFrettedInstrument):
        assert_typing(other, PositionOnFrettedInstrument)
        return isinstance(other, PositionOnFrettedInstrument) and self.fret == other.fret and self.string == other.string

    def __lt__(self, other: PositionOnFrettedInstrument):
        if self.get_chromatic() is None:
            return False
        if other.get_chromatic() is None:
            return True
        return (self.get_chromatic(), self.string) < (other.get_chromatic(), other.string)
    
    def __le__(self, other: PositionOnFrettedInstrument):
        return self == other or self<other

    def __hash__(self):
        return hash((self.fret, self.string))

    def __repr__(self):
        return f"{self.__class__.__name__}.make({self.string.value}, {self.fret.value})"
    
    def __sub__(self, other: PositionOnFrettedInstrument) -> ChromaticInterval:
        assert isinstance(other, PositionOnFrettedInstrument)
        return self.get_chromatic() - other.get_chromatic()
    
    def singleton_diagram_svg_name(self, instrument: FrettedInstrument):
        assert_typing(instrument, FrettedInstrument)
        """A unique filename for the diagram containing only this note."""
        return f"""{self.singleton_diagram_key(instrument)}.svg"""
    
    def singleton_diagram_key(self, instrument: FrettedInstrument):
        assert_typing(instrument, FrettedInstrument)
        """A unique name short name for this position."""
        return f"""{instrument.name}_{self.string.value}_{self.fret.value}"""

    def singleton_diagram_svg(self, instrument: FrettedInstrument):
        """The svg for a diagram with only this note"""
        assert_typing(instrument, FrettedInstrument)
        from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument
        return SetOfPositionOnFrettedInstrument.make({self}).svg(instrument=instrument, absolute=True)
    
    def transpose_same_string(self, transpose: int, transpose_open: bool, transpose_not_played: bool):
        return dataclasses.replace(self, fret=self.fret.transpose(transpose, transpose_open, transpose_not_played))

    #pragma mark - MakeableWithSingleArgument
    
    def repr_single_argument(self) -> str:
        return f"""{(self.string.value, self.fret.value)}"""

    @classmethod
    def _make_single_argument(cls, arg: Tuple[FrettedInstrument, Union[String, int], Union[Fret, int]]):
        string, fret = arg
        return cls.make(string= string, fret=fret)
    
    #pragma mark - ChromaticGetter

    def get_chromatic(self) -> Optional[ChromaticNote]:
        if self.fret.is_not_played():
            return None
        return self.string.note_open + ChromaticInterval.make(self.fret.value)

    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        assert_typing(self.fret, Fret)
        assert_typing(self.string, String)

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "string")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "fret", Fret.make_single_argument)
        return args, kwargs

PositionOnFrettedInstrumentType = TypeVar("PositionOnFrettedInstrumentType", bound=PositionOnFrettedInstrument)

class PositionOnFrettedInstrumentFrozenList(FrozenList[PositionOnFrettedInstrument]):
    type = PositionOnFrettedInstrument