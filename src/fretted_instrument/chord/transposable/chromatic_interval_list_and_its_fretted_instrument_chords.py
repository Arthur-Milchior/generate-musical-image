
from dataclasses import dataclass
from typing import ClassVar
from fretted_instrument.chord.chromatic_list_and_its_fretted_instrument_chords import ChromaticListAndItsFrettedInstrumentChords
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.util import img_tag


@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIntervalListAndItsFrettedInstrumentChords(ChromaticListAndItsFrettedInstrumentChords[ChromaticInterval]):
    """
    Csv is:
    name, other name, open ("), for chord (1, 2, 3, 4, 5, 6, 7, remaining): (the chord black, chord colored, partition)
    """
    open: ClassVar[bool] = False
    absolute: ClassVar[bool] = False
    
    def chord_pattern_name(self):
        return self.interval_and_its_inversions.easiest_name()

    def alternative_chord_pattern_names(self):
        return self.interval_and_its_inversions.alternative_names()
    
    def lily_field(self, *arg, **kwargs) -> str:
        return ""