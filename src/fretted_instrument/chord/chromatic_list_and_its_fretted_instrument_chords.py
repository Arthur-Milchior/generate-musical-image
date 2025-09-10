
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional

from fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument, FrettedInstrumentChordFrozenList
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.value.chromatic import ChromaticType
from solfege.value.interval.set.interval_list import IntervalList
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.recordable import RecordedContainer
from utils.util import assert_iterable_typing, assert_typing, img_tag

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticListAndItsFrettedInstrumentChords(RecordedContainer[ChordOnFrettedInstrument], CsvGenerator, Generic[ChromaticType], DataClassWithDefaultArgument):
    """    Csv is:
    name, other name, open, for chord (1, 2, 3, 4, 5, 6, 7, remaining): (the chord black, chord colored, partition)
    """
    instrument: FrettedInstrument
    interval_and_its_inversions: ChromaticIntervalListAndItsInversions
    fretted_instrument_chords: List[ChordOnFrettedInstrument] = field(hash=False, compare=False)
    open: ClassVar[bool]
    absolute: ClassVar[bool]

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["fretted_instrument_chords"] = list()
        return default

    def __post_init__(self):
        assert_typing(self.interval_and_its_inversions, ChromaticIntervalListAndItsInversions)
        assert_typing(self.fretted_instrument_chords, list)
        assert_iterable_typing(self.fretted_instrument_chords, ChordOnFrettedInstrument)
        super().__post_init__()

    def append(self, fretted_instrument_chord: ChordOnFrettedInstrument):
        assert_typing(fretted_instrument_chord, ChordOnFrettedInstrument)
        expected_chromatic_intervals = self.interval_and_its_inversions.chromatic_intervals
        actual_chromatic_intervals = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        assert expected_chromatic_intervals == actual_chromatic_intervals, f"""{expected_chromatic_intervals}\n!=\n{actual_chromatic_intervals}"""
        self.fretted_instrument_chords.append(fretted_instrument_chord)

    def is_smaller_than_known_chord(self, small_chord: ChordOnFrettedInstrument):
        for big_chord in self.fretted_instrument_chords:
            if small_chord < big_chord:
                return True
        return False
    
    def sort(self):
        """Sort the list of chords. Starting with smallest number of frets, and in case of equality greater number of notes"""
        self.fretted_instrument_chords.sort(key=lambda fretted_instrument_chord: (fretted_instrument_chord.number_of_frets(include_open=False), -fretted_instrument_chord.number_of_distinct_notes()))

    def maximals(self) -> FrettedInstrumentChordFrozenList:
        """Return the elements of the list that are not strictly contained in other elements of the list."""
        self.sort()
        return FrettedInstrumentChordFrozenList(fretted_instrument_chord for fretted_instrument_chord in self.fretted_instrument_chords if not self.is_smaller_than_known_chord(fretted_instrument_chord))

    def all_fretted_instrument_chords(self):
        return FrettedInstrumentChordFrozenList(self.fretted_instrument_chords)
    
    def __iter__(self):
        self.sort()
        yield from self.fretted_instrument_chords

    # Used for anki:

    def __len__(self):
        return len(self.fretted_instrument_chords)
    
    def name(self, inversion: InversionPattern) -> List[str]:
        return NotImplemented
    
    def first_name(self):
        return self.names()[0]
    
    def other_names(self):
        return ", ".join(self.names()[1:])

    def chord_names(self):
        return [self.name(inversion) for inversion in self.interval_and_its_inversions.inversions]
    
    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalList) -> str:
        return NotImplemented
    
    def triple_field(self, fretted_chord: ChordOnFrettedInstrument):
        return (
            img_tag(fretted_chord.file_name(stroke_colored=False, absolute=self.absolute)),
            img_tag(fretted_chord.file_name(stroke_colored=True, absolute=True)),
            self.lily_field(fretted_chord),
        )

    
    def csv_content(self, absolute: bool, lily_folder_path: Optional[str] = None):
        l = []
        inversions = self.interval_and_its_inversions.inversions
        easiest_inversion = inversions[0]
        other_inversions = inversions[1:]
        l.append(self.first_name())
        l.append(self.other_names)
        l.append("x" if self.open else "")
        maximals = self.maximals()
        interval_list = easiest_inversion.interval_list
        individual_maximals, other_maximals = maximals[:7], maximals[7:]
        for fretted_chord in individual_maximals:
            l += self.triple_field(fretted_chord)
        for _ in range(7- len(maximals)):
            l.append("")
            l.append("")
            l.append("")

        # Remaining maximals
        triples = [self.triple_field(fretted_chord) for fretted_chord in other_maximals]
        l.append(", ".join(blacks for blacks, _, _ in triples))
        l.append(", ".join(colored for _, colored, _ in triples))
        l.append(", ".join(partition for _, _, partition in triples) if self.absolute else "")
        return l