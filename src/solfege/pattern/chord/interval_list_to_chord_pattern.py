from typing import ClassVar, Type

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns


class ChromaticIntervalListToChordPattern(ChromaticIntervalListToPatterns["ChordPattern"]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordPattern

class IntervalListToChordPattern(IntervalListToPatterns["ChordPattern"]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordPattern
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToChordPattern.make()