from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Union

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from guitar.position.fret import NOT_PLAYED, OPEN_FRET, Fret
from guitar.position.string import String
from guitar.position.consts import *
from guitar.position.frets import Frets
from guitar.position.string_deltas import ANY_STRING, StringDeltas
from guitar.position.strings import ALL_STRINGS, Strings
from guitar.position.string import strings
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
# COLOR_TONIC = "red"
# COLOR_THIRD = "blue"
# COLOR_FIFTH = "grey"
# COLOR_QUALITY = "green"
# COLOR_OTHER = "purple"

# colors = [COLOR_TONIC, COLOR_OTHER, COLOR_OTHER, COLOR_THIRD, COLOR_THIRD, ]

GuitarPositionMakeSingleArgumentType = Union["GuitarPosition", Tuple[Union[String, int], Union[Fret, Optional[int]]]]
@dataclass(frozen=True)
class GuitarPosition:
    """A position on the guitar, that is, a string and a fret.
    Fret 0 is open. Fret None is not played.

    Order is the same as its chromatic note, and in case of equality the string. Not played notes is maximal. This ensure that the minimal of a chord is its lowest note."""
    string: String
    fret: Fret

    def __post_init__(self):
        assert_typing(self.fret, Fret)
        assert_typing(self.string, String)

    @classmethod
    def make(cls, string: Union[String, int], fret: Union[Fret, Optional[int]]):
        string = String.make_single_argument(string)
        fret = Fret.make_single_argument(fret)
        return GuitarPosition(string, fret)
    
    @classmethod
    def make_single_argument(cls, arg: GuitarPositionMakeSingleArgumentType):
        if isinstance(arg, GuitarPosition):
            return arg
        string, fret = arg
        return cls.make(string, fret)

    @staticmethod
    def from_chromatic(note:ChromaticNote, strings: Strings = ALL_STRINGS, frets: Frets = Frets()):
        """Return all the position for `note` in `frets` and `strings`"""
        assert_typing(note, ChromaticNote)
        positions: List[GuitarPosition] = []
        for string in strings:
            fret = string.fret_for_note(note)
            if fret is None:
                continue
            if fret not in frets:
                continue
            positions.append(GuitarPosition(string, fret))
        return positions
    
    def add(self, interval: ChromaticInterval, strings: Union[StringDeltas, Strings] = ANY_STRING, frets: Frets = Frets()):
        if isinstance(strings, StringDeltas):
            strings = strings.strings(self.string)
        note = self.get_chromatic() + interval
        return GuitarPosition.from_chromatic(note, strings, frets)

    def get_chromatic(self) -> Optional[ChromaticNote]:
        if self.fret.is_not_played():
            return None
        return self.string.note_open + ChromaticInterval(self.fret.value)

    def svg(self, absolute: bool, stroke_color: str= "black"):
        """Draw this position, assuming that f already contains the svg for the fret"""
        fill_color = "white" if self.fret.is_open() else "black"
        x = self.string.x()
        if self.fret.is_not_played():
            if absolute:
                return f"""<text x="{int(x)-15}" y="{int(MARGIN)-10}" font-size="50">x</text><!-- string {self.string.value}, not played-->"""
            return f"""<!-- string {self.string.value} not played. Not shown as it's transposable-->"""
        y = self.fret.y_dots()
        return f"""<circle cx="{int(x)}" cy="{int(y)}" r="{int(CIRCLE_RADIUS)}" fill="{stroke_color}" stroke="{stroke_color}" stroke-width="3"/><!-- String N° {self.string.value}, position {self.fret.value}-->"""

    def __eq__(self, other: GuitarPosition):
        assert_typing(other, GuitarPosition)
        return isinstance(other, GuitarPosition) and self.fret == other.fret and self.string == other.string

    def __lt__(self, other: GuitarPosition):
        if self.get_chromatic() is None:
            return False
        if other.get_chromatic() is None:
            return True
        return (self.get_chromatic(), self.string) < (other.get_chromatic(), other.string)
    
    def __le__(self, other: GuitarPosition):
        return self == other or self<other

    def __hash__(self):
        return hash((self.fret, self.string))

    def __repr__(self):
        return f"{self.__class__.__name__}.make({self.string.value}, {self.fret.value})"
    
    def __sub__(self, other: GuitarPosition) -> ChromaticInterval:
        assert isinstance(other, GuitarPosition)
        return self.get_chromatic() - other.get_chromatic()
    
    def singleton_diagram_svg_name(self):
        """A unique filename for the diagram containing only this note."""
        return f"""{self.singleton_diagram_key()}.svg"""
    
    def singleton_diagram_key(self):
        """A unique name short name for this position."""
        return f"""guitar_{self.string.value}_{self.fret.value}"""

    def singleton_diagram_svg(self):
        """The svg for a diagram with only this note"""
        from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
        return SetOfGuitarPositions(frozenset({self})).svg(absolute=True)
    
    def transpose_same_fret(self, transpose: int, transpose_open: bool, transpose_not_played: bool):
        return self.__class__(self.string, self.fret.transpose(transpose, transpose_open, transpose_not_played))