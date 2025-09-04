
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

from guitar.chord.guitar_chord import GuitarChord
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from solfege.pattern.chord import inversion_pattern
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalsAndItsInversions
from solfege.value.interval.set.list import ChromaticIntervalList
from utils.recordable import RecordedContainer

@dataclass(frozen=True)
class ChromaticIntervalListAndItsGuitarChords(RecordedContainer[GuitarChord]):
    interval: ChromaticIntervalsAndItsInversions
    guitar_chords: List[GuitarChord] = field(default_factory=list)

    def append(self, guitar_chord: GuitarChord):
        assert self.interval == guitar_chord.intervals_frow_lowest_note_in_base_octave()
        self.guitar_chords.append(guitar_chord)

    # Used for anki:

    def __len__(self):
        return len(self.guitar_chords)

    def name(self):
        return self.interval.easiest_name()

    def alternative_name(self):
        return self.interval.alternative_names()