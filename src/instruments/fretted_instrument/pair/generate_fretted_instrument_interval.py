"""
generates pair on note on distinct string. Show 6 frets in the images.
Generate an anki note, with this image, and the distance between both strings, assuming one of the fret is 0
"""
from dataclasses import dataclass
from pickletools import string1
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from solfege.value.interval.chromatic_interval import IntervalNameCreasing
from utils.csv import CsvGenerator
from utils.util import *
from consts import generate_root_folder

"""
Generate an image for each pair of notes between fret 0 and LAST_FRET on distinct string.
Also a card for each note. Used for the card type "fretted_instrument interval"
"""

@dataclass(frozen=True)
class FrettedInstrumentIntervalAnkiNote(CsvGenerator):
    instrument: FrettedInstrument
    pos1: PositionOnFrettedInstrument
    pos2: PositionOnFrettedInstrument

    def __post_init__(self):
        assert_typing(self.pos1, PositionOnFrettedInstrument)
        assert_typing(self.pos2, PositionOnFrettedInstrument)
        assert self.pos1.fret.value < 2 or self.pos2.fret.value < 2
        assert self.pos1.string < self.pos2.string

    def key(self):
        return f"{self.pos1.string.value}{self.pos1.fret.value}-{self.pos2.string.value}{self.pos2.fret.value}"
    
    def svg_name(self):
        return f"{self.instrument.name}_{self.key()}.svg"
    
    def interval(self):
        return self.pos2 - self.pos1
    
    def pos_difference(self):
        v = self.pos2.fret.value - self.pos1.fret.value
        if v == 0:
            return "=0"
        if v < 0:
           return str(v)
        else:
            return f"+{v}"
        
    def difference_name(self):
        return self.interval().get_interval_name(side = IntervalNameCreasing.DECREASING_ONLY)
    
    def svg(self):
        absolute = self.pos1.fret.is_open() or self.pos2.fret.is_open()
        if not absolute:
            assert 1 in [self.pos1.fret.value, self.pos2.fret.value]
        return SetOfPositionOnFrettedInstrument(PositionOnFrettedInstrumentFrozenList({self.pos1, self.pos2}), absolute).svg(instrument=self.instrument)
    
    #pragma mark CsvGenerator
    
    def csv_content(self):
        return [
            self.key(),
            str(self.pos1.string.value),
            str(self.pos2.string.value),
            img_tag(self.svg_name()),
            self.pos_difference(),
            str(self.interval().value),
            self.difference_name(),
            self.instrument.name
        ]

def pairs_of_frets_values(last_fret: Fret):
    assert_typing(last_fret, Fret)
    return (
        [(low_fret, high_fret) for low_fret in range(0, 2) for high_fret in range(0, last_fret.value + 1)] +
        [(low_fret, high_fret) for low_fret in range(2, last_fret.value + 1) for high_fret in range(0, 2)]
    )
