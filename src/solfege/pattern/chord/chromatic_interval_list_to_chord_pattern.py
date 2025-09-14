

from typing import ClassVar, List, Type
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern


class ChromaticIntervalListToChordPattern(ChromaticIntervalListToPatterns[ChordPattern, List]):
    """Associate to each Chromatic interval list the Chord it represents. The list sohuld contain at most one chord.
    It's returned as a list only for compatibliity with the api."""


    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordPattern
    _recorded_container_type: ClassVar[Type] = list

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[ChordPattern]:
        return list()
    
    def get_chord(self, chromatic_interval_list: ChromaticIntervalListPattern):
        patterns = self.get_recorded_container(chromatic_interval_list)
        if patterns:
            assert len(patterns == 1)
            return patterns[0]
        return None