from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
from typing import Callable, Dict, Generic, List, Optional, Type
from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.chord_utils import enumerate_fretted_instrument_chords
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.chromatic_inversion_instantiation_and_its_chords import ChromaticInversionInstantiationAndItsChords
from instruments.fretted_instrument.chord.chromatic_inversion_instantiation_to_chords import ChromaticInversionInstantiationToChords
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar, fretted_instruments
from consts import generate_root_folder
from instruments.fretted_instrument.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.inversion.chromatic_inversion_instantiation import ChromaticInversionInstantiation
from solfege.pattern_instantiation.inversion.inversion_instantiation import InversionInstantiation
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.recording.record_keeper import RecordKeeper
from utils.recording.singleton_container import SingletonContainer
from utils.util import assert_typing, ensure_folder, img_tag, save_file


interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)

lily_folder_path = f"{generate_root_folder}/lily"
ensure_folder(lily_folder_path)
@dataclass(frozen=True)
class AnkiNotesPreparation(DataClassWithDefaultArgument):
    instrument: FrettedInstrument
    record_keeper: RecordKeeper[ChromaticInversionInstantiation, ChordOnFrettedInstrument, ChromaticInversionInstantiationAndItsChords]
    decompositions: List[ChordDecompositionAnkiNote]

    def __hash__(self):
        # Not expected to be needed.
        return 0

    def min_fret(self):
        return 1

    def max_fret(self):
        return 2
        return 6 if self.open_chord else 4
    
    def recorded_container_getter(self, pattern: InversionInstantiation, chromatic_note: ChromaticNote):
        assert_typing(chromatic_note, ChromaticNote)
        return ChromaticInversionInstantiation(pattern, chromatic_note)
    
    def folder_name(self):
        path = f"{self.instrument.generated_folder_name()}/chord"
        ensure_folder(path)
        return path

    def register_all_chords(self):
        frets = Frets.make(
            closed_fret_interval=(self.min_fret(), self.max_fret()),
            allow_not_played=True, 
            allow_open=True,
            absolute = True
            )
        for fretted_instrument_chord in enumerate_fretted_instrument_chords(self.instrument, frets):
            if fretted_instrument_chord.number_of_distinct_notes() < 4:
                continue
            if fretted_instrument_chord.has_not_played_in_middle():
                continue
            if fretted_instrument_chord.playable(self.instrument) != Playable.EASY:
                continue
            # if fretted_instrument_chord.chord_pattern_is_redundant():
            #     continue
            # if fretted_instrument_chord.is_open() != self.open_chord:
            #     continue
            chromatic_notes = fretted_instrument_chord.chromatic_notes()
            min_chromatic_note: ChromaticNote = min(chromatic_notes.notes)
            chromatic_intervals_in_base_octave = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
            # if chromatic_intervals is None:
            #     # should not 
            #     continue
            assert_typing(chromatic_notes, ChromaticNoteList)
            assert_typing(chromatic_intervals_in_base_octave, ChromaticIntervalListPattern)
            inversion_pattern_container: SingletonContainer = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals_in_base_octave)
            if inversion_pattern_container is None:
                continue
            assert_typing(inversion_pattern_container, SingletonContainer)
            inversion_pattern = inversion_pattern_container.recorded_value
            assert_typing(inversion_pattern, InversionPattern)
            chromatic_inversion_instantiation = self.recorded_container_getter(pattern=inversion_pattern, chromatic_note=min_chromatic_note.in_base_octave())
            self.record_keeper.register(key=chromatic_inversion_instantiation, recorded=fretted_instrument_chord)
        return self.record_keeper
    
    def register_decompositions(self):
        for chromatic_identical_inversion_and_its_open_chords in self.anki_note_containers():
            chord_decompositions = chromatic_identical_inversion_and_its_open_chords.decompositions()
            for chord_decomposition in chord_decompositions:
                self.decompositions.append(chord_decomposition)

    def anki_note_containers(self) -> List[ChromaticInversionInstantiationAndItsChords]:
        return [chromatic_identical_inversion_and_its_open_chords for chromatic_identical_inversion, chromatic_identical_inversion_and_its_open_chords in self.record_keeper]

    #pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        instrument = kwargs["instrument"]
        kwargs["record_keeper"] = ChromaticInversionInstantiationToChords.make(instrument=instrument)
        kwargs["decompositions"] = list()
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        super().__post_init__()
        self.register_all_chords()
        self.register_decompositions()

def generate_instrument(instrument: FrettedInstrument):
    open_chord = AnkiNotesPreparation.make(instrument=instrument)
    folder_path = f"{instrument.generated_folder_name()}/chord"

    # decompositions
    decompositions: List[ChordDecompositionAnkiNote] = open_chord.decompositions
    decompositions.sort(key = lambda decomposition: decomposition.easy_key())
    anki_note_container_csv = "\n".join(decomposition.csv(folder_path=folder_path, lily_folder_path=lily_folder_path) for decomposition in decompositions)
    save_file(f"{folder_path}/decomposition.csv", anki_note_container_csv)

    #note containers
    anki_note_containers = open_chord.anki_note_containers()
    anki_note_containers.sort(key = lambda anki_note_container: anki_note_container.easy_key())
    anki_note_container_csv = "\n".join(anki_note_container.csv(folder_path=folder_path) for anki_note_container in anki_note_containers)
    save_file(f"{folder_path}/equivalent_chords.csv", anki_note_container_csv)

def generate_instruments():
    for instrument in fretted_instruments:
        generate_instrument(instrument)

generate_instruments()