from enum import Enum
from typing import Dict, List, Optional, Self, Union
from fretted_instrument.chord.playable import Playable
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList
from fretted_instrument.position.set.abstract_set_of_fretted_instrument_positions import COLOR_FIFTH, COLOR_OTHER, COLOR_QUALITY, COLOR_THIRD, COLOR_TONIC, Colors, ColorsWithTonic
from fretted_instrument.position.string.string import String, StringFrozenList
from fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument
import itertools

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from utils.frozenlist import FrozenList
from utils.util import assert_optional_typing, assert_typing, optional_max

class Barred(Enum):
    NO = "NO"
    PARTIALLY = "PARTIALLY"
    FULLY = "FULLY"

class ChordColors(ColorsWithTonic):
    def get_color_from_interval(self, chromatic_interval: ChromaticInterval):
        assert_typing(chromatic_interval, ChromaticInterval)
        return [COLOR_TONIC, 
         COLOR_OTHER, COLOR_OTHER,
         COLOR_THIRD, COLOR_THIRD,
         COLOR_OTHER,
         COLOR_FIFTH, COLOR_FIFTH, COLOR_FIFTH,
         COLOR_QUALITY, COLOR_QUALITY, COLOR_QUALITY][chromatic_interval.in_base_octave().value]

class ChordOnFrettedInstrument(SetOfPositionOnFrettedInstrument):

    @classmethod
    def make(cls, instrument: FrettedInstrument, frets: List[Union[Fret, int, None]]) -> Self:
        assert len(frets) == instrument.number_of_strings()
        l = []
        for fret in frets:
            if isinstance(fret, Fret):
                l.append(fret)
            else:
                assert_optional_typing(fret, int)
                l.append(instrument.fret(fret))
        fretted_positions = [PositionOnFrettedInstrument(string, fret) for string, fret in itertools.zip_longest(instrument.strings(), l)]
        return cls(positions=PositionOnFrettedInstrumentFrozenList(fretted_positions))
    
    def get_fret(self, string: String) -> Optional[Fret]:
        """Return the note played on this string, if any."""
        assert_typing(string, String)
        fret = None
        for pos in self:
            assert_typing(pos.string, String)
            if pos.string == string:
                assert fret is None
                fret = pos.fret
        return fret if fret else Fret(None)
 
    def get_frets(self, instrument: Optional[FrettedInstrument]= None) -> List[Optional[Fret]]:
        if instrument is not None:
            return [self.get_fret(string) for string in instrument.strings()]
        frets = dict()
        max_string = 0
        for pos in self:
            string = pos.string.value
            max_string = max(max_string, string)
            assert string not in frets
            frets[string] = pos.fret
        return [frets.get(string, Fret(None)) for string in range(1, max_string+1)]

    def __repr__(self):
        return f"""FrettedInstrumentChord.make([{", ".join(str(fret.value) for fret in self.get_frets())}])"""

    def chord_pattern_is_redundant(self):
        """Whether the same fingering pattern can be played higher on the fretted_instrument"""
        return self._min_fret(allow_open=True) > Fret(1)

    def is_open(self):
        return self._min_fret(allow_open=True).is_open()
    
    def is_transposable(self):
        return not self.is_open()
    
    def is_barred(self):
        if not self.is_transposable():
            return Barred.NO
        min_closed_strings = self.strings_at_min_fret(allow_open=False)
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
    
    def hand_for_fretted_instrument(self, instrument: FrettedInstrument) -> Optional["HandForChordForFrettedInstrument"]:
        from fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
        return HandForChordForFrettedInstrument.compute_hand(instrument, self)
    
    def playable(self, instrument: FrettedInstrument) -> Playable:
        from fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
        hand: HandForChordForFrettedInstrument = self.hand_for_fretted_instrument(instrument)
        if hand is None:
            return Playable.NO
        return hand.playable()
    
    def file_name(self, instrument:FrettedInstrument, stroke_colored: bool, absolute: bool):
        if not absolute:
            transposed, transpose_interval = self.transpose_to_fret_one()
            if not transpose_interval.unison():
                return transposed.file_name(instrument, stroke_colored, absolute)            
        fret_values = [fret.value for fret in self.get_frets(instrument)]
        frets = "_".join(str(value) if value is not None else "x" for value in fret_values)
        if stroke_colored:
            return f"fretted_instrument_chord_{frets}_colored.svg"
        return f"fretted_instrument_chord_{frets}_all_black.svg"
        

intervals_in_base_octave_to_fretted_instrument_chord: Dict[ChromaticIntervalList, List[ChordOnFrettedInstrument]] = dict()

class FrettedInstrumentChordFrozenList(FrozenList[ChordOnFrettedInstrument]):
    type = ChordOnFrettedInstrument