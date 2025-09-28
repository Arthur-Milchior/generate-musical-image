from typing import ClassVar, List, Type
from solfege.pattern.interval_list_to_pattern import IntervalListToPattern
from solfege.pattern.inversion.chromatic_interval_list_to_inversion_pattern import ChromaticIntervalListToInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.recording.singleton_container import SameKeyBehavior, SingletonContainer
from utils.util import assert_typing


class IntervalListToInversionPattern(IntervalListToPattern[InversionPattern]):
    """Associate to each interval list (assumed to be in base octave) all corresponding inversions.
    
    The recorded value has a copy of the interval list.
    """

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = InversionPattern
    _recorded_container_type: ClassVar[Type] = SingletonContainer
    _chromatic_recorded_container_type: ClassVar[Type] = SingletonContainer

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave()
    
    @classmethod
    def _new_container(self, key: IntervalList) -> List[InversionPattern]:
        assert_typing(key, IntervalList)
        return SingletonContainer[InversionPattern](SameKeyBehavior.MINIMUM)
    
    #pragma mark - IntervalListToPattern

    @classmethod
    def make_chromatic_record_keeper(cls):
        return ChromaticIntervalListToInversionPattern.make()