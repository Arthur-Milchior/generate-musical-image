from guitar.chord.open.chromatic_note_list_to_guitar_chords import ChromaticNoteListToGuitarChords
from guitar.chord.chord_utils import enumerate_guitar_chords
from guitar.chord.playable import Playable
from guitar.position.fret.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.chord.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.chord.inversion_pattern import InversionPattern
from consts import generate_root_folder
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.util import ensure_folder, save_file

open_folder = f"{generate_root_folder}/guitar/chord/open"
ensure_folder(open_folder)


note_to_chord = ChromaticNoteListToGuitarChords.make()
def register_all_chords():
    for guitar_chord in enumerate_guitar_chords(Frets.make(
        closed_fret_interval=(1, 
                              6
                              ),
        allow_not_played=True, 
        allow_open=True)):
        if guitar_chord.number_of_distinct_notes() < 4:
            continue
        if guitar_chord.has_not_played_in_middle():
            continue
        if guitar_chord.playable() != Playable.EASY:
            continue
        if guitar_chord.chord_pattern_is_redundant():
            continue
        chromatic_notes = guitar_chord.chromatic_notes()
        chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave()
        if chromatic_intervals is None:
            continue
        assert_typing(chromatic_notes, ChromaticNoteList)
        assert_typing(chromatic_intervals, ChromaticIntervalList)
        interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
        assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)
        chromatic_intervals_and_inversions = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals)
        if chromatic_intervals_and_inversions is None:
            continue
        note_to_chord.register(chromatic_notes, guitar_chord)
register_all_chords()


biggest_anki_note = max((anki_note_content for note_list, anki_note_content in note_to_chord), 
                        key=lambda anki_note_content: len(anki_note_content.maximals()))
print(f"{len(biggest_anki_note)=}")
print(f"{biggest_anki_note=}")

anki_notes = []
def generate_anki_notes():
    for note_list, chromatic_note_and_its_guitar_chord in note_to_chord:
        anki_notes.append(chromatic_note_and_its_guitar_chord.csv(absolute=True, lily_folder_path=open_folder))
        chromatic_interval_and_inversion = chromatic_note_and_its_guitar_chord.interval_and_its_inversions
        inversions = chromatic_interval_and_inversion.inversions
        easiest_inversion = inversions[0]
        position_of_lowest_interval_in_base_octave = easiest_inversion.position_of_lowest_interval_in_base_octave
        for guitar_chord in chromatic_note_and_its_guitar_chord.maximals():
            pos_of_lowest_note = guitar_chord.get_most_grave_note()
            lowest_note = pos_of_lowest_note.get_chromatic()
            tonic = lowest_note - position_of_lowest_interval_in_base_octave
            save_file(f"{open_folder}/{guitar_chord.file_name(stroke_colored=False, absolute=True)}", guitar_chord.svg(absolute=True, tonic=None))
            save_file(f"{open_folder}/{guitar_chord.file_name(stroke_colored=True, absolute=True)}", guitar_chord.svg(absolute=True, tonic=tonic))
generate_anki_notes()
save_file(f"{open_folder}/anki.csv", "\n".join(anki_notes))


