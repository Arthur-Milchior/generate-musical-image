import unittest
from piano.progression.generate import *

from piano.progression.generate import *

from piano.progression.generate import *

class TestGenerate(unittest.TestCase):
    def test_one(self):
        folder_path = f"{test_folder}/progressions"
        ensure_folder(folder_path)
        card_line = progression_for_pattern_tonic(folder_path, ii_v_i_third_and_seventh, Note.from_name("C"), wav=False)
        self.assertEqual(card_line,
                          """C  ,ii V I,<img src="first_chord_progression_C______ii_3_7.svg">,<img src="progression_ii_V_I_C______3_7.svg">""")
        display_svg_file(f"{folder_path}/progression_ii_V_I_C______3_7.svg")
        display_svg_file(f"{folder_path}/first_chord_progression_C______ii_3_7.svg")
