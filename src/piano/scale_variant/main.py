from lily.Lilyable.list_piano_lilyable import ListPianoLilyable
from lily.Lilyable.piano_lilyable import LiteralPianoLilyable
from lily.lily import compile_
from piano.fingering_generation.generate import generate_best_fingering_for_melody
from solfege.interval.interval import Interval
from solfege.key import sets_of_enharmonic_keys, Key
from solfege.scale.scale import Scale
from solfege.scale.scale_pattern import major_scale, scale_patterns
from utils.util import ensure_folder

"""
Generate the scales, followed by the same scale, moved by a semi-tone in the reverse side
"""

anki_entries = []
folder_path = "/home/milchior/generate-musical-image/generated/piano/scales_half_tone_off"
ensure_folder(folder_path)

for scale_pattern in scale_patterns:
    pattern_name = scale_pattern.first_of_the_names()
    pattern_name_ = pattern_name.replace(' ', '_')
    scale_folder = f"{folder_path}/{pattern_name_}"
    ensure_folder(scale_folder)
    for set_of_enharmonic_keys in sets_of_enharmonic_keys:
        first_key = set_of_enharmonic_keys[0]
        increasing_first_scale = scale_pattern.generate(first_key.note)
        decreasing_first_scale = Scale(list(reversed(increasing_first_scale.notes)), increasing_first_scale.pattern)
        for second_key_note in [
            first_key.note + Interval.make(chromatic=1, diatonic=1),
            first_key.note + Interval.make(chromatic=-1, diatonic=-1),
        ]:
            second_key = Key.from_note(second_key_note)
            interval_correction_second_key = second_key.note - second_key_note
            assert interval_correction_second_key.in_base_octave() == Interval.make(0, 0)
            nb_octave_correction = interval_correction_second_key.octave()
            second_key_note = second_key.simplest_enharmonic_major().note.add_octave(-nb_octave_correction)
            increasing_second_scale = scale_pattern.generate(second_key_note)
            decreasing_second_scale = Scale(list(reversed(increasing_second_scale.notes)),
                                            increasing_second_scale.pattern)
            for (first_scale, second_scale, first_direction, second_direction) in [
                (increasing_first_scale, decreasing_second_scale, "increasing", "decreasing"),
                (decreasing_first_scale, increasing_second_scale, "decreasing", "increasing"),
            ]:
                all_notes_right_hand = first_scale.notes + second_scale.notes
                all_notes_left_hand = first_scale.add_octave(-1).notes + second_scale.add_octave(-1).notes
                left_penalty = generate_best_fingering_for_melody(all_notes_left_hand, False)
                right_penalty = generate_best_fingering_for_melody(all_notes_right_hand, True)
                assert left_penalty is not None
                assert right_penalty is not None
                left_to_lily = left_penalty.fingerings[0]
                right_to_lily = right_penalty.fingerings[0]
                length = len(scale_pattern) + 1
                first_part = LiteralPianoLilyable.make(first_key.note, left_to_lily[:length], right_to_lily[:length])
                second_part = LiteralPianoLilyable.make(second_key_note, left_to_lily[length:],
                                                           right_to_lily[length:])
                two_scales = ListPianoLilyable([first_part, second_part])
                file_prefix = f"{pattern_name_}_{first_key.note.get_name_with_octave(
                    octave_notation=OctaveOutput.MIDDLE_IS_4,
                    alteration_output = AlterationOutput.SYMBOL, 
                    note_output = NoteOutput.LETTER, 
                    fixed_length = FixedLengthOutput.NO
                    ))}_{first_direction}_{second_key_note.get_name_with_octave(
                    octave_notation=OctaveOutput.MIDDLE_IS_4,
                    alteration_output = AlterationOutput.SYMBOL, 
                    note_output = NoteOutput.LETTER, 
                    fixed_length = FixedLengthOutput.NO
                    ))}_{second_direction}"
                compile_(two_scales.lily(False), f"{scale_folder}/{file_prefix}", False)
                anki_entries.append(
                    f"""<img src="{file_prefix}.svg"/>|{pattern_name} in {first_key.note.get_name_with_octave(octave_notation=OctaveOutput.OCTAVE_MIDDLE_PIANO_4, ascii=False, )} and {second_key_note.get_name_with_octave(octave_notation=OctaveOutput.OCTAVE_MIDDLE_PIANO_4, ascii=False, )}""")

with open(f"{folder_path}/anki.csv", "w") as f:
    f.write("\n".join(anki_entries))
