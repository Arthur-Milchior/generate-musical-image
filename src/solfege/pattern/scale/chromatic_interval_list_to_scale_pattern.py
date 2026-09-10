

from typing import ClassVar, List, Type
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern


class ChromaticIntervalListToScalePattern(ChromaticIntervalListToPatterns[ScalePattern]):
    """The chromatic-only record keeper companion to `IntervalListToScalePattern`."""
    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = ScalePattern
    """Same as RecordedType."""
    _recorded_container_type: ClassVar[Type] = list
    """Same as RecordedContainerType."""

    def is_key_valid(self, key: ChromaticIntervalListPattern) -> bool:
        """Only interval lists within one octave (the last note may land exactly on the octave) are valid
        scale shapes."""
        return key.is_in_base_octave(accepting_octave=True)

    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[ScalePattern]:
        """A fresh, empty container for `key`."""
        return list()