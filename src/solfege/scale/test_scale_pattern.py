# import unittest
# from .scale_pattern import *


# class TestScalePattern(unittest.TestCase):

#     def test_ne(self):
#         self.assertNotEqual(minor_melodic,
#                              ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], four_flats))
#         self.assertNotEqual(minor_melodic, ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2],
#                                                                    three_flats, suppress_warning=False))
#         self.assertNotEqual(minor_melodic, ScalePattern(["Minor"], [2, 1, 2, 2, 2, 2, 1],
#                                                                    three_flats))

#     def test_eq(self):
#         self.assertEqual(minor_melodic.interval_for_signature, three_flats)
#         self.assertEqual(minor_melodic._diatonic_sum, 7)
#         self.assertEqual(minor_melodic._chromatic_sum, 12)
#         self.assertEqual(minor_melodic.relative_intervals, [
#             Interval.make(chromatic=2, diatonic=1),
#             Interval.make(chromatic=1, diatonic=1),
#             Interval.make(chromatic=2, diatonic=1),
#             Interval.make(chromatic=2, diatonic=1),
#             Interval.make(chromatic=2, diatonic=1),
#             Interval.make(chromatic=2, diatonic=1),
#             Interval.make(chromatic=1, diatonic=1),
#         ])

#     def test_get_notes(self):
#         tonic = Note.make(0, 0)
#         self.assertEqual(minor_melodic.get_notes(tonic),
#                           [
#                               Note.make(0, 0),
#                               Note.make(2, 1),
#                               Note.make(3, 2),
#                               Note.make(5, 3),
#                               Note.make(7, 4),
#                               Note.make(9, 5),
#                               Note.make(1, 6),
#                               Note.make(2, 7),
#                           ])

#     def test_neg(self):
#         reversed = -minor_melodic
#         expected = ScalePattern(["Minor melodic"],
#                                           [
#                                               Interval.make(diatonic=-1, chromatic=- 1),
#                                               Interval.make(diatonic=-1, chromatic=-2),
#                                               Interval.make(diatonic=-1, chromatic=-2),
#                                               Interval.make(diatonic=-1, chromatic=-2),
#                                               Interval.make(diatonic=-1, chromatic=-2),
#                                               Interval.make(diatonic=-1, chromatic=-1),
#                                               Interval.make(diatonic=-1, chromatic=-2)], three_flats, increasing=False,
#                                           record=False)
#         self.assertEqual(reversed,
#                           expected)

#     def test_generate(self):
#         expected = Scale(notes=[
#             Note.make(0, 0),
#             Note.make(2, 1),
#             Note.make(3, 2),
#             Note.make(5, 3),
#             Note.make(7, 4),
#             Note.make(9, 5),
#             Note.make(11, 6),
#             Note.make(12, 7),
#         ], pattern=minor_melodic)
#         generated = minor_melodic.generate(Note.make(0, 0))
#         self.assertEqual(expected, generated)

#     def test_generate_two(self):
#         expected = Scale(notes=[
#             Note.make(0, 0),
#             Note.make(2, 1),
#             Note.make(3, 2),
#             Note.make(5, 3),
#             Note.make(7, 4),
#             Note.make(9, 5),
#             Note.make(11, 6),
#             Note.make(12, 7),
#             Note.make(14, 8),
#             Note.make(15, 9),
#             Note.make(17, 0),
#             Note.make(19, 1),
#             Note.make(21, 2),
#             Note.make(23, 3),
#             Note.make(24, 4),
#         ], pattern=minor_melodic)
#         generated = minor_melodic.generate(Note.make(0, 0), number_of_octaves=2)
#         self.assertEqual(expected, generated)
#         expected = Scale(notes=[
#             Note.make(0, 0),
#             Note.make(2, 1),
#             Note.make(3, 2),
#             Note.make(5, 3),
#             Note.make(7, 4),
#             Note.make(9, 5),
#             Note.make(11, 6),
#             Note.make(12, 7),
#             Note.make(14, 8),
#             Note.make(15, 9),
#             Note.make(17, 0),
#             Note.make(19, 1),
#             Note.make(21, 2),
#             Note.make(23, 3),
#             Note.make(24, 4),
#             Note.make(26, 5),
#         ], pattern=minor_melodic)
#         generated = minor_melodic.generate(Note.make(0, 0), number_of_octaves=2, add_an_extra_note=True)
#         self.assertEqual(expected, generated)

#     def test_generate_minus_two(self):
#         expected = Scale(notes=[
#             Note.make(0, 0),
#             Note.make(-1, -1),
#             Note.make(-3, -2),
#             Note.make(-5, -3),
#             Note.make(-7, -4),
#             Note.make(-9, -5),
#             Note.make(-10, -6),
#             Note.make(-12, -7),
#             Note.make(-13, -8),
#             Note.make(-15, -9),
#             Note.make(-17, 0),
#             Note.make(-19, 1),
#             Note.make(-21, 2),
#             Note.make(-22, 3),
#             Note.make(-24, 4),
#         ], pattern=minor_melodic)
#         generated = minor_melodic.generate(Note.make(0, 0), number_of_octaves=-2)
#         self.assertEqual(expected, generated)
#         expected = Scale(notes=[
#             Note.make(0, 0),
#             Note.make(-1, -1),
#             Note.make(-3, -2),
#             Note.make(-5, -3),
#             Note.make(-7, -4),
#             Note.make(-9, -5),
#             Note.make(-10, -6),
#             Note.make(-12, -7),
#             Note.make(-13, -8),
#             Note.make(-15, -9),
#             Note.make(-17, 0),
#             Note.make(-19, 1),
#             Note.make(-21, 2),
#             Note.make(-22, 3),
#             Note.make(-24, 4),
#             Note.make(-25, 5),
#         ], pattern=minor_melodic)
#         generated = minor_melodic.generate(Note.make(0, 0), number_of_octaves=-2, add_an_extra_note=True)
#         self.assertEqual(expected, generated)

#     def test_number_of_intervals(self):
#         self.assertEqual(len(minor_melodic), 7)
#         self.assertEqual(len(pentatonic_minor), 5)
