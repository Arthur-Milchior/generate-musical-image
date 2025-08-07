from __future__ import annotations

import unittest
from typing import Optional

from solfege.interval import ChromaticInterval
from solfege.note import ChromaticNote

# The 1-th string played free
string_number_to_note_played_when_free = {
    1: ChromaticNote(chromatic=-8),
    2: ChromaticNote(chromatic=-3),
    3: ChromaticNote(chromatic=2),
    4: ChromaticNote(chromatic=7),
    5: ChromaticNote(chromatic=11),
    6: ChromaticNote(chromatic=16),
}

# Constants used in SVG
fret_distance = 50
string_distance = 30
circle_radius = 11


class GuitarPosition:
    """A position on the guitar, that is, a string and a fret.
    Fret 0 is open. Fret None is not played.

    Lexicographical order by string and fret. A non played string is less than a played string."""
    string: int
    fret: Optional[int]

    def __init__(self, string: int, fret: Optional[int]):
        super().__init__(string=string, fret=fret)
        assert isinstance(string, int)
        assert 1 <= string <= 6
        if fret is not None:
            assert isinstance(fret, int)
            assert 0 <= fret <= 24  # Usually there are at most 24 frets on guitar

    def get_chromatic(self) -> Optional[ChromaticNote]:
        if self.fret is None:
            return None
        return ChromaticNote(value=string_number_to_note_played_when_free[self.string] + ChromaticInterval(self.fret))

    def get_stroke_color(self):
        return "black"

    def svg(self):
        """Draw this position, assuming that f already contains the svg for the fret"""
        fill_color = "white" if self.fret is 0 else "black"
        cx = string_distance * (self.string - 0.5)
        if self.fret is None:
            return f"""
    <text x="{cx:d}" y="{fret_distance / 3:d}" font-size="30">x</text>"""
        else:
            if self.fret == 0:
                cy = fret_distance / 2
            else:
                cy = self.fret * fret_distance
            return f"""
    <circle cx="{cx:d}" cy="{cy:d}" r="{circle_radius:d}" fill="{fill_color}" stroke="{self.get_stroke_color()}" stroke-width="3"/>"""

    def __eq__(self, other: GuitarPosition):
        return self.fret == other.fret and self.string == other.fret

    def __lt__(self, other: GuitarPosition):
        if self.string < other.string:
            return True
        if self.string > other.string:
            return True
        if self.fret is None:
            return other.fret is not None
        if other.fret is None:
            return False
        return self.fret < other.fret

    def __le__(self, other: GuitarPosition):
        return self == other or self < other

