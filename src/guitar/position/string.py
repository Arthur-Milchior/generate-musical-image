from dataclasses import dataclass
from typing import Optional, Union

from guitar.position.fret import HIGHEST_FRET, Fret
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.util import assert_typing
from guitar.position.consts import *

STRING_THICKNESS = 5

@dataclass(frozen=True)
class String:
    """Represents one of the string of the Guitar."""

    value: int
    """The note when the string is played empty."""
    note_open: ChromaticNote

    def __post_init__(self):
        assert_typing(self.value, int)
        assert_typing(self.note_open, ChromaticNote)

    @staticmethod
    def make_single_argument(string: Union["String", int]):
        if isinstance(string, String):
            return string
        assert_typing(string, int)
        return strings[string-1]

    def __add__(self, other: int):
        if self.value is None:
            return self
        value = self.value + other
        if value < 1:
            return None
        if value > 6:
            return None
        return strings[value-1]
    
    def __sub__(self, other: int):
        return self + (-other)
    
    def fret_for_note(self, note: ChromaticNote) -> Optional[Fret]:
        assert_typing(note, ChromaticNote)
        if note < self.note_open:
            return None
        interval = note-self.note_open
        fret = Fret(interval.value)
        if fret > HIGHEST_FRET:
            return None
        return fret
    
    def position_for_note(self, note:ChromaticNote):
        from guitar.position.guitar_position import GuitarPosition
        fret = self.fret_for_note(note)
        if fret is None:
            return None
        return GuitarPosition(self, fret)
    
    def __lt__(self, other: "String"):
        return self.value < other.value
    
    def __eq__(self, other: "String"):
        assert_typing(other, String)
        return self.value == other.value and self.note_open == other.note_open
    
    def __repr__(self):
        return f"strings[{self.value - 1}]"
    
    def x(self):
        return MARGIN + (self.value-1) * DISTANCE_BETWEEN_STRING
    
    def svg(self, lowest_fret: Fret, show_open_fret: bool):
        """
        The svg to display current string.
        If `show_open_fret`, a margin at the top represents the top of the board.
        Otherwise the fret goes over the entire height.
        The fret ends below `lowest_fret` so that it also cover the margin at the bottom.
        """
        y1 = int(MARGIN) if show_open_fret else 0
        y2 = int(lowest_fret.y_fret())
        x = int(self.x())
        return f"""<line x1="{self.x()}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="{STRING_THICKNESS}" stroke="black" /><!-- Fret {self.value}-->"""


        
    
String.E3 = String(1, Note.from_name("E3").get_chromatic())
String.A3 = String(2, Note.from_name("A3").get_chromatic())
String.D4 = String(3, Note.from_name("D4").get_chromatic())
String.G4 = String(4, Note.from_name("G4").get_chromatic())
String.B4 = String(5, Note.from_name("B4").get_chromatic())
String.E5 = String(6, Note.from_name("E5").get_chromatic())

strings = [String.E3, String.A3, String.D4, String.G4, String.B4, String.E5]