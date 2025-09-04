from guitar.chord.chromatic_interval_list_to_guitar_chords import ChromaticIntervalListToGuitarChord
from guitar.chord.utils import enumerate_guitar_chords

interval_to_chord = ChromaticIntervalListToGuitarChord()
for chord in enumerate_guitar_chords():
    interval_to_chord.maybe_register(chord)


max_length = max(len(anki_note_content) for interval_list, anki_note_content in interval_to_chord)

print(f"{max_length=}")
    