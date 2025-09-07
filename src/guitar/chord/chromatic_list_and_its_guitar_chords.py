
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List

from guitar.chord.guitar_chord import GuitarChord
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.value.chromatic import ChromaticType
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.recordable import RecordedContainer
from utils.util import assert_iterable_typing, assert_typing, img_tag

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticListAndItsGuitarChords(RecordedContainer[GuitarChord], CsvGenerator, Generic[ChromaticType], DataClassWithDefaultArgument):
    interval_and_its_inversions: ChromaticIntervalListAndItsInversions
    guitar_chords: List[GuitarChord] = field(hash=False, compare=False)

    @classmethod
    def _default_arguments_for_constructor(cls):
        kwargs = super()._default_arguments_for_constructor()
        kwargs["guitar_chords"] = list()
        return kwargs

    def __post_init__(self):
        assert_typing(self.interval_and_its_inversions, ChromaticIntervalListAndItsInversions)
        assert_typing(self.guitar_chords, list)
        assert_iterable_typing(self.guitar_chords, GuitarChord)
        super().__post_init__()

    def append(self, guitar_chord: GuitarChord):
        expected_chromatic_intervals = self.interval_and_its_inversions.chromatic_intervals
        actual_chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave()
        assert expected_chromatic_intervals == actual_chromatic_intervals, f"""{expected_chromatic_intervals}\n!=\n{actual_chromatic_intervals}"""
        self.guitar_chords.append(guitar_chord)

    def is_smaller_than_known_chord(self, small_chord: GuitarChord):
        for big_chord in self.guitar_chords:
            if small_chord < big_chord:
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