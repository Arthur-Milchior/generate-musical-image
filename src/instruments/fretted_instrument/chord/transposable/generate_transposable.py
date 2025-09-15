from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.chord.transposable.inversion_pattern_to_chords_on_fretted_instrument import ChordPatternToChordsOnFrettedInstrument, ChromaticIntervalListToFrettedInstrumentChords
from instruments.fretted_instrument.chord.chord_utils import enumerate_fretted_instrument_chords
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.inversion.interval_list_to_identical_inversion_patterns import IntervalListToIdenticalInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from consts import generate_root_folder
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from utils.util import assert_typing, ensure_folder, save_file

def transposable_folder(instrument: FrettedInstrument):
    path = f"{instrument.generated_folder_name()}/chord/transposable"
    ensure_folder(path)
    return path

def register_all_chords(instrument: FrettedInstrument) -> ChordPatternToChordsOnFrettedInstrument:
    interval_to_chord = ChordPatternToChordsOnFrettedInstrument.make(instrument=instrument)
    for fretted_instrument_chord in enumerate_fretted_instrument_chords(instrument, Frets.make(closed_fret_interval=(1, 
                                                                                              4
                                                                                              ), allow_not_played=True, allow_open=False)):
        if fretted_instrument_chord.number_of_distinct_notes() < 4:
            continue
        if fretted_instrument_chord.has_not_played_in_middle():
            continue
        if fretted_instrument_chord.playable(instrument) != Playable.EASY:
            continue
        if fretted_instrument_chord.chord_pattern_is_redundant():
            continue
        chromatic_intervals = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        if chromatic_intervals is None:
            continue
        assert_typing(chromatic_intervals, ChromaticIntervalListPattern)
        interval_to_inversion_patterns: IntervalListToIdenticalInversionPattern = InversionPattern.get_record_keeper()
        assert_typing(interval_to_inversion_patterns, IntervalListToIdenticalInversionPattern)
        chromatic_intervals_and_inversions = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals)
        if chromatic_intervals_and_inversions is None:
            continue
        interval_to_chord.register(chromatic_intervals, fretted_instrument_chord)
    return interval_to_chord


def generate_anki_notes(instrument: FrettedInstrument):
    interval_to_chord = register_all_chords(instrument)
    chords_anki_notes = []
    chord_decomposition_anki_notes = []
    folder_path = transposable_folder(instrument)
    for interval_list, chromatic_interval_and_its_fretted_instrument_chord in interval_to_chord:
        chords_anki_notes.append(chromatic_interval_and_its_fretted_instrument_chord.csv(folder_path, chord_decomposition_anki_notes))
    return chords_anki_notes, chord_decomposition_anki_notes, interval_to_chord

for instrument in fretted_instruments:
    register_all_chords(instrument)
    anki_notes, chord_decomposition_anki_notes, interval_to_chord = generate_anki_notes(instrument)
    save_file(f"{transposable_folder(instrument)}/anki_chords.csv", "\n".join(anki_notes))
    save_file(f"{transposable_folder(instrument)}/anki_chord_decomposition.csv", "\n".join(chord_decomposition_anki_notes))

    biggest_anki_note = max((anki_note_content for interval_list, anki_note_content in interval_to_chord), 
                            key=lambda anki_note_content: len(anki_note_content.maximals()))
    print(f"=====================\n{instrument.name}, transposable chord\n===============================")
    print(f"{len(biggest_anki_note)=}")
    print(f"{biggest_anki_note=}")