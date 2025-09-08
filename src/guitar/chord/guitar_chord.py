from enum import Enum
from typing import Dict, List, Optional, Self, Union
from guitar.chord.playable import Playable
from guitar.position.fret.fret import Fret
from guitar.position.guitar_position import GuitarPosition
from guitar.position.string.string import String, strings
from guitar.position.set.set_of_guitar_positions import SetOfGuitarPositions
import itertools

from solfege.value.interval.set.interval_list import ChromaticIntervalList
from utils.util import assert_typing, optional_max

class Barred(Enum):
    NO = "NO"
    PARTIALLY = "PARTIALLY"
    FULLY = "FULLY"

class GuitarChord(SetOfGuitarPositions):
    @classmethod
    def make(cls, frets: List[Union[Fret, int, None]]) -> Self:
        assert len(frets) == len(strings)
        frets = [Fret.make(fret) for fret in frets]
        guitar_positions = [GuitarPosition(string, fret) for string, fret in itertools.zip_longest(strings, frets)]
        return cls(frozenset(guitar_positions))
    
    def get_fret(self, string: String):
        assert_typing(string, String)
        fret = None
        for pos in self:
            assert_typing(pos.string, String)
            if pos.string == string:
                assert fret is None
                fret = pos.fret
        return fret
    
    def get_frets(self):
        return [self.get_fret(string) for string in strings]
    
    def __repr__(self):
        return f"""GuitarChord.make([{", ".join(str(fret.value) for fret in self.get_frets())}])"""

    def chord_pattern_is_redundant(self):
        """Whether the same fingering pattern can be played higher on the guitar"""
        return self._min_fret(include_open=True) > Fret(1)

    def is_open(self):
        return self._min_fret(include_open=True).is_open()
    
    def is_transposable(self):
        return not self.is_open()
    
    def is_barred(self):
        if not self.is_transposable():
            return Barred.NO
        min_closed_strings = self.strings_at_min_fret(include_open=False)
        assert min_closed_strings
        if len(min_closed_strings) == 1:
            # Single closed string on this fret, so no need to bar.
            return Barred.NO
        # Let's consider partially barred.
        open_strings = self.open_strings()
        if not open_strings:
            return Barred.FULLY
        max_open_string = max(open_strings)
        min_closed_stirng = min(min_closed_stirng)
        if min_closed_stirng <= max_open_string:
            # some open string would be covered by the bar if we did it.
            return Barred.NO
        return Barred.FULLY
    
    def has_not_played_in_middle(self):
        # Status can be not_played_start, then played, then not_played_end
        played_encountered = False
        not_played_after_played_encountered = False
        for fret in self.get_frets():
            if fret.is_not_played():
                if played_encountered:
                    not_played_after_played_encountered = True
            else:
                played_encountered = True
                if not_played_after_played_encountered:
                    return True
        return False
    
    def hand_for_guitar(self) -> Optional["HandForGuitardChord"]:
        from guitar.chord.hand_for_chord import HandForGuitarChord
        return HandForGuitarChord.make(self)
    
    def playable(self) -> Playable:
        from guitar.chord.hand_for_chord import HandForGuitarChord
        hand: HandForGuitarChord = self.hand_for_guitar()
        if hand is None:
            return Playable.NO
        return hand.playable()
    
    def file_name(self, stroke_colored: bool):
        fret_values = [fret.value for fret in self.get_frets()]
        frets = "_".join(str(value) if value is not None else "x" for value in fret_values)
        if stroke_colored:
            return f"guitar_chord_{frets}_colored.svg"
        return f"guitar_chord_{frets}_all_black.svg"
        

intervals_in_base_octave_to_guitar_chord: Dict[ChromaticIntervalList, List[GuitarChord]] = dict()