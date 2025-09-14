from typing import ClassVar, List, Type

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chord.chromatic_interval_list_to_chord_pattern import ChromaticIntervalListToChordPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList


class IntervalListToChordPattern(IntervalListToPatterns["ChordPattern", List, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordPattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = list

    def is_key_valid(self, key: IntervalList):
        return key.is_in_base_octave()
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToChordPattern.make()
    
    @classmethod
    def _new_container(self, key: ChromaticIntervalList) -> List[ChordPattern]:
        return list()