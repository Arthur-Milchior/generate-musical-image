import traceback
from typing import Dict, Iterator, Union
from solfege.note.chromatic import ChromaticNote
from saxophone.buttons import *
from solfege.note import Note

FINGERING_A = "A"
FINGERING_B = "B"
FINGERING_C = "C"
FINGERING_D = "D"
FINGERING_DK = "DK"
FINGERING_I = "I"
FINGERING_K_COMPLETELY_EXPOSED = "K*"
FINGERING_K_PARTIALLY_EXPOSED = "K"
FINGERING_N_COMPLETLY_EXPOSED = "N*"
FINGERING_N_PARTIALLY_EXPOSED = "N"
FINGERING_P = "P"
FINGERING_S = "S"
FINGERING_T = "T"
FINGERING_TB = "TB"
FINGERING_TK = "TK"
FINGERING_TH = "TH"
FINGERING_TW = "TW"
FINGERING_V = "V"
FINGERING_VB = "VB"
FINGERING_2 = "2"
FINGERING_5 = "5"
FINGERING_6 = "6"
FINGERING_RASCHER = "rascher"

COMPLETLY_EXPOSED = "Completly exposed"
PARTIALLY_EXPOSED = "Partially exposed"
HIDDEN = "hidden"
RASCHER_exposed = "Rascher"

#n, k, b, p, a
#n, k

exposure = {
    FINGERING_A: COMPLETLY_EXPOSED,
    FINGERING_B: COMPLETLY_EXPOSED,
    FINGERING_C: PARTIALLY_EXPOSED,
    FINGERING_D: PARTIALLY_EXPOSED,
    FINGERING_DK: PARTIALLY_EXPOSED,
    FINGERING_I: PARTIALLY_EXPOSED,
    FINGERING_K_COMPLETELY_EXPOSED: COMPLETLY_EXPOSED,
    FINGERING_K_PARTIALLY_EXPOSED: PARTIALLY_EXPOSED,
    FINGERING_N_COMPLETLY_EXPOSED: COMPLETLY_EXPOSED,
    FINGERING_N_PARTIALLY_EXPOSED: PARTIALLY_EXPOSED,
    FINGERING_P: COMPLETLY_EXPOSED,
    FINGERING_S: PARTIALLY_EXPOSED,
    FINGERING_T: PARTIALLY_EXPOSED,
    FINGERING_TB: PARTIALLY_EXPOSED,
    FINGERING_TK: PARTIALLY_EXPOSED,
    FINGERING_TH: PARTIALLY_EXPOSED,
    FINGERING_TW: PARTIALLY_EXPOSED,
    FINGERING_V: PARTIALLY_EXPOSED,
    FINGERING_VB: PARTIALLY_EXPOSED,
    FINGERING_2: COMPLETLY_EXPOSED,
    FINGERING_5: COMPLETLY_EXPOSED,
    FINGERING_6: COMPLETLY_EXPOSED,
    FINGERING_RASCHER: RASCHER_exposed,
}

D_DESCRIPTION = "Drop fingering"

symbols_to_description = {
    FINGERING_A: "Alternate fingering",
    FINGERING_C: "cross fingering",
    FINGERING_D: D_DESCRIPTION,
    FINGERING_DK: D_DESCRIPTION,
    FINGERING_N_COMPLETLY_EXPOSED: "Normal",
    FINGERING_N_PARTIALLY_EXPOSED: "Normal",
    FINGERING_P: "For piano",
    FINGERING_S: "Slide",
    FINGERING_T: "Trill",
    FINGERING_TB: "Trill",
    FINGERING_TK: "Trill",
    FINGERING_TH: "Trill from lower half-tone",
    FINGERING_TW: "Trill from lower tone",
    FINGERING_V: "Velocity",
    FINGERING_VB: "Velocity",
}

