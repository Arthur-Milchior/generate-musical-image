

from typing import ClassVar, List, Type
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern


class ChromaticIntervalListToScalePattern(ChromaticIntervalListToPatterns[ScalePattern, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ScalePattern
    _recorded_container_type: ClassVar[Type] = list

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave(accepting_octave=True)
    
    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[ScalePattern]:
        return list()