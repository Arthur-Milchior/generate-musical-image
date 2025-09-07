from typing import ClassVar, List, Type

from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList


class ChromaticIntervalListToScalePattern(ChromaticIntervalListToPatterns[ScalePattern, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ScalePattern
    _recorded_container_type: ClassVar[Type] = list
    
    @classmethod
    def _new_container(self, key: ChromaticIntervalList) -> List[ScalePattern]:
        return list()

class IntervalListToScalePattern(IntervalListToPatterns[ScalePattern, List, List]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ScalePattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = list
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToScalePattern.make()
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[ScalePattern]:
        return list()
    
    def register(self, key: IntervalList, recorded: ScalePattern):
        key.assert_in_base_octave(accepting_octave=True)
        super().register(key, recorded)