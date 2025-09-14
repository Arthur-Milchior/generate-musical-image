

from typing import ClassVar, List, Type
from solfege.pattern.inversion.chromatic_interval_list_to_inversion_pattern import ChromaticIntervalListToInversion
from solfege.pattern.inversion.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern


class IntervalListToInversionPattern(IntervalListToPatterns[InversionPattern, list, ChromaticIntervalListAndItsInversions]):
    """Associate to each interval list all inversions that are related."""


    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = list
    _chromatic_recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsInversions

    def is_key_valid(self, key: IntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def make_chromatic_container(self):
        return ChromaticIntervalListToInversion.make()
    
    @classmethod
    def _new_container(self, key: IntervalListPattern) -> List[InversionPattern]:
        return list()