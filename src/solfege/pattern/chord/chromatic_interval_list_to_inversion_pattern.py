from typing import ClassVar, List, Type
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList
from utils.util import assert_typing


class ChromaticIntervalListToInversion(ChromaticIntervalListToPatterns[InversionPattern, ChromaticIntervalListAndItsInversions]):
    """Associate to each interval list (assumed to be in base octave) all corresponding inversions.
    
    The recorded value has a copy of the interval list.
    """

    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsInversions

    def is_key_valid(self, key: ChromaticIntervalList):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[InversionPattern]:
        return ChromaticIntervalListAndItsInversions(key)