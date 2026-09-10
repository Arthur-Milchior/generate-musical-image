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
    """Same as RecordedType."""
    _recorded_container_type: ClassVar[Type] = SingletonContainer
    """Same as RecordedContainerType."""
    _chromatic_recorded_container_type: ClassVar[Type] = SingletonContainer
    """The container type used by the chromatic-only companion record keeper (see `make_chromatic_record_keeper`)."""

    def is_key_valid(self, key: ChromaticIntervalListPattern) -> bool:
        """Only interval lists strictly within one octave are valid chord/inversion shapes."""
        return key.is_in_base_octave()

    @classmethod
    def _new_container(self, key: IntervalList) -> List[InversionPattern]:
        """A fresh `SingletonContainer` for `key` that keeps the easiest (`SameKeyBehavior.MINIMUM`) inversion
        when several are registered under the same exact shape."""
        assert_typing(key, IntervalList)
        return SingletonContainer[InversionPattern](SameKeyBehavior.MINIMUM)

    #pragma mark - IntervalListToPattern

    @classmethod
    def make_chromatic_record_keeper(cls) -> ChromaticIntervalListToInversionPattern:
        """Build the companion `ChromaticIntervalListToInversionPattern`."""
        return ChromaticIntervalListToInversionPattern.make()