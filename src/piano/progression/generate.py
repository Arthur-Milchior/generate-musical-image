import unittest
from typing import List

from lily.lily import compile_
from lily.svg import display_svg_file
from piano.progression.pattern import ChordProgressionPattern, ii_v_i_third_and_seventh, patterns
from solfege.key import sets_of_enharmonic_keys
from solfege.note import Note
from utils.constants import test_folder
from utils.util import ensure_folder


def progression_for_pattern_tonic(folder_path: str, pattern: ChordProgressionPattern, tonic: Note, wav: bool) -> str:
    """Generate the svg for this progression with this fundamental. Returns the anki card as a csv line"""
    first_chord_pattern = pattern.chords[0]
    progression = pattern + tonic
    first_chord = progression.first_chord()
    first_chord_prefix = f"""first_chord_progression_{tonic.get_ascii_name()}_{first_chord_pattern.role}_{first_chord_pattern.order.replace(" ", "_")}"""
    lily_first_chord = first_chord.lily()
    compile_(lily_first_chord, f"{folder_path}/{first_chord_prefix}", wav=wav)

    progression_prefix = f"""progression_ii_V_I_{tonic.get_ascii_name()}_{first_chord_pattern.order.replace(" ", "_")}"""
    compile_(progression.lily(), f"{folder_path}/{progression_prefix}", wav=wav)

    return ",".join([tonic.get_symbol_name(), "ii V I", f"""<img src="{first_chord_prefix}.svg">""",
                     f"""<img src="{progression_prefix}.svg">"""])


def progressions_for_pattern(folder_path: str, pattern: ChordProgressionPattern, wav: bool) -> List[str]:
    note_csv = []
    for set_of_enharmonic_keys in sets_of_enharmonic_keys:
        tonic = set_of_enharmonic_keys[0].note
        note_csv.append(progression_for_pattern_tonic(folder_path, pattern, tonic, wav))
    return note_csv


def progressions(folder_path: str, wav: bool) -> List[str]:
    note_csv = []
    for progression_pattern in patterns:
        note_csv += progressions_for_pattern(folder_path, progression_pattern, wav)
    return note_csv


class TestGenerate(unittest.TestCase):
    def test_one(self):
        folder_path = f"{test_folder}/progressions"
        ensure_folder(folder_path)
        card_line = progression_for_pattern_fundamental(folder_path, ii_v_i_third_and_seventh, Note("C"))
        self.assertEquals(card_line,
                          """C  ,<img src="first_chord_progression_C______ii_3_7.svg">,<img src="progression_ii_V_I_C______3_7.svg">""")
        display_svg_file(f"{folder_path}/progression_ii_V_I_C______3_7.svg")
        display_svg_file(f"{folder_path}/first_chord_progression_C______ii_3_7.svg")
