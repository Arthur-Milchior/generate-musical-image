from dataclasses import dataclass
from typing import Optional, Self, Tuple, Union

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.frozenlist import FrozenList, MakeableWithSingleArgument
from utils.util import assert_typing
from instruments.fretted_instrument.position.consts import *


@dataclass(frozen=True)
class String(MakeableWithSingleArgument):
    """Represents one of the string of the FrettedInstrument."""

    value: int
    """The note when the string is played empty."""
    note_open: ChromaticNote

    def add(self, instrument: FrettedInstrument, other: int) -> Optional[Self]:
        assert_typing(other, int)
        new_string_value = self.value + other
        if new_string_value < 1:
            return None
        if new_string_value > instrument.number_of_strings():
            return None
        return instrument.string(new_string_value)
    
    def __sub__(self, other: int):
        return self + (-other)
    
    def fret_for_note(self, instrument: FrettedInstrument, note: ChromaticNote) -> Optional[Fret]:
        """The fret to play `note` on `self`. None if it can't be done withing the limit of the instrument."""
        assert_typing(instrument, FrettedInstrument)
        assert_typing(note, ChromaticNote)
        if note < self.note_open:
            return None
        interval = note-self.note_open
        fret = instrument.fret(interval.value)
        if fret > instrument.last_fret():
            return None
        return fret
    
    def position_for_note(self, instrument: FrettedInstrument, note:ChromaticNote):
        """The position to play `note` on `self`. None if it can't be done on `instrument`."""
        from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
        fret = self.fret_for_note(instrument, note)
        if fret is None:
            return None
        return PositionOnFrettedInstrument(self, fret)
    
    def __lt__(self, other: "String"):
        return self.value < other.value
    
    def __le__(self, other: "String"):
        return self.value <= other.value
    
    def __eq__(self, other: "String"):
        assert_typing(other, String)
        return self.value == other.value and self.note_open == other.note_open
    
    def __repr__(self):
        return f"String[{self.value}]"
    
    def x(self):
        return MARGIN + (self.value-1) * DISTANCE_BETWEEN_STRING
    
    def svg(self, lowest_fret: Fret, show_open_fret: bool):
        """
        The svg to display current string.
        If `show_open_fret`, a margin at the top represents the top of the board.
        Otherwise the fret goes over the entire height.
        The fret ends below `lowest_fret` so that it also cover the margin at the bottom.
        """
        assert_typing(lowest_fret, Fret)
        y1 = int(MARGIN) if show_open_fret else 0
        y2 = int(lowest_fret.y_fret()+MARGIN)
        x = int(self.x())
        return f"""<line x1="{self.x()}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="{STRING_THICKNESS}" stroke="black" /><!-- String {self.value}-->"""

    #pragma mark - MakeableWithSingleArgument

    def repr_single_argument(self) -> str:
        return f"""{self.value}"""
    
    @staticmethod
    def _make_single_argument(arg: Tuple[FrettedInstrument, int]):
        instrument, string = arg
        assert_typing(instrument, FrettedInstrument)
        assert_typing(string, int)
        return instrument.string(string)

    #pragma mark - MakeableWithSingleArgument
    
    def __post_init__(self):
        assert_typing(self.value, int)
        assert_typing(self.note_open, ChromaticNote)


# ukulele_G4 = String(1, Note.from_name("G4").get_chromatic())
# ukulele_C4 = String(2, Note.from_name("C4").get_chromatic())
# ukulele_E4 = String(3, Note.from_name("E4").get_chromatic())
# ukulele_A4 = String(4, Note.from_name("A4").get_chromatic())
    
# bass_E2 = String(1, Note.from_name("E2").get_chromatic())
# bass_A2 = String(2, Note.from_name("A2").get_chromatic())
# bass_D3 = String(3, Note.from_name("D3").get_chromatic())
# bass_G3 = String(4, Note.from_name("G3").get_chromatic())

# fretted_instrument_E3 = String(1, Note.from_name("E3").get_chromatic())
# fretted_instrument_A3 = String(2, Note.from_name("A3").get_chromatic())
# fretted_instrument_D4 = String(3, Note.from_name("D4").get_chromatic())
# fretted_instrument_G4 = String(4, Note.from_name("G4").get_chromatic())
# fretted_instrument_B4 = String(5, Note.from_name("B4").get_chromatic())
# fretted_instrument_E5 = String(6, Note.from_name("E5").get_chromatic())

class StringFrozenList(FrozenList[String]):
    type = String