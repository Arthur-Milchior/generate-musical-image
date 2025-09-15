from typing import ClassVar, List, Type
from solfege.pattern.inversion.identical_inversion_patterns import IdentiticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from utils.util import assert_typing


class ChromaticIntervalListToInversion(ChromaticIntervalListToPatterns[InversionPattern, IdentiticalInversionPatterns]):
    """Associate to each interval list (assumed to be in base octave) all corresponding inversions.
    
    The recorded value has a copy of the interval list.
    """

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = IdentiticalInversionPatterns

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: IntervalListPattern) -> List[InversionPattern]:
        return IdentiticalInversionPatterns(key)