fingering_symbols = {
    FINGERING_A: "Alternate fingering",
    FINGERING_B: "Use the B key on top of Bis",
    FINGERING_C: "cross fingering",
    FINGERING_D: "Drop fingering. Used principally in fast passage to drop from a note a half-tone or whole-tone higher and return to it",
    FINGERING_DK: "Drop from a key fingering",
    FINGERING_I: "Fingering for Bb or A# using the index finger of each hand",
    FINGERING_K_COMPLETELY_EXPOSED: "Fingering using the key, full exposure",
    FINGERING_K_PARTIALLY_EXPOSED: "Fingering using the key, partial exposure",
    FINGERING_N_COMPLETLY_EXPOSED: "Normal fingering, full exposure",
    FINGERING_N_PARTIALLY_EXPOSED: "Normal fingering, partial exposure",
    FINGERING_P: "Fingering to play a note piano",
    FINGERING_S: "slide with the left or right finger",
    FINGERING_T: "Trill fingering, for trills and certain fast passages",
    FINGERING_TB: "Trill fingering involving the ue of bis key",
    FINGERING_TK: "Trill fingering involving the ue of side key",
    FINGERING_TH: "Trill fingering froma note a half-tone lower",
    FINGERING_TW: "Trill fingering froma note a whole-tone lower",
    FINGERING_V: "veloticity fingering, for use only in very fast passage",
    FINGERING_VB: "velocity fingeirng involving the use of the bis key",
    FINGERING_2: "Special fingering for G# using key 2",
    FINGERING_5: "Special fingering for G# using key 5",
    FINGERING_6: "Special fingering for G# using key 6",
    FINGERING_RASCHER: "Fingering from Rascher book. Playing using harmonics"
}


class Fingering(ChromaticNote):
    def __init__(self, chromatic_note_description: Union[str, int], buttons: Iterator[SaxophoneButton], fingering_symbol: str = FINGERING_N_COMPLETLY_EXPOSED, *, authors: Union[None, str, Iterator[str]] = None, test: bool = False):
        self.stack = traceback.format_stack(limit= 5)
        assert fingering_symbol in fingering_symbols
        self._buttons = frozenset(buttons)
        self.sorted_buttons = list(buttons)
        self.sorted_buttons.sort()
        self.fingering_symbol = fingering_symbol
        self.added_to_some_fingerings = False
        if isinstance(authors, str):
            authors = frozenset({authors})
        self.authors = authors
        if isinstance(chromatic_note_description, str):
            name: str = chromatic_note_description
            note = Note(name)
            value = note.get_chromatic().value
        else:
            assert isinstance(chromatic_note_description, int)
            value = chromatic_note_description
        fingerings_with_same_value = value_to_fingering.get(value, list())
        assert isinstance(fingerings_with_same_value, list) 
        if not test:
            fingerings_with_same_value.append(self)
        value_to_fingering[value] = fingerings_with_same_value
        super().__init__(value)

    def buttons(self):
        """Returns buttons in order from lowest to highest"""
        return self.sorted_buttons
    
    def  __repr__(self):
        return f"""Fingering(value={self.get_name_with_octave()}, buttons={", ".join(str(button) for button in self.buttons())}, fingering_symbol={self.fingering_symbol})"""

    def __eq__(self, other: "Fingering"):
        assert isinstance(other, Fingering), f"""Comparing {other} to a fingering"""
        return self._buttons == other._buttons and super().__eq__(other)
    
    def __hash__(self):
        return hash((super().__hash__(), self._buttons))
    
    def _add_buttons_interval(self, interval: int, *args):
        buttons = list(args)
        last = buttons[-1]
        if isinstance (last, str):
            fingering_symbol = last
            buttons.pop()
        else:
            fingering_symbol = FINGERING_N_COMPLETLY_EXPOSED
        for button in buttons:
            assert button not in self._buttons, f"{button}, {self}"
            assert isinstance(button, SaxophoneButton), button
        return self.__class__(chromatic_note_description =self.value + interval, buttons = self._buttons | frozenset(buttons), authors = self.authors, fingering_symbol=fingering_symbol)        

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
        pressed = "\n  ".join( button.svg(selected=True) for button in self.buttons())
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

from . import k, cn, overtone, rascher, main_column
