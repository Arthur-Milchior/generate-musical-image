# from solfege.solfege_pattern import SolfegePattern
# from solfege.pattern.scale.scale_pattern import ScalePattern
# from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
# from instruments.fretted_instrument.position.string.string import strings
# from instruments.fretted_instrument.position.fret.fret import Fret
# from instruments.fretted_instrument.scale.utils import scale2Pos
# import unittest

# majorScale = SolfegePattern.class_to_name_to_pattern[ScalePattern].get("Major")

# class TestScale(unittest.TestCase):
#     def testEqual(self):
#         self.assertEqual(
#             scale2Pos(majorScale.get_intervals(), PositionOnFrettedInstrument(strings[0], instrument.fret(1))),
#             [PositionOnFrettedInstrument(strings[0], instrument.fret(1)), PositionOnFrettedInstrument(strings[0], instrument.fret(3)), PositionOnFrettedInstrument(strings[0], instrument.fret(5)), PositionOnFrettedInstrument(strings[1], instrument.fret(1)), PositionOnFrettedInstrument(strings[1], instrument.fret(3)),
#                                                             PositionOnFrettedInstrument(strings[1], instrument.fret(5)), PositionOnFrettedInstrument(strings[2], instrument.fret(2)), PositionOnFrettedInstrument(strings[2], instrument.fret(3))])
# #print(scale2Pos(majorScale.get_intervals(), PositionOnFrettedInstrument(strings[0], instrument.fret(2)))
