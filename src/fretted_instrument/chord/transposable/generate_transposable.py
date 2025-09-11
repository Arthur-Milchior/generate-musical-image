from fretted_instrument.chord.fretted_instrument_chord import ChordColors
from fretted_instrument.chord.transposable.chromatic_interval_list_to_fretted_instrument_chords import ChromaticIntervalListToFrettedInstrumentChords
from fretted_instrument.chord.chord_utils import enumerate_fretted_instrument_chords
from fretted_instrument.chord.playable import Playable
from fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.chord.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.chord.inversion_pattern import InversionPattern
from consts import generate_root_folder
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from utils.util import assert_typing, ensure_folder, save_file

def transposable_folder(instrument: FrettedInstrument):
    path = f"{instrument.generated_folder_name()}/chord/transposable"
    ensure_folder(path)
    return path

def register_all_chords(instrument: FrettedInstrument):
    interval_to_chord = ChromaticIntervalListToFrettedInstrumentChords.make(instrument=instrument)
    for fretted_instrument_chord in enumerate_fretted_instrument_chords(instrument, Frets.make(closed_fret_interval=(1, 
                                                                                              4
                                                                                              ), allow_not_played=True, allow_open=False)):
        if fretted_instrument_chord.number_of_distinct_notes() < 4:
            continue
        if fretted_instrument_chord.has_not_played_in_middle():
            continue
        if fretted_instrument_chord.playable() != Playable.EASY:
            continue
        if fretted_instrument_chord.chord_pattern_is_redundant():
            continue
        chromatic_intervals = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        if chromatic_intervals is None:
            continue
        assert_typing(chromatic_intervals, ChromaticIntervalList)
        interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
        assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)
        chromatic_intervals_and_inversions = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals)
        if chromatic_intervals_and_inversions is None:
            continue
        interval_to_chord.register(chromatic_intervals, fretted_instrument_chord)
    return interval_to_chord


def generate_anki_notes(instrument: FrettedInstrument):
    interval_to_chord = register_all_chords(instrument)
    anki_notes = []
    for interval_list, chromatic_interval_and_its_fretted_instrument_chord in interval_to_chord:
        anki_notes.append(chromatic_interval_and_its_fretted_instrument_chord.csv())
        chromatic_interval_and_inversion = chromatic_interval_and_its_fretted_instrument_chord.interval_and_its_inversions
        inversions = chromatic_interval_and_inversion.inversions
        easiest_inversion = inversions[0]
        chromatic_position_of_lowest_interval_in_base_octave = easiest_inversion.position_of_lowest_interval_in_base_octave.chromatic
        for fretted_instrument_chord in chromatic_interval_and_its_fretted_instrument_chord.maximals():
            pos_of_lowest_note = fretted_instrument_chord.get_most_grave_note()
            lowest_note = pos_of_lowest_note.get_chromatic()
            tonic = lowest_note - chromatic_position_of_lowest_interval_in_base_octave
            save_file(f"{transposable_folder(instrument)}/{fretted_instrument_chord.file_name(stroke_colored=False, absolute=False)}", fretted_instrument_chord.svg(absolute=False))
            save_file(f"{transposable_folder(instrument)}/{fretted_instrument_chord.file_name(stroke_colored=True, absolute=False)}", fretted_instrument_chord.svg(absolute=False, colors=ChordColors(tonic)))
    return anki_notes, interval_to_chord

for instrument in fretted_instruments:
    register_all_chords(instrument)
    anki_notes, interval_to_chord = generate_anki_notes(instrument)
    save_file(f"{transposable_folder(instrument)}/anki.csv", "\n".join(anki_notes))

    biggest_anki_note = max((anki_note_content for interval_list, anki_note_content in interval_to_chord), 
                            key=lambda anki_note_content: len(anki_note_content.maximals()))
    print(f"=====================\n{instrument.name}, transposable chord\n===============================")
    print(f"{len(biggest_anki_note)=}")
    print(f"{biggest_anki_note=}")