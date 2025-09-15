from typing import ClassVar, List, Type
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatterns
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from utils.util import assert_typing


class ChromaticIntervalListToInversionPattern(ChromaticIntervalListToPatterns[InversionPattern, IdenticalInversionPatterns]):
    """Associate to each interval list (assumed to be in base octave) all corresponding inversions.
    
    The recorded value has a copy of the interval list.
    """

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = ChromaticIdenticalInversionPatterns

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[InversionPattern]:
        assert_typing(key, ChromaticIntervalListPattern)
        return ChromaticIdenticalInversionPatterns(key)