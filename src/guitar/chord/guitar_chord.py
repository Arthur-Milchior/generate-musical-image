from typing import Dict, List, Self, Union
from guitar.position.fret import NOT_PLAYED, OPEN_FRET, Fret
from guitar.position.guitar_position import GuitarPosition
from guitar.position.string import String, strings
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
import itertools

from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.value.interval.set.list import ChromaticIntervalList
from utils.util import assert_typing

class GuitarChord(SetOfGuitarPositions):
    @classmethod
    def make(cls, frets: List[Union[Fret, int]]) -> Self:
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

    def chord_pattern_is_redundant(self):
        """Whether the same fingering pattern can be played higher on the guitar"""
        return self._min_fret() > Fret(1)

    def is_open(self):
        return self._min_fret() == OPEN_FRET
    
    def is_barred(self):
        min_fret = self._min_fret()
        if min_fret in (NOT_PLAYED, OPEN_FRET):
            return False
        return len([1 for position in self.positions if position.fret == min_fret]) > 1
    
    def is_playable(self):
        """ Whether at most 4 fingers must be used
        
        The lowest fret can be used for multiple string
        
        TODO: deal with finger on the first string.
        """
        min_fret = self._min_fret()
        if self.is_barred():
            assert min_fret not in (NOT_PLAYED, OPEN_FRET)
            return len([1 for position in self.positions if position.fret > min_fret])<=3
        return len([1 for position in self.positions if position.fret not in (OPEN_FRET, NOT_PLAYED)])<=4
        
    def get_inversions(self):
        return InversionPattern.get_patterns_from_chromatic_interval(self.intervals_frow_lowest_note_in_base_octave())

intervals_in_base_octave_to_guitar_chord: Dict[ChromaticIntervalList, List[GuitarChord]] = dict()