from typing import ClassVar, List, Type

from solfege.pattern.scale.chromatic_interval_list_to_scale_pattern import ChromaticIntervalListToScalePattern
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_pattern import IntervalListToPattern
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.recording.singleton_container import SameKeyBehavior, SingletonContainer

class IntervalListToScalePattern(IntervalListToPattern[ScalePattern]):
    """The record keeper backing `ScalePattern`: maps an exact interval list to the (at most one, see
    `SameKeyBehavior.IMPOSSIBLE` below) `ScalePattern` with that shape, pairing it with a chromatic-only
    companion (`ChromaticIntervalListToScalePattern`, see `make_chromatic_record_keeper`)."""
    #pragma mark - RecordKeeper
    _recorded_type: ClassVar[Type] = ScalePattern
    """Same as RecordedType."""

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        """Only interval lists within one octave (the last note may land exactly on the octave) are valid
        scale shapes."""
        return key.is_in_base_octave(accepting_octave=True)

    @classmethod
    def _new_container(self, key: IntervalList) -> SingletonContainer[ScalePattern]:
        """A fresh `SingletonContainer` for `key` that raises if a second, different scale is registered under
        the exact same interval list (`SameKeyBehavior.IMPOSSIBLE`) -- see ../README.md's "Uniqueness" section."""
        return SingletonContainer[ScalePattern](same_key_behavior=SameKeyBehavior.IMPOSSIBLE)

    #pragma mark - IntervalListToPatterns
    @classmethod
    def make_chromatic_record_keeper(self):
        """Build the companion `ChromaticIntervalListToScalePattern`."""
        return ChromaticIntervalListToScalePattern.make()
    
