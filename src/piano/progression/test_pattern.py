from .pattern import *

# class ProgressionPatternTest(unittest.TestCase):
#     maxDiff = None
#
#     def test_add_chord(self):
#         from piano.progression.chord_progression import ProgressionTest
#         s = (ProgressionTest.d_min_7-Note("C4")) + Note("C4")
#         self.assertEqual(s, ProgressionTest.d_min_7)
#
#     def test_add_progression(self):
#         from piano.progression.chord_progression import ProgressionTest
#         s = (ProgressionTest.three_five_c - Note("C4")) + Note("C")
#         self.assertEqual(s, ProgressionTest.three_five_c)
#
#     def test_see_all(self):
#         from piano.progression.progressions_in_C import patterns_in_C
#         for pattern in patterns_in_C:
#             lily = pattern.lily()
#             path = f"{test_folder}/{pattern.progression_name}"
#             compile_(lily, path, wav=True)
#             display_svg_file(f"{path}.svg")
