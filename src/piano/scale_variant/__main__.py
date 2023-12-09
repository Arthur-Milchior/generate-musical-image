from lily.Lilyable.list_piano_lilyable import ListPianoLilyable
from lily.Lilyable.piano_lilyable import LiteralPianoLilyable
from lily.lily import compile_
from solfege.interval.interval import Interval
from solfege.key import sets_of_enharmonic_keys, Key
from solfege.scale.scale_pattern import major_scale
from utils.util import ensure_folder

files = []
folder_path = "/home/milchior/generate-musical-image/generated/piano/scale_half_tone_off"
ensure_folder(folder_path)

for set_of_enharmonic_keys in sets_of_enharmonic_keys:
    key = set_of_enharmonic_keys[0].note
    scale = major_scale.generate(key)
    increasing_two_hands_first_scale = LiteralPianoLilyable.factory(
        key, scale.add_octave(-1).notes, scale.notes
    )
    decreasing_two_hands_first_scale = LiteralPianoLilyable.factory(
        key, reversed(scale.add_octave(-1).notes), reversed(scale.notes)
    )
    for second_key_note in [
        key + Interval(chromatic=1, diatonic=1),
        key + Interval(chromatic=-1, diatonic=-1),
    ]:
        second_key = Key.from_note(second_key_note).simplest_enharmonic_major().note
        second_scale = major_scale.generate(second_key)
        for (first_scale_two_hands, second_scale_two_hands, first_direction, second_direction) in [
            (increasing_two_hands_first_scale, LiteralPianoLilyable.factory(
                second_key, reversed(second_scale.add_octave(-1).notes), reversed(second_scale.notes)
            ), "increasing", "decreasing"),
            (decreasing_two_hands_first_scale, LiteralPianoLilyable.factory(
                second_key, second_scale.add_octave(-1).notes, second_scale.notes
            ), "decreasing", "increasing"),
        ]:
            two_scales = ListPianoLilyable([first_scale_two_hands, second_scale_two_hands])
            file_prefix = f"major_{key.get_ascii_name()}_{first_direction}_{second_key.get_ascii_name()}_{second_direction}"
            compile_(two_scales.lily(False), f"{folder_path}/{file_prefix}", False)
            files.append(f"{file_prefix}.svg")

with open(f"{folder_path}/anki.csv", "w") as f:
    f.write("\n".join(f"""<img src="{file_name}"/>""" for file_name in files))
