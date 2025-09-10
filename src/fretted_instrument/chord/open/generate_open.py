from fretted_instrument.chord.fretted_instrument_chord import ChordColors
from fretted_instrument.chord.open.chromatic_note_list_to_fretted_instrument_chords import ChromaticNoteListToFrettedInstrumentChords
from fretted_instrument.chord.chord_utils import enumerate_fretted_instrument_chords
from fretted_instrument.chord.playable import Playable
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.fretted_instrument.fretted_instruments import Gui_tar, fretted_instruments
from fretted_instrument.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.chord.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.chord.inversion_pattern import InversionPattern
from consts import generate_root_folder
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.util import assert_typing, ensure_folder, save_file

def open_folder(instrument: FrettedInstrument):
    path = f"{instrument.generated_folder_name()}/chord/open"
    ensure_folder(path)
    return path


note_to_chord = ChromaticNoteListToFrettedInstrumentChords.make()
def register_all_chords(instrument):
    for fretted_instrument_chord in enumerate_fretted_instrument_chords(instrument, Frets.make(instrument,
        _closed_fret_interval=(1, 
                              6
                              ),
        allow_not_played=True, 
        allow_open=True)):
        if fretted_instrument_chord.number_of_distinct_notes() < 4:
            continue
        if fretted_instrument_chord.has_not_played_in_middle():
            continue
        if fretted_instrument_chord.playable() != Playable.EASY:
            continue
        if fretted_instrument_chord.chord_pattern_is_redundant():
            continue
        chromatic_notes = fretted_instrument_chord.chromatic_notes()
        chromatic_intervals = fretted_instrument_chord.intervals_frow_lowest_note_in_base_octave()
        if chromatic_intervals is None:
            continue
        assert_typing(chromatic_notes, ChromaticNoteList)
        assert_typing(chromatic_intervals, ChromaticIntervalList)
        interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
        assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)
        chromatic_intervals_and_inversions = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals)
        if chromatic_intervals_and_inversions is None:
            continue
        note_to_chord.register(chromatic_notes, fretted_instrument_chord)


def generate_anki_notes(instrument: FrettedInstrument):
    anki_notes = []
    for note_list, chromatic_note_and_its_fretted_instrument_chord in note_to_chord:
        anki_notes.append(chromatic_note_and_its_fretted_instrument_chord.csv(absolute=True, lily_folder_path=open_folder(instrument)))
        chromatic_interval_and_inversion = chromatic_note_and_its_fretted_instrument_chord.interval_and_its_inversions
        inversions = chromatic_interval_and_inversion.inversions
        easiest_inversion = inversions[0]
        chromatic_position_of_lowest_interval_in_base_octave = easiest_inversion.position_of_lowest_interval_in_base_octave.chromatic
        for fretted_instrument_chord in chromatic_note_and_its_fretted_instrument_chord.maximals():
            pos_of_lowest_note = fretted_instrument_chord.get_most_grave_note()
            lowest_note = pos_of_lowest_note.get_chromatic()
            chromatic_tonic = lowest_note - chromatic_position_of_lowest_interval_in_base_octave
            save_file(f"{open_folder(instrument)}/{fretted_instrument_chord.file_name(stroke_colored=False, absolute=True)}", fretted_instrument_chord.svg(absolute=True))
            save_file(f"{open_folder(instrument)}/{fretted_instrument_chord.file_name(stroke_colored=True, absolute=True)}", fretted_instrument_chord.svg(absolute=True, colors=ChordColors(chromatic_tonic)))
    return anki_notes

for instrument in fretted_instruments:
    register_all_chords(instrument)
    anki_notes = generate_anki_notes(instrument)
    save_file(f"{open_folder(instrument)}/anki.csv", "\n".join(anki_notes))



biggest_anki_note = max((anki_note_content for note_list, anki_note_content in note_to_chord), 
                        key=lambda anki_note_content: len(anki_note_content.maximals()))
print(f"{len(biggest_anki_note)=}")
print(f"{biggest_anki_note=}")
