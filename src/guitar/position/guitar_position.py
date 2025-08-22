from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

from solfege.interval import ChromaticInterval
from solfege.note import ChromaticNote
from guitar.position.fret import NOT_PLAYED, OPEN_FRET, Fret
from guitar.position.string import String
from guitar.position.frets import Frets
from guitar.position.string_deltas import ANY_STRING, StringDeltas
from guitar.position.strings import ALL_STRINGS, Strings
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

# Constants used in SVG
fret_distance = 50
string_distance = 30
circle_radius = 11


@dataclass(frozen=True, eq=True)
class GuitarPosition:
    """A position on the guitar, that is, a string and a fret.
    Fret 0 is open. Fret None is not played.

    Order is the same as its chromatic note, and in case of equality the string. Not played notes is maximal. This ensure that the minimal of a chord is its lowest note."""
    string: String
    fret: Fret

    def __post_init__(self):
        assert_typing(self.fret, Fret)
        assert_typing(self.string, String)

    @staticmethod
    def from_chromatic(note:ChromaticNote, strings: Strings = ALL_STRINGS, frets: Frets = Frets()):
        """Return all the position for `note` in `frets` and `strings`"""
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
        if self.fret == NOT_PLAYED:
            return None
        return self.string.note_open + ChromaticInterval(self.fret.value)

    def get_stroke_color(self):
        return "black"

    def svg(self):
        """Draw this position, assuming that f already contains the svg for the fret"""
        fill_color = "white" if self.fret == OPEN_FRET else "black"
        cx = string_distance * (self.string.value - 0.5)
        if self.fret is NOT_PLAYED:
            return f"""
    <text x="{int(cx)}" y="{int(fret_distance / 3)}" font-size="30">x</text>"""
        else:
            if self.fret == OPEN_FRET:
                cy = fret_distance / 2
            else:
                cy = self.fret.value * fret_distance
            return f"""
    <circle cx="{int(cx)}" cy="{int(cy)}" r="{int(circle_radius)}" fill="{fill_color}" stroke="{self.get_stroke_color()}" stroke-width="3"/>"""

    def __eq__(self, other: GuitarPosition):
        assert_typing(other, GuitarPosition)
        return isinstance(other, GuitarPosition) and self.fret == other.fret and self.string == other.string

    def __lt__(self, other: GuitarPosition):
        if self.get_chromatic() is None:
            return False
        if other.get_chromatic() is None:
            return True
        if self.get_chromatic() == other.get_chromatic():
            return self.string < other.string
        return self.get_chromatic() < other.get_chromatic()
    
    def __le__(self, other: GuitarPosition):
        return self == other or self<other

    def __hash__(self):
        return hash((self.fret, self.string))

    def __repr__(self):
        return f"{self.__class__.__name__}(string={self.string}, fret={self.fret})"
    
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
        from .set_of_guitar_positions import SetOfGuitarPositions
        return SetOfGuitarPositions(frozenset({self})).svg()