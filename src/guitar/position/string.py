from dataclasses import dataclass
from typing import Optional, Union

from guitar.position.fret import HIGHEST_FRET, Fret
from solfege.interval.chromatic import ChromaticInterval
from solfege.note.chromatic import ChromaticNote
from solfege.note.note import Note
from utils.util import assert_typing


@dataclass(frozen=True, eq=True)
class String:
    """Represents one of the string of the Guitar."""

    value: int
    """The note when the string is played empty."""
    note_open: ChromaticNote

    def __post_init__(self):
        assert_typing(self.value, int)
        assert_typing(self.note_open, ChromaticNote)

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
    
    def fret_for_note(self, note: ChromaticNote):
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
        
    
String.E3 = String(1, Note("E3").get_chromatic())
String.A3 = String(2, Note("A3").get_chromatic())
String.D4 = String(3, Note("D4").get_chromatic())
String.G4 = String(4, Note("G4").get_chromatic())
String.B4 = String(5, Note("B4").get_chromatic())
String.E5 = String(6, Note("E5").get_chromatic())

strings = [String.E3, String.A3, String.D4, String.G4, String.B4, String.E5]