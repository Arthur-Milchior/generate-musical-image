# from solfege.solfege_pattern import SolfegePattern
# from solfege.pattern.scale.scale_pattern import ScalePattern
# from guitar.position.guitar_position import GuitarPosition
# from guitar.position.string import strings
# from guitar.position.fret import Fret
# from guitar.scale.utils import scale2Pos
# import unittest

# majorScale = SolfegePattern.class_to_name_to_pattern[ScalePattern].get("Major")

# class TestScale(unittest.TestCase):
#     def testEqual(self):
#         self.assertEqual(
#             scale2Pos(majorScale.get_intervals(), GuitarPosition(strings[0], Fret(1))),
#             [GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[0], Fret(3)), GuitarPosition(strings[0], Fret(5)), GuitarPosition(strings[1], Fret(1)), GuitarPosition(strings[1], Fret(3)),
#                                                             GuitarPosition(strings[1], Fret(5)), GuitarPosition(strings[2], Fret(2)), GuitarPosition(strings[2], Fret(3))])
# #print(scale2Pos(majorScale.get_intervals(), GuitarPosition(strings[0], Fret(2)))
