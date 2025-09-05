from guitar.chord.chromatic_interval_list_to_guitar_chords import ChromaticIntervalListToGuitarChords
from guitar.chord.chord_utils import enumerate_guitar_chords
from guitar.position.frets import Frets

# Ensure that all chords are registered
from solfege.pattern.chord.chord_patterns import *
from solfege.pattern.chord.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.chord.inversion_pattern import InversionPattern
from consts import generate_root_folder
from solfege.value.interval.set.list import ChromaticIntervalList
from utils.util import ensure_folder

transposable_folder = f"{generate_root_folder}/guitar/chord/transposable"
ensure_folder(transposable_folder)


interval_to_chord = ChromaticIntervalListToGuitarChords.make()
for guitar_chord in enumerate_guitar_chords(Frets(min_fret=1, max_fret=3, allow_not_played=True, allow_open=False)):
    if not guitar_chord.is_playable():
        continue
    if guitar_chord.chord_pattern_is_redundant():
        continue
    if guitar_chord.number_of_distinct_notes() < 4:
        continue
    chromatic_intervals = guitar_chord.intervals_frow_lowest_note_in_base_octave()
    if chromatic_intervals is None:
        continue
    assert_typing(chromatic_intervals, ChromaticIntervalList)
    interval_to_inversion_patterns: IntervalListToInversionPattern = InversionPattern.get_record_keeper()
    assert_typing(interval_to_inversion_patterns, IntervalListToInversionPattern)
    chromatic_intervals_and_inversions = interval_to_inversion_patterns.get_from_chromatic_interval_list(chromatic_intervals)
    if chromatic_intervals_and_inversions is None:
        continue
    interval_to_chord.register(chromatic_intervals, guitar_chord)


biggest_anki_note = max((anki_note_content for interval_list, anki_note_content in interval_to_chord), 
                        key=lambda anki_note_content: len(anki_note_content.maximals()))

anki_notes = []
for interval_list, anki_note_content in interval_to_chord:
    anki_notes.append(anki_note_content.csv())
    for guitard_chord in anki_note_content.maximals():
        with open(f"{transposable_folder}/{guitar_chord.file_name(stroke_colored=False)}", "w") as f:
            f.write(guitar_chord.svg(absolute=False, stroke_colored=False))
        with open(f"{transposable_folder}/{guitar_chord.file_name(stroke_colored=True)}", "w") as f:
            f.write(guitar_chord.svg(absolute=False, stroke_colored=True))
with open(f"{transposable_folder}/anki.csv", "w") as f:
    f.write("\n".join(anki_notes))



print(f"{len(biggest_anki_note)=}")
print(f"{biggest_anki_note=}")