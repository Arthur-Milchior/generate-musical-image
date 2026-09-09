from typing import ClassVar, List, Type

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chord.chromatic_interval_list_to_chord_pattern import ChromaticIntervalListToChordPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_pattern import IntervalListToPattern
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList


class IntervalListToChordPattern(IntervalListToPattern["ChordPattern"]):
    """The record keeper backing `ChordPattern`: maps an exact interval list (root position or any inversion,
    fifth included or omitted) to the `ChordPattern`(s) sharing it, pairing it with a chromatic-only
    companion (`ChromaticIntervalListToChordPattern`, see `make_chromatic_record_keeper`)."""
    #pragma mark - RecordKeeper

    _recorded_type: ClassVar[Type] = ChordPattern
    """Same as RecordedType."""
    _recorded_container_type: ClassVar[Type] = list
    """Same as RecordedContainerType."""
    _chromatic_recorded_container_type: ClassVar[Type] = list
    """The container type used by the chromatic-only companion record keeper (see `make_chromatic_record_keeper`)."""

    def is_key_valid(self, key: IntervalList):
        """Only interval lists strictly within one octave are valid chord shapes."""
        return key.is_in_base_octave()

    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[ChordPattern]:
        """A fresh, empty container for `key`."""
        return list()

    #pragma mark - IntervalListToPatterns
    @classmethod
    def make_chromatic_record_keeper(self):
        """Build the companion `ChromaticIntervalListToChordPattern`."""
        return ChromaticIntervalListToChordPattern.make()
