

from typing import ClassVar, List, Type
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern


class ChromaticIntervalListToChordPattern(ChromaticIntervalListToPatterns[ChordPattern]):
    """Associate to each Chromatic interval list the Chord it represents. The list should contain at most one chord.
    It's returned as a list only for compatibility with the api."""

    #pragma mark - RecordKeeper
    _recorded_type: ClassVar[Type] = ChordPattern
    """Same as RecordedType."""
    _recorded_container_type: ClassVar[Type] = list
    """Same as RecordedContainerType."""

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        """Only interval lists strictly within one octave are valid chord shapes."""
        return key.is_in_base_octave()

    @classmethod
    def _new_container(self, key: ChromaticIntervalListPattern) -> List[ChordPattern]:
        """A fresh, empty container for `key`."""
        return list()

    # public
    def get_chord(self, chromatic_interval_list: ChromaticIntervalListPattern):
        """The single `ChordPattern` registered under `chromatic_interval_list`, or None if there is none."""
        patterns = self.get_recorded_container(chromatic_interval_list)
        if patterns:
            assert len(patterns == 1)
            return patterns[0]
        return None