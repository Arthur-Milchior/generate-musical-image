from typing import ClassVar, List, Type
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern
from utils.recording.singleton_container import SameKeyBehavior, SingletonContainer
from utils.util import assert_typing


class ChromaticIntervalListToInversionPattern(ChromaticIntervalListToPatterns[InversionPattern]):
    """Associate to each interval list (assumed to be in base octave) all corresponding inversions.
    
    The recorded value has a copy of the interval list.
    """

    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = InversionPattern
    """Same as RecordedType."""
    _recorded_container_type: ClassVar[Type] = SingletonContainer
    """Same as RecordedContainerType."""

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        """Only interval lists strictly within one octave are valid chord/inversion shapes."""
        return key.is_in_base_octave()

    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[InversionPattern]:
        """A fresh `SingletonContainer` for `key` that keeps the easiest (`SameKeyBehavior.MINIMUM`) inversion
        when several are registered under the same chromatic-only shape."""
        assert_typing(key, ChromaticIntervalListPattern)
        return SingletonContainer[InversionPattern](SameKeyBehavior.MINIMUM)