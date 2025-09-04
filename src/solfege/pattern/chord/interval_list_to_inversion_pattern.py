from typing import ClassVar, Type
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns


class ChromaticIntervalListToInversion(ChromaticIntervalListToPatterns[InversionPattern]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = InversionPattern

class IntervalListToInversion(IntervalListToPatterns[InversionPattern]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = InversionPattern
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToInversion.make()