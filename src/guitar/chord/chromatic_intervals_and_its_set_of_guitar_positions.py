
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

from guitar.chord.guitar_chord import GuitarChord
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from solfege.pattern.chord import inversion_pattern
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalsAndItsInversions
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.value.interval.set.list import ChromaticIntervalList


@dataclass(frozen=True)
class ChromaticIntervalAndItsSetsOfGuitarChords:
    interval: ChromaticIntervalsAndItsInversions
    guitar_chords: List[GuitarChord] = field(default_factory=list)
    chromatic_intervals_to_self: ClassVar[Dict[ChromaticIntervalList, "ChromaticIntervalAndItsSetsOfGuitarChords"]] = dict()

    @classmethod
    def register(cls, guitar_chord: GuitarChord):
        chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave()
        if chromatic_intervals not in cls.chromatic_intervals_to_self:
            cls.chromatic_intervals_to_self[chromatic_intervals] = ChromaticIntervalAndItsSetsOfGuitarChords(chromatic_intervals)

        cls.chromatic_intervals_to_self[chromatic_intervals].guitar_chords.append(guitar_chord)

    @classmethod
    def maybe_register(cls, guitar_chord: GuitarChord):
        """Register the chord if it's playable and a chord."""
        if not guitar_chord.is_playable():
            return
        chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave
        chromatic_intervals_and_inversions = ChromaticIntervalsAndItsInversions.chromatic_interval_to_patterns.get(chromatic_intervals)
        if chromatic_intervals_and_inversions is None:
            return
        cls.register(guitar_chord)