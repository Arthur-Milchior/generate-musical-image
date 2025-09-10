# import unittest
# from .fretted_instrument_position_with_finger import *

# class TestFrettedInstrumentPositionWithFinger(unittest.TestCase):
#     def test_positions_minus_tone_finger_1(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=2, fret=9, finger=4),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=1)
#         .positions_for_interval(ChromaticInterval(-2))
#         )

#     def test_positions_minus_half_tone_finger_1(self):
#         self.assertEqual([
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=1)
#         .positions_for_interval(ChromaticInterval(-1))
#         )

#     def test_positions_minus_half_tone_finger_3(self):
#         self.assertEqual([
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=5, finger=1),
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=5, finger=2),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=3)
#         .positions_for_interval(ChromaticInterval(-1))
#         )

#     def test_positions_minus_half_tone_finger_4(self):
#         self.assertEqual([
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=5, finger=1),
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=5, finger=2),
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=5, finger=3),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=4)
#         .positions_for_interval(ChromaticInterval(-1))
#         )

        
#     def test_positions_half_tone_finger_1(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=7, finger=2),
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=7, finger=3),
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=7, finger=4),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=1)
#         .positions_for_interval(ChromaticInterval(1))
#         )

#     def test_positions_half_tone_finger_3(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=7, finger=4),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=3)
#         .positions_for_interval(ChromaticInterval(1))
#         )

#     def test_positions_half_tone_finger_4(self):
#         self.assertEqual([
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=4)
#         .positions_for_interval(ChromaticInterval(1))
#         )

#     def test_positions_tone_finger_1(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=8, finger=3),
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=8, finger=4),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=1)
#         .positions_for_interval(ChromaticInterval(2))
#         )

#     def test_positions_tone_finger_3(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=3, fret=8, finger=4),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=3)
#         .positions_for_interval(ChromaticInterval(2))
#         )

#     def test_positions_tone_finger_4(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=4, fret=3, finger=1),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=4)
#         .positions_for_interval(ChromaticInterval(2))
#         )

#     def test_positions_2tone_finger_1(self):
#         self.assertEqual([
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=1)
#         .positions_for_interval(ChromaticInterval(4))
#         )

#     def test_positions_2tone_finger_3(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=4, fret=5, finger=1),
#             FrettedInstrumentPositionWithFinger.make(string=4, fret=5, finger=2),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=3)
#         .positions_for_interval(ChromaticInterval(4))
#         )

#     def test_positions_2tone_finger_4(self):
#         self.assertEqual([
#             FrettedInstrumentPositionWithFinger.make(string=4, fret=5, finger=1),
#             FrettedInstrumentPositionWithFinger.make(string=4, fret=5, finger=2),
#             FrettedInstrumentPositionWithFinger.make(string=4, fret=5, finger=3),
#         ],
#         FrettedInstrumentPositionWithFinger.make(string=3, fret=6, finger=4)
#         .positions_for_interval(ChromaticInterval(4))
#         )