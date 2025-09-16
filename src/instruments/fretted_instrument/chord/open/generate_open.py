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
from utils.util import assert_typing, ensure_folder, save_file

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
    chord_anki_notes = []
    chord_decomposition_anki_notes = []
    instrument_folder_path = open_folder(instrument)
    for chromatic_identical_inversion, chromatic_identical_inversion_and_its_open_chords in chromatic_identical_inversion_to_chords:
        chord_anki_notes.append(chromatic_identical_inversion_and_its_open_chords.csv(instrument_folder_path, chord_decomposition_anki_notes))
    return chord_anki_notes, chord_decomposition_anki_notes, chromatic_identical_inversion_to_chords

def generate_instruments():
    for instrument in fretted_instruments:
        register_all_chords(instrument)
        anki_notes, chord_decomposition_anki_notes, note_to_chord = generate_anki_notes(instrument)
        save_file(f"{open_folder(instrument)}/anki_open_chords.csv", "\n".join(anki_notes))
        save_file(f"{open_folder(instrument)}/anki_decomposition.csv", "\n".join(chord_decomposition_anki_notes))

        biggest_anki_note = max((anki_note_content for note_list, anki_note_content in note_to_chord), 
                                key=lambda anki_note_content: len(anki_note_content.maximals()))
        print(f"=================\n{instrument.name}\n=======================")
        print(f"{len(biggest_anki_note)=}")
        print(f"{biggest_anki_note=}")

generate_instruments()