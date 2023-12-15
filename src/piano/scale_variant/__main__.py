from lily.Lilyable.list_piano_lilyable import ListPianoLilyable
from lily.Lilyable.piano_lilyable import LiteralPianoLilyable
from lily.lily import compile_
from piano.fingering_generation.generate import generate_best_fingering_for_melody
from solfege.interval.interval import Interval
from solfege.key import sets_of_enharmonic_keys, Key
from solfege.scale.scale import Scale
from solfege.scale.scale_pattern import major_scale, scale_patterns
from utils.util import ensure_folder

anki_entries = []
folder_path = "/home/milchior/generate-musical-image/generated/piano/scale_half_tone_off"
ensure_folder(folder_path)

for scale_pattern in scale_patterns:
    pattern_name = scale_pattern.get_the_first_of_the_name()
    pattern_name_ = pattern_name.replace(' ', '_')
    scale_folder = f"{folder_path}/{pattern_name_}"
    ensure_folder(scale_folder)
    for set_of_enharmonic_keys in sets_of_enharmonic_keys:
        first_key = set_of_enharmonic_keys[0].note
        increasing_first_scale = scale_pattern.generate(first_key)
        decreasing_first_scale = Scale(list(reversed(increasing_first_scale.notes)), increasing_first_scale.pattern)
        for second_key_note in [
            first_key + Interval(chromatic=1, diatonic=1),
            first_key + Interval(chromatic=-1, diatonic=-1),
        ]:
            second_key = Key.from_note(second_key_note).simplest_enharmonic_major().note
            increasing_second_scale = scale_pattern.generate(second_key)
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
                length = scale_pattern.number_of_intervals() + 1
                first_part = LiteralPianoLilyable.factory(first_key, left_to_lily[:length], right_to_lily[:length])
                second_part = LiteralPianoLilyable.factory(second_key, left_to_lily[length:], right_to_lily[length:])
                two_scales = ListPianoLilyable([first_part, second_part])
                file_prefix = f"{pattern_name_}_{first_key.get_ascii_name()}_{first_direction}_{second_key.get_ascii_name()}_{second_direction}"
                compile_(two_scales.lily(False), f"{scale_folder}/{file_prefix}", False)
                anki_entries.append(
                    f"""<img src="{file_prefix}.svg"/>|{pattern_name} in {first_key.get_symbol_name()} and {second_key.get_symbol_name()}""")

with open(f"{folder_path}/anki.csv", "w") as f:
    f.write("\n".join(anki_entries))
