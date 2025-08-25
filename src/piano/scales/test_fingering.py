# import unittest
# from .fingering import *

# class TestFingering(unittest.TestCase):
#     maxDiff = None
#     tonic = Note.from_name("C")
#     right_minor_melodic_fingering = Fingering(for_right_hand=True).add_pinky_side(PianoNote.from_name("C5", 5))
#     right_minor_melodic_1 = [PianoNote.make(chromatic=0, diatonic=0, finger=1),
#                              PianoNote.make(chromatic=2, diatonic=1, finger=2),
#                              PianoNote.make(chromatic=3, diatonic=2, finger=3),
#                              PianoNote.make(chromatic=5, diatonic=3, finger=1),
#                              PianoNote.make(chromatic=7, diatonic=4, finger=2),
#                              PianoNote.make(chromatic=9, diatonic=5, finger=3),
#                              PianoNote.make(chromatic=11, diatonic=6, finger=4),
#                              PianoNote.make(chromatic=12, diatonic=7, finger=5),
#                              ]
#     for note in reversed(right_minor_melodic_1[:-1]):
#         right_minor_melodic_fingering = right_minor_melodic_fingering.add(
#             PianoNote.make(chromatic=note.get_chromatic().value, diatonic=note.get_diatonic().value,
#                       finger=note.finger))

#     left_minor_melodic_fingering = Fingering(for_right_hand=False).add_pinky_side(PianoNote.from_name("C", 5))
#     left_minor_melodic_1 = [PianoNote.make(chromatic=0, diatonic=0, finger=5),
#                             PianoNote.make(chromatic=2, diatonic=1, finger=4),
#                             PianoNote.make(chromatic=3, diatonic=2, finger=3),
#                             PianoNote.make(chromatic=5, diatonic=3, finger=2),
#                             PianoNote.make(chromatic=7, diatonic=4, finger=1),
#                             PianoNote.make(chromatic=9, diatonic=5, finger=3),
#                             PianoNote.make(chromatic=11, diatonic=6, finger=2),
#                             PianoNote.make(chromatic=12, diatonic=7, finger=1),
#                             ]

#     for note in left_minor_melodic_1[1:]:
#         left_minor_melodic_fingering = left_minor_melodic_fingering.add(
#             PianoNote.make(chromatic=note.get_chromatic().value, diatonic=note.get_diatonic().value,
#                       finger=note.finger))

#     empty = Fingering(for_right_hand=True)
#     pinky_alone = empty.add_pinky_side(PianoNote.from_name("C", 5))
#     octave = Note.make(12, 7)
#     octave_interval = pinky_alone.add(PianoNote.from_name("C", 1))
#     three_notes = octave_interval.add(PianoNote.from_name("D", 2))

#     def test_pinky(self):
#         self.assertIsInstance(self.pinky_alone, Fingering)
#         self.assertEqual(self.pinky_alone.get_pinky_side_tonic_finger(), 5)
#         self.assertEqual(self.pinky_alone.get_thumb_side_tonic_finger(), None)
#         self.assertEqual(self.pinky_alone.tonic, self.tonic)
#         self.assertEqual(self.pinky_alone.get_finger(self.tonic), None)
#         self.assertEqual(self.pinky_alone.get_finger(self.tonic, pinky_side_finger=True), 5)
#         self.assertEqual(self.pinky_alone.get_finger(Note.from_name("D")), None)
#         with self.assertRaises(Exception):
#             self.pinky_alone.get_finger(Note.from_name("D"), pinky_side_finger=True)
#         r = repr(self.pinky_alone)
#         self.assertEqual(r, """scales(for_right_hand=True).
#   add_pinky_side(PianoNote.make(chromatic=0, diatonic=0, finger=5))""")

#     def test_one_note(self):
#         self.assertIsInstance(self.octave_interval, Fingering)
#         self.assertEqual(self.octave_interval.get_pinky_side_tonic_finger(), 5)
#         self.assertEqual(self.octave_interval.get_thumb_side_tonic_finger(), 1)
#         self.assertEqual(self.octave_interval.tonic, self.tonic)
#         self.assertEqual(self.octave_interval.get_finger(self.tonic), 1)
#         self.assertEqual(self.octave_interval.get_finger(self.tonic, pinky_side_finger=True), 5)
#         self.assertEqual(self.octave_interval.get_finger(Note.from_name("D")), None)
#         r = repr(self.octave_interval)
#         self.assertEqual(r, """scales(for_right_hand=True).
#   add_pinky_side(PianoNote.make(chromatic=0, diatonic=0, finger=5)).
#   add(PianoNote.make(chromatic=0, diatonic=0, finger=1))""")
#         with self.assertRaises(Exception):
#             self.octave_interval.get_finger(Note.from_name("D"), pinky_side_finger=True)

#     def test_two_note(self):
#         self.assertIsInstance(self.three_notes, Fingering)
#         self.assertEqual(self.three_notes.get_pinky_side_tonic_finger(), 5)
#         self.assertEqual(self.three_notes.get_thumb_side_tonic_finger(), 1)
#         self.assertEqual(self.three_notes.tonic, self.tonic)
#         self.assertEqual(self.three_notes.get_finger(self.tonic), 1)
#         self.assertEqual(self.three_notes.get_finger(self.tonic, pinky_side_finger=True), 5)
#         self.assertEqual(self.three_notes.get_finger(Note.from_name("D")), 2)
#         r = repr(self.three_notes)
#         self.assertEqual(r, """scales(for_right_hand=True).
#   add_pinky_side(PianoNote.make(chromatic=0, diatonic=0, finger=5)).
#   add(PianoNote.make(chromatic=0, diatonic=0, finger=1)).
#   add(PianoNote.make(chromatic=2, diatonic=1, finger=2))""")
#         with self.assertRaises(Exception):
#             self.three_notes.get_finger(Note.from_name("D"), pinky_side_finger=True)

