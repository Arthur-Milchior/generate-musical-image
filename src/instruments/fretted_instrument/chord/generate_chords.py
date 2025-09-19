from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
from typing import Callable, Dict, Generic, List, Optional, Type
from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.chord_utils import enumerate_fretted_instrument_chords
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.open.chromatic_identical_inversion_pattern_with_note_and_its_transposable_chords import ChromaticIdenticalInversionAndItsOpenChords
from instruments.fretted_instrument.chord.open.chromatic_identical_inversion_to_chords_on_fretted_instrument import ChromaticIdenticalInversionToItsOpenChords
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.chord.transposable.chromatic_inversion_pattern_to_chords_on_fretted_instrument import ChromaticIdenticalInversionPatternToItsTransposableChords
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar, fretted_instruments
from instruments.fretted_instrument.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import MinimalChordDecompositionInput
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.inversion.chromatic_identical_inversions import ChromaticIdenticalInversions
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.recordable import KeyType, RecordKeeper, RecordedContainerType, RecordedType
from utils.util import assert_typing, ensure_folder, img_tag, save_file


interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)
@dataclass(frozen=True)
class AnkiNotesPreparation(DataClassWithDefaultArgument):
    open_chord: bool
    instrument: FrettedInstrument
    record_keeper: RecordKeeper[ChromaticIdenticalInversions, ChordOnFrettedInstrument, ChromaticIdenticalInversionAndItsOpenChords]
    decompositions: List[ChordDecompositionAnkiNote]

    def __hash__(self):
        # Not expected to be needed.
        return 0

    def min_fret(self):
        return 1

    def max_fret(self):
        #return 2
        return 6 if self.open_chord else 4
    
    def recorded_container_getter(self, pattern: IdenticalInversionPatterns, note: ChromaticNote) ->MinimalChordDecompositionInput:
        return ChromaticIdenticalInversions(pattern, note) if self.open_chord else pattern
    
    def subfolder_name(self):
        return "open" if self.open_chord else "transposable"

    def folder_name(self):
        path = f"{self.instrument.generated_folder_name()}/chord/{self.subfolder_name()}"
        ensure_folder(path)
        return path

    def register_all_chords(self):
        frets = Frets.make(
            closed_fret_interval=(self.min_fret(), self.max_fret()),
            allow_not_played=True, 
            allow_open=self.open_chord,
            absolute = self.open_chord
            )
        for fretted_instrument_chord in enumerate_fretted_instrument_chords(self.instrument, frets):
            if fretted_instrument_chord.number_of_distinct_notes() < 4:
                continue
            if fretted_instrument_chord.has_not_played_in_middle():
                continue
            if fretted_instrument_chord.playable(self.instrument) != Playable.EASY:
                continue
            if fretted_instrument_chord.chord_pattern_is_redundant():
                continue
            if fretted_instrument_chord.is_open() != self.open_chord:
                continue
            chromatic_notes = fretted_instrument_chord.chromatic_notes()
            min_chromatic_note = min(chromatic_notes)
            chromatic_intervals_in_base_octave = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
            # if chromatic_intervals is None:
            #     # should not 
            #     continue
            assert_typing(chromatic_notes, ChromaticNoteList)
            assert_typing(chromatic_intervals_in_base_octave, ChromaticIntervalListPattern)
            chromatic_identical_inversion_pattern: Optional[IdenticalInversionPatterns] = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals_in_base_octave)
            if chromatic_identical_inversion_pattern is None:
                continue
            chromatic_identical_inversion = self.recorded_container_getter(chromatic_identical_inversion_pattern, min_chromatic_note.in_base_octave())
            self.record_keeper.register(key=chromatic_identical_inversion, recorded=fretted_instrument_chord)
        return self.record_keeper
    
    def register_decompositions(self):
        for chromatic_identical_inversion_and_its_open_chords in self.anki_note_containers():
            chord_decompositions = chromatic_identical_inversion_and_its_open_chords.decompositions()
            for chord_decomposition in chord_decompositions:
                self.decompositions.append(chord_decomposition)

    def anki_note_containers(self) -> List[CsvGenerator]:
        return [chromatic_identical_inversion_and_its_open_chords for chromatic_identical_inversion, chromatic_identical_inversion_and_its_open_chords in self.record_keeper]

    #pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "open_chord")
        open_chord = kwargs["open_chord"]
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        instrument = kwargs["instrument"]
        kwargs["record_keeper"] = ChromaticIdenticalInversionToItsOpenChords.make(instrument=instrument) if open_chord else ChromaticIdenticalInversionPatternToItsTransposableChords.make(instrument=instrument)
        kwargs["decompositions"] = list()
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        super().__post_init__()
        self.register_all_chords()
        self.register_decompositions()

def generate_instrument(instrument: FrettedInstrument):
    open_chord = AnkiNotesPreparation.make(open_chord=True, instrument=instrument)
    transposable = AnkiNotesPreparation.make(open_chord=False, instrument=instrument)
    folder_path = f"{instrument.generated_folder_name()}/chord"

    # decompositions
    decompositions: List[ChordDecompositionAnkiNote] = open_chord.decompositions + transposable.decompositions
    decompositions.sort(key = lambda decomposition: decomposition.easy_key())
    anki_note_container_csv = "\n".join(decomposition.csv(folder_path=folder_path) for decomposition in decompositions)
    save_file(f"{folder_path}/decomposition.csv", anki_note_container_csv)

    #note containers
    anki_note_containers = open_chord.anki_note_containers() + transposable.anki_note_containers()
    anki_note_containers.sort(key = lambda anki_note_container: anki_note_container.easy_key())
    anki_note_container_csv = "\n".join(anki_note_container.csv(folder_path=folder_path) for anki_note_container in anki_note_containers)
    save_file(f"{instrument.generated_folder_name()}/chord/equivalent_chords.csv", anki_note_container_csv)

def generate_instruments():
    for instrument in fretted_instruments:
        generate_instrument(instrument)

generate_instruments()