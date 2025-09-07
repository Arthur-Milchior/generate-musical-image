from typing import ClassVar, List, Type
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList
from utils.util import assert_typing


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
    
    def register(self, key: IntervalList, recorded: InversionPattern):
        key.assert_in_base_octave()
        super().register(key, recorded)
    

def get_chromatic_intervals_and_inversions(chromatic_interval_list: ChromaticIntervalList):
    assert_typing(chromatic_interval_list, ChromaticIntervalList)
    chromatic_interval_list.assert_in_base_octave()
    interval_list_to_inversion: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
    assert_typing(interval_list_to_inversion, IntervalListToInversionPattern)
    chromatic_intervals_and_inversions = interval_list_to_inversion.get_from_chromatic_interval_list(chromatic_interval_list)
    assert_typing(chromatic_intervals_and_inversions, ChromaticIntervalListAndItsInversions)
    return chromatic_intervals_and_inversions