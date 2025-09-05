from typing import ClassVar, List, Type
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.list import IntervalList


class ChromaticIntervalListToInversion(ChromaticIntervalListToPatterns[InversionPattern, ChromaticIntervalListAndItsInversions]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsInversions
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[InversionPattern]:
        return ChromaticIntervalListAndItsInversions(key)

class IntervalListToInversionPattern(IntervalListToPatterns[InversionPattern, list, ChromaticIntervalListAndItsInversions]):
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsInversions
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToInversion.make()
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[InversionPattern]:
        return list()