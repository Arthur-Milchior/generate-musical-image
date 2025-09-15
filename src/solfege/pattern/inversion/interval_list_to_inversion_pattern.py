from typing import ClassVar, List, Type
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatterns
from solfege.pattern.inversion.chromatic_interval_list_to_inversion_pattern import ChromaticIntervalListToInversionPattern
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from utils.util import assert_typing


class IntervalListToInversionPattern(IntervalListToPatterns[InversionPattern, IdenticalInversionPatterns, ChromaticIntervalListToInversionPattern]):
    """Associate to each interval list (assumed to be in base octave) all corresponding inversions.
    
    The recorded value has a copy of the interval list.
    """

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = IdenticalInversionPatterns
    _chromatic_recorded_container_type: ClassVar[Type] = ChromaticIdenticalInversionPatterns

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: IntervalListPattern) -> List[InversionPattern]:
        assert_typing(key, IntervalListPattern)
        return IdenticalInversionPatterns(key)
    
    #pragma mark - IntervalListToPattern

    @classmethod
    def make_chromatic_record_keeper(cls):
        return ChromaticIntervalListToInversionPattern.make()