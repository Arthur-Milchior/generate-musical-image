import util
from lily.lily import lilypond_code_for_one_hand, compile_
from piano.chord_successions.generate import chord_patterns, ChordPattern, \
    chord_succession_for_scale
from solfege.Scale.scale import Scale
from solfege.Scale.scale_pattern import major_scale
from solfege.clef import clefs
from solfege.note.alteration import LILY, FILE_NAME


def generate_chord_successions_pattern_fundamental(two_octave_scales: Scale,
                                                   key_file: str,
                                                   key_lily: str,
                                                   chord_pattern: ChordPattern,
                                                   folder_path: str,
                                                   execute_lily: bool,
                                                   wav: bool):
    chords = chord_succession_for_scale(scale=two_octave_scales, chord_pattern=chord_pattern, nb_of_chords=8)
    file_prefix = f"{folder_path}/{chord_pattern.name}_in_{key_file}"
    if execute_lily:
        lily_code = lilypond_code_for_one_hand(key=key_lily, notes_or_chords=chords, use_color=False,
                                               for_right_hand=True, midi=wav)
        compile_(lily_code, file_prefix, execute_lily=execute_lily, wav=wav)
    return f"{chord_pattern.name},{key_file},<img src='{file_prefix}.svg'>"


def generate_chord_successions_pattern(chord_pattern: ChordPattern, folder_path: str, execute_lily: bool, wav: bool):
    anki_csv = []
    for key in clefs:
        two_octave_scales = major_scale.generate(fundamental=key.note, number_of_octaves=2)
        csv_line = generate_chord_successions_pattern_fundamental(two_octave_scales=two_octave_scales,
                                                                  key_file=key.note.get_note_name(FILE_NAME),
                                                                  key_lily=key.note.get_note_name(LILY),
                                                                  chord_pattern=chord_pattern, folder_path=folder_path,
                                                                  execute_lily=execute_lily, wav=wav)
        anki_csv.append(csv_line)
    return anki_csv


def generate_chord_successions(folder_path: str, execute_lily: bool, wav: bool):
    anki_csv = []
    for chord_pattern in chord_patterns:
        anki_csv += generate_chord_successions_pattern(chord_pattern, folder_path, execute_lily, wav)
    with open(f"{folder_path}/anki.csv", "w") as file:
        file.write("\n".join(anki_csv))


if __name__ == '__main__':
    folder_path = "../../../generated/piano/chord_successions"
    util.ensure_folder(folder_path)
    generate_chord_successions(folder_path=folder_path, execute_lily=True, wav=True)
