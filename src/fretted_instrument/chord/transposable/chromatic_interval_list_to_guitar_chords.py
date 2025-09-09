from dataclasses import dataclass
from typing import ClassVar, Type

from fretted_instrument.chord.transposable.chromatic_interval_list_and_its_guitar_chords import ChromaticIntervalListAndItsGuitarChords
from fretted_instrument.chord.guitar_chord import GuitarChord
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.interval_list_to_inversion_pattern import ChromaticIntervalListToInversion, IntervalListToInversionPattern, get_chromatic_intervals_and_inversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from utils.recordable import RecordKeeper
from utils.util import assert_typing


class ChromaticIntervalListToGuitarChords(RecordKeeper[ChromaticIntervalList, GuitarChord, ChromaticIntervalListAndItsGuitarChords]):
    _pattern_type: ClassVar[Type] = GuitarChord
    _pattern_with_chromatic_interval_type: ClassVar[Type] = ChromaticIntervalListAndItsGuitarChords
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = GuitarChord
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIntervalList
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsGuitarChords

    def _new_container(self, chromatic_interval_list: ChromaticIntervalList) -> ChromaticIntervalListAndItsGuitarChords:
        chromatic_intervals_and_inversions = get_chromatic_intervals_and_inversions(chromatic_interval_list)
        assert_typing(chromatic_intervals_and_inversions, ChromaticIntervalListAndItsInversions)
        return ChromaticIntervalListAndItsGuitarChords.make(chromatic_intervals_and_inversions)