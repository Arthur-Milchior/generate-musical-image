from typing import ClassVar, List, Type

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chord.chromatic_interval_list_to_chord_pattern import ChromaticIntervalListToChordPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern


class IntervalListToChordPattern(IntervalListToPatterns["ChordPattern", List, List]):
    #pragma mark - RecordKeeper
    
    _recorded_type: ClassVar[Type] = ChordPattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = list

    def is_key_valid(self, key: IntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[ChordPattern]:
        return list()
    
    #pragma mark - IntervalListToPatterns
    @classmethod
    def make_chromatic_record_keeper(self):
        return ChromaticIntervalListToChordPattern.make()
