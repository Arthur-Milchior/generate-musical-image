from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Iterator, Union
from solfege.value.note.chromatic_note import ChromaticNote
from saxophone.buttons import *
from solfege.value.note.note import Note
from utils.util import assert_typing

class FingeringSymbol(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    DK = "DK"
    I = "I"
    K_COMPLETELY_EXPOSED = "K*"
    K_PARTIALLY_EXPOSED = "K"
    N_COMPLETLY_EXPOSED = "N*"
    N_PARTIALLY_EXPOSED = "N"
    P = "P"
    S = "S"
    T = "T"
    TB = "TB"
    TK = "TK"
    TH = "TH"
    TW = "TW"
    V = "V"
    VB = "VB"
    TWO = "2"
    FIVE = "5"
    SIX = "6"
    RASCHER = "rascher"

COMPLETLY_EXPOSED = "Completly exposed"
PARTIALLY_EXPOSED = "Partially exposed"
HIDDEN = "hidden"
RASCHER_exposed = "Rascher"

#n, k, b, p, a
#n, k

exposure = {
    FingeringSymbol.A: COMPLETLY_EXPOSED,
    FingeringSymbol.B: COMPLETLY_EXPOSED,
    FingeringSymbol.C: PARTIALLY_EXPOSED,
    FingeringSymbol.D: PARTIALLY_EXPOSED,
    FingeringSymbol.DK: PARTIALLY_EXPOSED,
    FingeringSymbol.I: PARTIALLY_EXPOSED,
    FingeringSymbol.K_COMPLETELY_EXPOSED: COMPLETLY_EXPOSED,
    FingeringSymbol.K_PARTIALLY_EXPOSED: PARTIALLY_EXPOSED,
    FingeringSymbol.N_COMPLETLY_EXPOSED: COMPLETLY_EXPOSED,
    FingeringSymbol.N_PARTIALLY_EXPOSED: PARTIALLY_EXPOSED,
    FingeringSymbol.P: COMPLETLY_EXPOSED,
    FingeringSymbol.S: PARTIALLY_EXPOSED,
    FingeringSymbol.T: PARTIALLY_EXPOSED,
    FingeringSymbol.TB: PARTIALLY_EXPOSED,
    FingeringSymbol.TK: PARTIALLY_EXPOSED,
    FingeringSymbol.TH: PARTIALLY_EXPOSED,
    FingeringSymbol.TW: PARTIALLY_EXPOSED,
    FingeringSymbol.V: PARTIALLY_EXPOSED,
    FingeringSymbol.VB: PARTIALLY_EXPOSED,
    FingeringSymbol.TWO: COMPLETLY_EXPOSED,
    FingeringSymbol.FIVE: COMPLETLY_EXPOSED,
    FingeringSymbol.SIX: COMPLETLY_EXPOSED,
    FingeringSymbol.RASCHER: RASCHER_exposed,
}

D_DESCRIPTION = "Drop fingering"

symbols_to_description = {
    FingeringSymbol.A: "Alternate fingering",
    FingeringSymbol.C: "cross fingering",
    FingeringSymbol.D: D_DESCRIPTION,
    FingeringSymbol.DK: D_DESCRIPTION,
    FingeringSymbol.N_COMPLETLY_EXPOSED: "Normal",
    FingeringSymbol.N_PARTIALLY_EXPOSED: "Normal",
    FingeringSymbol.P: "For piano",
    FingeringSymbol.S: "Slide",
    FingeringSymbol.T: "Trill",
    FingeringSymbol.TB: "Trill",
    FingeringSymbol.TK: "Trill",
    FingeringSymbol.TH: "Trill from lower half-tone",
    FingeringSymbol.TW: "Trill from lower tone",
    FingeringSymbol.V: "Velocity",
    FingeringSymbol.VB: "Velocity",
}

fingering_symbols = {
    FingeringSymbol.A: "Alternate fingering",
    FingeringSymbol.B: "Use the B key on top of Bis",
    FingeringSymbol.C: "cross fingering",
    FingeringSymbol.D: "Drop fingering. Used principally in fast passage to drop from a note a half-tone or whole-tone higher and return to it",
    FingeringSymbol.DK: "Drop from a key fingering",
    FingeringSymbol.I: "Fingering for Bb or A# using the index finger of each hand",
    FingeringSymbol.K_COMPLETELY_EXPOSED: "Fingering using the key, full exposure",
    FingeringSymbol.K_PARTIALLY_EXPOSED: "Fingering using the key, partial exposure",
    FingeringSymbol.N_COMPLETLY_EXPOSED: "Normal fingering, full exposure",
    FingeringSymbol.N_PARTIALLY_EXPOSED: "Normal fingering, partial exposure",
    FingeringSymbol.P: "Fingering to play a note piano",
    FingeringSymbol.S: "slide with the left or right finger",
    FingeringSymbol.T: "Trill fingering, for trills and certain fast passages",
    FingeringSymbol.TB: "Trill fingering involving the ue of bis key",
    FingeringSymbol.TK: "Trill fingering involving the ue of side key",
    FingeringSymbol.TH: "Trill fingering froma note a half-tone lower",
    FingeringSymbol.TW: "Trill fingering froma note a whole-tone lower",
    FingeringSymbol.V: "veloticity fingering, for use only in very fast passage",
    FingeringSymbol.VB: "velocity fingeirng involving the use of the bis key",
    FingeringSymbol.TWO: "Special fingering for G# using key 2",
    FingeringSymbol.FIVE: "Special fingering for G# using key 5",
    FingeringSymbol.SIX: "Special fingering for G# using key 6",
    FingeringSymbol.RASCHER: "Fingering from Rascher book. Playing using harmonics"
}


@dataclass(frozen=True)
class Fingering(ChromaticNote):
    buttons: frozenset[SaxophoneButton]
    authors: frozenset[str]
    fingering_symbol: str
    test: bool
    """The list of fingerings to which it's added"""
    fingerings: List

    @classmethod
    def make(cls, 
            chromatic_note_description: Union[str, int], 
            buttons: Iterable[SaxophoneButton],
            fingering_symbol: str = FingeringSymbol.N_COMPLETLY_EXPOSED,
            *, 
            authors: Union[None, str, Iterator[str]] = None, 
            test: bool = False) -> Self:
        buttons = frozenset(list(sorted(buttons)))
        if authors is None:
            authors = {}
        if isinstance(authors, str):
            authors = {authors}
        authors = frozenset(authors)
        if isinstance(chromatic_note_description, str):
            name: str = chromatic_note_description
            note = Note.from_name(name)
            value = note.get_chromatic().value
        else:
            assert_typing(chromatic_note_description, int)
            value = chromatic_note_description
        return cls(buttons = buttons, fingering_symbol=fingering_symbol, authors = authors, test= test, value = value, fingerings=[])

    def __post_init__(self):
        super().__post_init__()
        assert_typing(self.buttons, frozenset)
        for button in self.buttons:
            assert_typing(button, SaxophoneButton)
        if self.test:
            return
        # only register this fingering if we're not doing a test.
        if self.value not in value_to_fingering:
            value_to_fingering[self.value] = []
        value_to_fingering[self.value].append(self)
    
    def  __repr__(self):
        return f"""Fingering.make(value={self.get_name_with_octave()}, buttons={", ".join(str(button) for button in self.buttons)}, fingering_symbol={self.fingering_symbol})"""

    def __eq__(self, other: "Fingering"):
        assert isinstance(other, Fingering), f"""Comparing {other} to a fingering"""
        return self.buttons == other.buttons and super().__eq__(other)
    
    def __hash__(self):
        return hash((super().__hash__(), self.buttons))
    
    def _add_buttons_interval(self, interval: int, *args):
        buttons = list(args)
        last = buttons[-1]
        if isinstance (last, FingeringSymbol):
            fingering_symbol = last
            buttons.pop()
        else:
            fingering_symbol = FingeringSymbol.N_COMPLETLY_EXPOSED
        for button in buttons:
            assert button not in self.buttons, f"{button}, {self}"
            assert_typing(button, SaxophoneButton)
        return self.__class__.make(chromatic_note_description =self.value + interval, buttons = self.buttons | frozenset(buttons), authors = self.authors, fingering_symbol=fingering_symbol)        

    def add_octave(self, fingering_symbol: Optional[str] = None) -> "Fingering":
        if fingering_symbol is None:
            fingering_symbol = self.fingering_symbol
        return self._add_buttons_interval(12, octave, fingering_symbol)
    
    def add_semi_tone(self, *args) -> "Fingering":
        return self._add_buttons_interval(1, *args)
    
    def remove_semi_tone(self, *args) -> "Fingering":
        return self._add_buttons_interval(-1, *args)

    def silent_button(self, *args) -> "Fingering":
        return self._add_buttons_interval(0, *args)
    
    def add_tone(self, *args) -> "Fingering":
        return self._add_buttons_interval(2, *args)
    
    def remove_tone(self, *args) -> "Fingering":
        return self._add_buttons_interval(-2, *args)
    
    def svg(self) -> str:
        empty = "\n  ".join( button.svg(selected=False) for button in buttons)
        pressed = "\n  ".join( button.svg(selected=True) for button in self.buttons)
        return f"""<svg version="1.1" width="75" height="153" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="white" />
  {empty}
  {pressed}
</svg>"""
    
    def anki_comment(self):
        exp = exposure[self.fingering_symbol]
        desc = symbols_to_description.get(self.fingering_symbol, None)
        if desc:
            return f"""{desc}; {exp}"""
        return exp

value_to_fingering: Dict[int, List[Fingering]] = dict()

from saxophone.fingering import k, cn, overtone, rascher, main_column
