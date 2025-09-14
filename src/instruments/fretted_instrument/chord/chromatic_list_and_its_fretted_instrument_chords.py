
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Generic, List, Optional

from instruments.fretted_instrument.chord import chord_decomposition_anki_note
from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordColors, ChordOnFrettedInstrument, FrettedInstrumentChordFrozenList
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.pattern.inversion.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.inversion.inversion_pattern import InversionPattern, InversionPatternGetter, InversionPatternGetterType
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.recordable import RecordedContainer, RecordedType
from utils.util import assert_iterable_typing, assert_typing, img_tag

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticListAndItsFrettedInstrumentChords(InversionPatternGetter, RecordedContainer[InversionPatternGetterType], CsvGenerator, DataClassWithDefaultArgument, Generic[InversionPatternGetterType]):
    """    Csv is:
    name, other name, open, for chord (1, 2, 3, 4, 5, 6, 7, remaining): (the chord black, chord colored, partition)
    """
    instrument: FrettedInstrument
    key: InversionPatternGetterType
    fretted_instrument_chords: List[ChordOnFrettedInstrument] = field(hash=False, compare=False)
    # open: ClassVar[bool]
    # absolute: ClassVar[bool]

    #pragma mark - InversionPatternGetter

    def get_inversion_pattern(self) -> InversionPattern:
        return self.key.get_inversion_pattern()

    def append(self, fretted_instrument_chord: ChordOnFrettedInstrument):
        assert_typing(fretted_instrument_chord, ChordOnFrettedInstrument)
        expected_chromatic_intervals = self.get_inversion_pattern().chromatic_interval_lists()
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
        self.fretted_instrument_chords.sort(key=lambda fretted_instrument_chord: (fretted_instrument_chord.number_of_frets(allow_open=False), -fretted_instrument_chord.number_of_distinct_notes()))

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
        names = self.names()
        assert_iterable_typing(names, str)
        other_names = names[1:]
        return ", ".join(other_names)

    def names(self):
        return [self.name(inversion) for inversion in self.interval_and_its_inversions.inversions]
    
    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalListPattern) -> str:
        return NotImplemented
    
    def triple_field(self, folder_path: str, fretted_chord: ChordOnFrettedInstrument, chord_decompositions: List[str]):
        """Generate the svg for the `fretted_chord` and its decompositions. Add the csv for decmoposition in chord_decompositions"""
        transposed_chord, transposition = fretted_chord, 0 if self.absolute else fretted_chord.transpose_to_fret_one()
        pos_of_lowest_note = transposed_chord.get_most_grave_note()
        lowest_note = pos_of_lowest_note.get_chromatic()
        tonic = lowest_note - self.interval_and_its_inversions.easiest_inversion().position_of_lowest_interval_in_base_octave.chromatic
        cdan = ChordDecompositionAnkiNote(self.names(), transposed_chord, absolute=self.absolute, tonic=tonic)
        chord_decompositions.append(cdan.csv(folder_path = folder_path))
        return (
            img_tag(transposed_chord.save_svg(folder_path, self.instrument, colors=None, absolute=self.absolute)),
            img_tag(transposed_chord.save_svg(folder_path, self.instrument, colors=ChordColors(tonic), absolute=self.absolute)),
            self.lily_field(transposed_chord, self.interval_and_its_inversions.easiest_inversion().get_interval_list()),
        )

    def csv_content(self, folder_path: str, chord_decompositions: List[str]):
        l = []
        l.append(self.first_name())
        l.append(self.other_names())
        l.append("x" if self.open else "")
        maximals = self.maximals()
        individual_maximals, other_maximals = maximals[:7], maximals[7:]
        for fretted_chord in individual_maximals:
            l += self.triple_field(folder_path, fretted_chord, chord_decompositions)
        for _ in range(7- len(maximals)):
            l.append("")
            l.append("")
            l.append("")

        # Remaining maximals
        triples = [self.triple_field(folder_path, fretted_chord, chord_decompositions) for fretted_chord in other_maximals]
        l.append(", ".join(blacks for blacks, _, _ in triples))
        l.append(", ".join(colored for _, colored, _ in triples))
        l.append(", ".join(partition for _, _, partition in triples) if self.absolute else "")
        return l
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["fretted_instrument_chords"] = list()
        return default

    def __post_init__(self):
        assert_typing(self.fretted_instrument_chords, list)
        assert_iterable_typing(self.fretted_instrument_chords, ChordOnFrettedInstrument)
        super().__post_init__()