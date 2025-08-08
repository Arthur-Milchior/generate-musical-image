from __future__ import annotations

from typing import Optional

from solfege.interval import ChromaticInterval
from solfege.note import ChromaticNote

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
HIGHEST_FRET = 24

class GuitarPosition:
    """A position on the guitar, that is, a string and a fret.
    Fret 0 is open. Fret None is not played.

    Order is the same as its chromatic note, and in case of equality the string. Not played notes is maximal. This ensure that the minimal of a chord is its lowest note."""
    string: int
    fret: Optional[int]

    def __init__(self, string: int, fret: Optional[int], **kwargs):
        assert isinstance(string, int)
        assert 1 <= string <= 6
        super().__init__(**kwargs)
        self.string = string
        self.fret = fret
        if fret is not None:
            assert isinstance(fret, int)
            assert 0 <= fret <= HIGHEST_FRET  # Usually there are at most 24 frets on guitar

    @classmethod
    def from_chromatic(cl, chromatic: ChromaticInterval) -> GuitarPosition:
        string = 1
        for i in range(2,7):
            if string_number_to_note_played_when_free[i] < chromatic:
                string = i
            else:
                break
        fret = chromatic - string_number_to_note_played_when_free[string]
        return cl(string=string, fret=fret.value)

    def get_chromatic(self) -> Optional[ChromaticNote]:
        if self.fret is None:
            return None
        return string_number_to_note_played_when_free[self.string] + ChromaticInterval(self.fret)

    def get_stroke_color(self):
        return "black"

    def svg(self):
        """Draw this position, assuming that f already contains the svg for the fret"""
        fill_color = "white" if self.fret is 0 else "black"
        cx = string_distance * (self.string - 0.5)
        if self.fret is None:
            return f"""
    <text x="{int(cx)}" y="{int(fret_distance / 3)}" font-size="30">x</text>"""
        else:
            if self.fret == 0:
                cy = fret_distance / 2
            else:
                cy = self.fret * fret_distance
            return f"""
    <circle cx="{int(cx)}" cy="{int(cy)}" r="{int(circle_radius)}" fill="{fill_color}" stroke="{self.get_stroke_color()}" stroke-width="3"/>"""

    def __eq__(self, other: GuitarPosition):
        return self.fret == other.fret and self.string == other.string

    def __lt__(self, other: GuitarPosition):
        if self.fret == other.fret == None:
            return self.string < other.string
        if self.fret is not None and other.fret is None:
            return True
        if self.fret is None and other.fret is not None:
            return False

        if self.get_chromatic() < other.get_chromatic():
            return True
        if self.get_chromatic() > other.get_chromatic():
            return False
        return self.string < other.string

    def __le__(self, other: GuitarPosition):
        return self == other or self < other

    def __hash__(self):
        return hash((self.fret, self.string))

    def __repr__(self):
        return f"{self.__class__.__name__}(string={self.string}, fret={self.fret})"
    
    def __sub__(self, other: GuitarPosition) -> ChromaticInterval:
        assert isinstance(other, GuitarPosition)
        return self.get_chromatic() - other.get_chromatic()
    
    def __add__(self, other: ChromaticInterval):
        assert isinstance(other, ChromaticInterval)
        return self.add(other)

    def add(self, interval, min=0, max=5):
        """A pos, equal to self, with `interval`  semitone added

        fret is minimal in [min,max]. If no such pos exists, return None

        interval -- a chromatic interval
        """
        chromaticResult = self.get_chromatic() + interval
        assert isinstance(chromaticResult, ChromaticNote)
        max_string = None
        for string, chromatic_note in string_number_to_note_played_when_free.items():
            if min <= (chromaticResult - chromatic_note).get_number() <= max:
                if (max_string is None) or (string > max_string):
                    max_string = string
        if max_string:
            return GuitarPosition(max_string, (chromaticResult - string_number_to_note_played_when_free[max_string]).get_number())
        else:
            return None