#     def test_add_two_same_note(self):
#         self.assertTrue(self.three_notes.add(PianoNote.from_name("D", 2)))
#         self.assertFalse(self.three_notes.add(PianoNote.from_name("D", 3)))

#     def test_generate_right_hand(self):
#         self.assertEqual(
#             self.right_minor_melodic_fingering.generate(first_played_note=self.tonic, scale_pattern=minor_melodic),
#             self.right_minor_melodic_1)
#         two_octaves = [
#             PianoNote.make(chromatic=0, diatonic=0, finger=1),
#             PianoNote.make(chromatic=2, diatonic=1, finger=2),
#             PianoNote.make(chromatic=3, diatonic=2, finger=3),
#             PianoNote.make(chromatic=5, diatonic=3, finger=1),
#             PianoNote.make(chromatic=7, diatonic=4, finger=2),
#             PianoNote.make(chromatic=9, diatonic=5, finger=3),
#             PianoNote.make(chromatic=11, diatonic=6, finger=4),
#             PianoNote.make(chromatic=12, diatonic=7, finger=1),
#             PianoNote.make(chromatic=14, diatonic=8, finger=2),
#             PianoNote.make(chromatic=15, diatonic=9, finger=3),
#             PianoNote.make(chromatic=17, diatonic=10, finger=1),
#             PianoNote.make(chromatic=19, diatonic=11, finger=2),
#             PianoNote.make(chromatic=21, diatonic=12, finger=3),
#             PianoNote.make(chromatic=23, diatonic=13, finger=4),
#             PianoNote.make(chromatic=24, diatonic=14, finger=5),
#         ]
#         self.assertEqual(
#             self.right_minor_melodic_fingering.generate(first_played_note=self.tonic, scale_pattern=minor_melodic,
#                                                         number_of_octaves=2),
#             two_octaves)
#         two_octaves.reverse()
#         self.assertEqual(
#             self.right_minor_melodic_fingering.generate(first_played_note=self.tonic.add_octave(2),
#                                                         scale_pattern=minor_melodic,
#                                                         number_of_octaves=-2),
#             two_octaves)

#     def test_generate_left_hand(self):
#         generated = self.left_minor_melodic_fingering.generate(first_played_note=self.tonic,
#                                                                scale_pattern=minor_melodic)
#         self.assertEqual(
#             generated,
#             self.left_minor_melodic_1)
#         two_octaves = [
#             PianoNote.make(chromatic=0, diatonic=0, finger=5),
#             PianoNote.make(chromatic=2, diatonic=1, finger=4),
#             PianoNote.make(chromatic=3, diatonic=2, finger=3),
#             PianoNote.make(chromatic=5, diatonic=3, finger=2),
#             PianoNote.make(chromatic=7, diatonic=4, finger=1),
#             PianoNote.make(chromatic=9, diatonic=5, finger=3),
#             PianoNote.make(chromatic=11, diatonic=6, finger=2),
#             PianoNote.make(chromatic=12, diatonic=7, finger=1),
#             PianoNote.make(chromatic=14, diatonic=8, finger=4),
#             PianoNote.make(chromatic=15, diatonic=9, finger=3),
#             PianoNote.make(chromatic=17, diatonic=10, finger=2),
#             PianoNote.make(chromatic=19, diatonic=11, finger=1),
#             PianoNote.make(chromatic=21, diatonic=12, finger=3),
#             PianoNote.make(chromatic=23, diatonic=13, finger=2),
#             PianoNote.make(chromatic=24, diatonic=14, finger=1),
#         ]
#         self.assertEqual(
#             self.left_minor_melodic_fingering.generate(first_played_note=self.tonic, scale_pattern=minor_melodic,
#                                                        number_of_octaves=2),
#             two_octaves)
#         two_octaves.reverse()
#         self.assertEqual(
#             self.left_minor_melodic_fingering.generate(first_played_note=self.tonic.add_octave(2),
#                                                        scale_pattern=minor_melodic,
#                                                        number_of_octaves=-2),
#             two_octaves)

#     def test_from_scale(self):
#         fingering = FingeringSymbol.from_scale(self.right_minor_melodic_1, for_right_hand=True)
#         self.assertEqual(fingering, self.right_minor_melodic_fingering)
#         self.assertIsNone(FingeringSymbol.from_scale([
#             PianoNote.make(chromatic=0, diatonic=0, finger=1),
#             PianoNote.make(chromatic=2, diatonic=1, finger=2),
#             PianoNote.make(chromatic=3, diatonic=2, finger=3),
#             PianoNote.make(chromatic=5, diatonic=3, finger=1),
#             PianoNote.make(chromatic=7, diatonic=4, finger=2),
#             PianoNote.make(chromatic=9, diatonic=5, finger=3),
#             PianoNote.make(chromatic=11, diatonic=6, finger=4),
#             PianoNote.make(chromatic=12, diatonic=7, finger=1)], for_right_hand=True))
