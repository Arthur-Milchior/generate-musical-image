from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
from typing import List
from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.chord_utils import enumerate_fretted_instrument_chords
from instruments.fretted_instrument.chord.open.chromatic_identical_inversion_to_chords_on_fretted_instrument import ChromaticIdenticalInversionToItsOpenChords
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from instruments.fretted_instrument.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.inversion.chromatic_identical_inversions import ChromaticIdenticalInversions
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.util import assert_typing, ensure_folder, img_tag, save_file

def open_folder(instrument: FrettedInstrument):
    path = f"{instrument.generated_folder_name()}/chord/open"
    ensure_folder(path)
    return path


interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()

def register_all_chords(instrument: FrettedInstrument):
    chromatic_identical_inversion_to_chords = ChromaticIdenticalInversionToItsOpenChords.make(instrument=instrument)
    for fretted_instrument_chord in enumerate_fretted_instrument_chords(instrument, Frets.make(
        closed_fret_interval=(1, 
                              6
                              ),
        allow_not_played=True, 
        allow_open=True)):
        if fretted_instrument_chord.number_of_distinct_notes() < 4:
            continue
        if fretted_instrument_chord.has_not_played_in_middle():
            continue
        if fretted_instrument_chord.playable(instrument) != Playable.EASY:
            continue
        if fretted_instrument_chord.chord_pattern_is_redundant():
            continue
        if not fretted_instrument_chord.is_open():
            continue
        chromatic_notes = fretted_instrument_chord.chromatic_notes()
        min_chromatic_note = min(chromatic_notes)
        chromatic_intervals_in_base_octave = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        # if chromatic_intervals is None:
        #     # should not 
        #     continue
        assert_typing(chromatic_notes, ChromaticNoteList)
        assert_typing(chromatic_intervals_in_base_octave, ChromaticIntervalListPattern)
        assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)
        chromatic_identical_inversion_pattern = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals_in_base_octave)
        if chromatic_identical_inversion_pattern is None:
            continue
        chromatic_identical_inversion = ChromaticIdenticalInversions(chromatic_identical_inversion_pattern, min_chromatic_note.in_base_octave())
        chromatic_identical_inversion_to_chords.register(chromatic_identical_inversion, fretted_instrument_chord)
    return chromatic_identical_inversion_to_chords


def generate_anki_notes(instrument: FrettedInstrument):
    chromatic_identical_inversion_to_chords = register_all_chords(instrument)
    chord_anki_notes: List[str] = []
    decomposition_anki_notes: List[str] = []
    folder_path = open_folder(instrument)
    instrument_folder_path = open_folder(instrument)
    chromatic_identical_inversion_and_its_open_chordss = [chromatic_identical_inversion_and_its_open_chords for chromatic_identical_inversion, chromatic_identical_inversion_and_its_open_chords in chromatic_identical_inversion_to_chords]
    chromatic_identical_inversion_and_its_open_chordss.sort(key = lambda chromatic_identical_inversion_and_its_open_chords: chromatic_identical_inversion_and_its_open_chords.easy_key())
    for chromatic_identical_inversion_and_its_open_chords in chromatic_identical_inversion_and_its_open_chordss:
        chord_anki_notes.append(chromatic_identical_inversion_and_its_open_chords.csv(instrument_folder_path))
        chord_decompositions = chromatic_identical_inversion_and_its_open_chords.decompositions()
        for chord_decomposition in chord_decompositions:
            decomposition_anki_notes.append(chord_decomposition.csv(folder_path))
    return chord_anki_notes, decomposition_anki_notes

def generate_instruments():
    for instrument in fretted_instruments:
        register_all_chords(instrument)
        anki_notes, chord_decompositions = generate_anki_notes(instrument)
        save_file(f"{open_folder(instrument)}/anki_open_chords.csv", "\n".join(anki_notes))
        save_file(f"{open_folder(instrument)}/anki_decomposition.csv", "\n".join(chord_decompositions))

generate_instruments()