
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cache
from typing import ClassVar, Generic, List, Type

from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument, FrettedInstrumentChordFrozenList
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.black_only import BlackOnly
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_for_interval import FrettedPositionMakerForInterval
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatternsGetter, IdenticalInversionPatternsGetterType, IdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import ClassWithEasyness
from utils.recordable import RecordedContainer, RecordedType
from utils.util import T, assert_iterable_typing, assert_typing, img_tag

@dataclass(frozen=True, unsafe_hash=True)
class AbstractIdenticalInversionAndItsFrettedInstrumentChords(RecordedContainer[ChordOnFrettedInstrument], CsvGenerator, DataClassWithDefaultArgument, ClassWithEasyness, ABC, Generic[IdenticalInversionPatternsGetterType]):
    """    Csv is:
    name, other names, open, for chord (1, 2, 3, 4, 5, 6, 7, remaining): (the chord black, chord colored, partition)
    """
    instrument: FrettedInstrument
    key: IdenticalInversionPatternsGetterType
    fretted_instrument_chords: List[ChordOnFrettedInstrument] = field(hash=False, compare=False, default_factory=list)

    #pragma mark - InversionPatternGetter

    def get_identical_inversion_pattern(self) -> IdenticalInversionPatterns:
        return self.key.get_identical_inversion_pattern()

    def append(self, fretted_instrument_chord: ChordOnFrettedInstrument):
        assert_typing(fretted_instrument_chord, ChordOnFrettedInstrument)
        expected_chromatic_intervals = self.get_identical_inversion_pattern().easiest_inversion().get_interval_list().get_chromatic_interval_list()
        actual_chromatic_intervals = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        assert expected_chromatic_intervals == actual_chromatic_intervals, f"""{expected_chromatic_intervals}\n!=\n{actual_chromatic_intervals}"""
        assert fretted_instrument_chord not in self.fretted_instrument_chords
        self.fretted_instrument_chords.append(fretted_instrument_chord)
        self.fretted_instrument_chords.sort(key = lambda chord: chord.easy_key())

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
    
    def decompositions(self):
        """Return ChordDecompositionAnkiNote for all maximal chords sorted by easyness"""
        return sorted([
            ChordDecompositionAnkiNote(self.instrument, self.key, chord)
            for chord in self.maximals()
        ], key=lambda decomposition: decomposition.easy_key())

    def all_fretted_instrument_chords(self):
        return FrettedInstrumentChordFrozenList(self.fretted_instrument_chords)
    
    def __iter__(self):
        self.sort()
        yield from self.fretted_instrument_chords

    # Used for anki:

    def __len__(self):
        return len(self.fretted_instrument_chords)
    
    def first_name(self):
        return self.names()[0]
    
    def other_names(self):
        names = self.names()
        assert_iterable_typing(names, str)
        other_names = names[1:]
        return ", ".join(other_names)

    @cache
    def names(self):
        return [name for inversion in self.get_identical_inversion_pattern().inversion_patterns for name in self.names_from_inversion(inversion)]
    
    def plain_and_numbered_field(self, folder_path: str, fretted_chord: ChordOnFrettedInstrument):
        """Generate the svg for the `fretted_chord` and its decompositions. Add the csv for decomposition in chord_decompositions"""
        transposed_chord, transposition = fretted_chord, 0 if self.absolute else fretted_chord.transpose_to_fret_one()
        pos_of_lowest_note = transposed_chord.get_most_grave_note()
        chromatic_lowest_note = pos_of_lowest_note.get_chromatic()
        easiest_inversion_pattern = self.key.get_identical_inversion_pattern().easiest_inversion()
        lowest_note = easiest_inversion_pattern.get_interval_list().best_enharmonic_starting_note(chromatic_lowest_note)
        tonic = easiest_inversion_pattern.get_tonic(lowest_note)
        chromatic_tonic = tonic.get_chromatic().in_base_octave()
        return (
            img_tag(transposed_chord.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=BlackOnly(), absolute=self.absolute)),
            img_tag(transposed_chord.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=FrettedPositionMakerForInterval.make(tonic=chromatic_tonic, pattern=easiest_inversion_pattern.base), absolute=self.absolute)),
            #self.lily_field(transposed_chord, self.key.get_identical_inversion_pattern().easiest_inversion().get_interval_list()),
        )
    
    #pragma mark - ClassWithEasyness

    def easy_key(self):
        return (self.key.easy_key(), self.fretted_instrument_chords[0].easy_key())

    #Pragma mark - CsvGenerator

    def csv_content(self, folder_path: str):
        yield self.first_name()
        yield self.other_names()
        yield self.instrument.get_name()
        yield "x" if self.absolute else ""
        maximals = self.maximals()
        individual_maximals, other_maximals = maximals[:7], maximals[7:]
        for fretted_chord in individual_maximals:
            yield from self.plain_and_numbered_field(folder_path, fretted_chord)
        nb_empty = 7- len(maximals)
        yield from [""] * (2 * nb_empty)
        # Remaining maximals
        triples = [self.plain_and_numbered_field(folder_path, fretted_chord) for fretted_chord in other_maximals]
        yield ", ".join(blacks for blacks, _ in triples)
        yield ", ".join(colored for _, colored in triples)
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["fretted_instrument_chords"] = list()
        return default

    def __post_init__(self):
        assert_typing(self.key, self.identical_inversion_pattern_getter_type)
        assert_typing(self.fretted_instrument_chords, list)
        assert_iterable_typing(self.fretted_instrument_chords, ChordOnFrettedInstrument)
        super().__post_init__()

    # Must be implemented by subclasses

    """Same As IdenticalInversionPatternsGetterType"""
    identical_inversion_pattern_getter_type: ClassVar[Type[IdenticalInversionPatternsGetter]]
    absolute: ClassVar[bool]

    @abstractmethod
    def names_from_inversion(self, inversion: InversionPattern) -> List[str]:...

    @abstractmethod
    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalListPattern) -> str:...
    # The anki field for the partition if any.
        