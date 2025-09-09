from dataclasses import dataclass
from typing import Optional, Union

from fretted_instrument.fretted_instrumet import FrettedInstrument
from fretted_instrument.position.fret.fret import HIGHEST_FRET, Fret
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.frozenlist import FrozenList, MakeableWithSingleArgument
from utils.util import assert_typing
from fretted_instrument.position.consts import *

STRING_THICKNESS = 5

@dataclass(frozen=True)
class String(MakeableWithSingleArgument):
    """Represents one of the string of the Guitar."""

    value: int
    """The note when the string is played empty."""
    note_open: ChromaticNote
    instrument: FrettedInstrument

    def __post_init__(self):
        assert_typing(self.value, int)
        assert_typing(self.note_open, ChromaticNote)

    def repr_single_argument(self) -> str:
        return f"""{self.value}"""
    
    @staticmethod
    def _make_single_argument(instrument: FrettedInstrument, string: Union["String", int]):
        assert_typing(string, int)
        return instrument.strings[string-1]

    def __add__(self, other: int) -> Optional[Self]:
        assert_typing(other, int)
        new_string_value = self.value + other
        if new_string_value < 1:
            return None
        if new_string_value > self.instrument.number_of_frets():
            return None
        return self.instrument.string(new_string_value)
    
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
        from fretted_instrument.position.guitar_position import GuitarPosition
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


        
    
ukulele_G4 = String(1, Note.from_name("G4").get_chromatic())
ukulele_C4 = String(2, Note.from_name("C4").get_chromatic())
ukulele_E4 = String(3, Note.from_name("E4").get_chromatic())
ukulele_A4 = String(4, Note.from_name("A4").get_chromatic())
    
bass_E2 = String(1, Note.from_name("E2").get_chromatic())
bass_A2 = String(2, Note.from_name("A2").get_chromatic())
bass_D3 = String(3, Note.from_name("D3").get_chromatic())
bass_G3 = String(4, Note.from_name("G3").get_chromatic())

guitar_E3 = String(1, Note.from_name("E3").get_chromatic())
guitar_A3 = String(2, Note.from_name("A3").get_chromatic())
guitar_D4 = String(3, Note.from_name("D4").get_chromatic())
guitar_G4 = String(4, Note.from_name("G4").get_chromatic())
guitar_B4 = String(5, Note.from_name("B4").get_chromatic())
guitar_E5 = String(6, Note.from_name("E5").get_chromatic())

class StringFrozenList(FrozenList[String]):
    type = String