
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

from guitar.chord.guitar_chord import GuitarChord
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from solfege.pattern.chord import inversion_pattern
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.value.interval.set.list import ChromaticIntervalList
from utils.csv import CsvGenerator
from utils.frozenlist import FrozenList
from utils.recordable import RecordedContainer
from utils.util import assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class ChromaticIntervalListAndItsGuitarChords(RecordedContainer[GuitarChord], CsvGenerator):
    interval_and_its_inversions: ChromaticIntervalListAndItsInversions
    guitar_chords: List[GuitarChord] = field(default_factory=list)

    def __post_init__(self):
        assert_typing(self.interval_and_its_inversions, ChromaticIntervalListAndItsInversions)
        assert_typing(self.guitar_chords, list)
        assert_iterable_typing(self.guitar_chords, GuitarChord)

    def append(self, guitar_chord: GuitarChord):
        expected_chromatic_intervals = self.interval_and_its_inversions.chromatic_intervals
        actual_chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave()
        assert expected_chromatic_intervals == actual_chromatic_intervals, f"""{expected_chromatic_intervals}\n!=\n{actual_chromatic_intervals}"""
        self.guitar_chords.append(guitar_chord)

    def is_smaller_than_known_chord(self, small_chord: GuitarChord):
        for big_chord in self.guitar_chords:
            if small_chord<big_chord:
                return True
        return False

    def maximals(self) -> FrozenList[GuitarChord]:
        """Return the elements of the list that are not strictly contained in other elements of the list."""
        return FrozenList(guitar_chord for guitar_chord in self.guitar_chords if not self.is_smaller_than_known_chord(guitar_chord))

    def all_guitar_chords(self):
        return FrozenList(self.guitar_chords)
    
    def __iter__(self):
        yield from self.guitar_chords

    # Used for anki:

    def __len__(self):
        return len(self.guitar_chords)

    def name(self):
        return self.interval_and_its_inversions.easiest_name()

    def alternative_name(self):
        return self.interval_and_its_inversions.alternative_names()
    
    def csv_content(self):
        l = []
        l.append(self.name())
        l.append(self.alternative_name())
        maximals = self.maximals()
        for guitar_chord in maximals:
            l.append(guitar_chord.file_name(stroke_colored=False))
            l.append(guitar_chord.file_name(stroke_colored=True))
        for _ in range(7- len(maximals)):
            l.append("")
            l.append("")
        return l