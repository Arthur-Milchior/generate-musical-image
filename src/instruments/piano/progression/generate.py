# from typing import List

# from lily.lily import compile_
# from lily.svg import display_svg_file
# from instruments.piano.progression.chord_progression import ChordProgression, TwoHandsChord
# from instruments.piano.progression.progressions_in_C import patterns_in_C, ii_v_i_third_and_seventh
# from solfege.value.key.key import sets_of_enharmonic_keys
# from solfege.value.note.note import Note
# from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
# from utils.constants import test_folder
# from utils.util import ensure_folder


# def progression_for_pattern_tonic(folder_path: str, pattern: ChordProgression, tonic: Note, wav: bool) -> str:
#     """Generate the svg for this progression with this tonic. Returns the anki card as a csv line

#     pattern: the chord progression in C"""

#     first_chord_pattern: TwoHandsChord = pattern.chords[0]
#     progression = pattern + (tonic - Note.from_name("C4"))
#     first_chord = progression.first_chord()
#     tonic_note_name_for_file = tonic.get_name_up_to_octave(alteration_output=AlterationOutput.ASCII, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.UNDERSCORE_SIMPLE)
#     first_chord_prefix = f"""first_chord_progression_{tonic_note_name_for_file}_{first_chord_pattern.name}_{pattern.disambiguation.replace(" ", "_")}"""
#     lily_first_chord = first_chord.lily()
#     compile_(lily_first_chord, f"{folder_path}/{first_chord_prefix}", wav=wav)

#     progression_prefix = f"""progression_ii_V_I_{tonic_note_name_for_file}_{pattern.disambiguation.replace(" ", "_")}"""
#     compile_(progression.lily(), f"{folder_path}/{progression_prefix}", wav=wav)

#     tonic_note_name_for_field = tonic.get_name_up_to_octave(alteration_output= AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.SPACE_DOUBLE)
#     return ",".join([tonic_note_name_for_field, "ii V I", f"""<img src="{first_chord_prefix}.svg">""",
#                      f"""<img src="{progression_prefix}.svg">"""])


# def progressions_for_pattern(folder_path: str, pattern: ChordProgression, wav: bool) -> List[str]:
#     """pattern: the chord progression in C"""
#     note_csv = []
#     for set_of_enharmonic_keys in sets_of_enharmonic_keys:
#         tonic = set_of_enharmonic_keys[0].note
#         note_csv.append(progression_for_pattern_tonic(folder_path, pattern, tonic, wav))
#     return note_csv


# def progressions(folder_path: str, wav: bool) -> List[str]:
#     note_csv = []
#     for progression_pattern in patterns_in_C:
#         note_csv += progressions_for_pattern(folder_path, progression_pattern, wav)
#     return note_csv


