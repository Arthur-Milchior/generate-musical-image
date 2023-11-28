import os

import util
from lily.lily import lilypond_code_for_one_hand, compile_
from piano.chord_successions.generate import chord_patterns, ChordPattern, \
    chord_succession_for_scale
from solfege.key import sets_of_enharmonic_keys
from solfege.note import Note
from solfege.scale.scale import Scale
from solfege.scale.scale_pattern import major_scale


def generate_chord_successions_pattern_fundamental(two_octave_scales: Scale,
                                                   key: Note,
                                                   chord_pattern: ChordPattern,
                                                   folder_path: str,
                                                   execute_lily: bool,
                                                   wav: bool):
    chords = chord_succession_for_scale(scale=two_octave_scales, chord_pattern=chord_pattern, nb_of_chords=8)
    file_prefix = f"{chord_pattern.name}_in_{key.get_ascii_name()}"
    file_path_prefix = f"{folder_path}/{file_prefix}"
    if execute_lily:
        lily_code = lilypond_code_for_one_hand(key=key.lily(), notes_or_chords=chords,
                                               for_right_hand=True, midi=wav)
        compile_(lily_code, file_path_prefix, execute_lily=execute_lily, wav=wav)
    return f"Play the {chord_pattern.name}s in the {key.get_symbol_name()} major scale,<img src='{file_prefix}.svg'>"


def generate_chord_successions_pattern(chord_pattern: ChordPattern, folder_path: str, execute_lily: bool, wav: bool):
    anki_csv = []
    for set_of_enharmonic_keys in sets_of_enharmonic_keys:
        key = set_of_enharmonic_keys[0].note
        while key >= Note.from_name("F4"):
            key = key.add_octave(-1)
        two_octave_scales = major_scale.generate(fundamental=key, number_of_octaves=2)
        csv_line = generate_chord_successions_pattern_fundamental(two_octave_scales=two_octave_scales,
                                                                  key=key,
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
    os.system("echo $(pwd)")
    folder_path = "../../../generated/piano/chord_successions"
    util.ensure_folder(folder_path)
    generate_chord_successions(folder_path=folder_path, execute_lily=True, wav=True)
