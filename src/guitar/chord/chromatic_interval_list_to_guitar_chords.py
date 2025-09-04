from dataclasses import dataclass
from typing import ClassVar, Type

from guitar.chord.chromatic_interval_list_and_its_guitar_chords import ChromaticIntervalListAndItsGuitarChords
from guitar.chord.guitar_chord import GuitarChord
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalsAndItsInversions
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.list import ChromaticIntervalList
from utils.recordable import RecordKeeper


class ChromaticIntervalListToGuitarChord(RecordKeeper[ChromaticIntervalList, GuitarChord, ChromaticIntervalListAndItsGuitarChords]):
    _pattern_type: ClassVar[Type] = GuitarChord
    _pattern_with_chromatic_interval_type: ClassVar[Type] = ChromaticIntervalListAndItsGuitarChords
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = GuitarChord
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIntervalList
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsGuitarChords
    
    def newPatternWithChromaticIntervalListList(self, chromatic_interval: ChromaticIntervalList) -> ChromaticIntervalListAndItsGuitarChords:
        return ChromaticIntervalListAndItsGuitarChords(chromatic_interval)

    @classmethod
    def maybe_register(cls, guitar_chord: GuitarChord):
        """Register the chord if it's playable and a chord."""
        if not guitar_chord.is_playable():
            return
        chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave()
        chromatic_intervals_and_inversions = ChromaticIntervalsAndItsInversions.chromatic_interval_to_patterns.get(chromatic_intervals)
        if chromatic_intervals_and_inversions is None:
            return
        cls.register(guitar_chord)