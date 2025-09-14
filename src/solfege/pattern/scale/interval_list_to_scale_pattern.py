from typing import ClassVar, List, Type

from solfege.pattern.scale.chromatic_interval_list_to_scale_pattern import ChromaticIntervalListToScalePattern
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern

class IntervalListToScalePattern(IntervalListToPatterns[ScalePattern, List, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ScalePattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = list

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave(accepting_octave=True)
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToScalePattern.make()
    
    @classmethod
    def _new_container(self, key: IntervalListPattern) -> List[ScalePattern]:
        return list()