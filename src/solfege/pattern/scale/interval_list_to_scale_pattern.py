from typing import ClassVar, Type

from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns


class ChromaticIntervalListToScalePattern(ChromaticIntervalListToPatterns[ScalePattern]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ScalePattern

class IntervalListToScalePattern(IntervalListToPatterns[ScalePattern]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ScalePattern
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToScalePattern.make()