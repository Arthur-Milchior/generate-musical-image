from instruments.piano.progression.pattern import *

# class ProgressionPatternTest(unittest.TestCase):
#     maxDiff = None
#
#     def test_add_chord(self):
#         from instruments.piano.progression.chord_progression import ProgressionTest
#         s = (ProgressionTest.d_min_7-Note.from_name("C4")) + Note.from_name("C4")
#         self.assertEqual(s, ProgressionTest.d_min_7)
#
#     def test_add_progression(self):
#         from instruments.piano.progression.chord_progression import ProgressionTest
#         s = (ProgressionTest.three_five_c - Note.from_name("C4")) + Note.from_name("C")
#         self.assertEqual(s, ProgressionTest.three_five_c)
#
#     def test_see_all(self):
#         from instruments.piano.progression.progressions_in_C import patterns_in_C
#         for pattern in patterns_in_C:
#             lily = pattern.lily()
#             path = f"{test_folder}/{pattern.progression_name}"
#             compile_(lily, path, wav=True)
#             display_svg_file(f"{path}.svg")
