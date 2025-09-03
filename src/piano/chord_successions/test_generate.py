# import unittest
# from piano.chord_successions.generate import *

# class TestChordSuccession(unittest.TestCase):
#     maxDiff = None

#     scale = Scale([
#         Note.from_name("C"),
#         Note.from_name("D"),
#         Note.from_name("E"),
#         Note.from_name("F"),
#         Note.from_name("G"),
#         Note.from_name("A"),
#         Note.from_name("B"),
#         Note.from_name("C5"),
#         Note.from_name("D5"),
#         Note.from_name("E5"),
#         Note.from_name("F5"),
#         Note.from_name("G5"),
#         Note.from_name("A5"),
#         Note.from_name("B5"),
#         Note.from_name("C6"),
#     ], pattern=major_scale)

#     triad_right_succession = [
#         SetOfNotes(
#             [
#                 Note.from_name("C"),
#                 Note.from_name("E"),
#                 Note.from_name("G"),
#             ],
#             Note.from_name("C"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("D"),
#                 Note.from_name("F"),
#                 Note.from_name("A"),
#             ],
#             Note.from_name("D"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("E"),
#                 Note.from_name("G"),
#                 Note.from_name("B"),
#             ],
#             Note.from_name("E"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("F"),
#                 Note.from_name("A"),
#                 Note.from_name("C5"),
#             ],
#             Note.from_name("F"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("G"),
#                 Note.from_name("B"),
#                 Note.from_name("D5"),
#             ],
#             Note.from_name("G"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("A"),
#                 Note.from_name("C5"),
#                 Note.from_name("E5"),
#             ],
#             Note.from_name("A"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("B"),
#                 Note.from_name("D5"),
#                 Note.from_name("F5"),
#             ],
#             Note.from_name("B"),
#         ),
#         SetOfNotes(
#             [
#                 Note.from_name("C5"),
#                 Note.from_name("E5"),
#                 Note.from_name("G5"),
#             ],
#             Note.from_name("C5"),
#         ),
#     ]

#     lily_right_c_triad = """\
# \\version "2.20.0"
# \\score{
#   <<
#     \\new Staff{
#       \\override Staff.TimeSignature.stencil = ##f
#       \\omit Staff.BarLine
#       \\omit PianoStaff.SpanBar
#       \\time 30/4
#       \\set Staff.printKeyCancellation = ##f
#       \\clef treble
#       \\key c \\major
#       <c' e' g'> <d' f' a'> <e' g' b'> <f' a' c''> <g' b' d''> <a' c'' e''> <b' d'' f''> <c'' e'' g''>
#     }
#   >>
# }"""

#     lily_left_c_triad = """\
# \\version "2.20.0"
# \\score{
#   <<
#     \\new Staff{
#       \\override Staff.TimeSignature.stencil = ##f
#       \\omit Staff.BarLine
#       \\omit PianoStaff.SpanBar
#       \\time 30/4
#       \\set Staff.printKeyCancellation = ##f
#       \\clef bass
#       \\key c \\major
#       <c e g> <d f a> <e g b> <f a c'> <g b d'> <a c' e'> <b d' f'> <c' e' g'>
#     }
#   >>
# }"""

#     lily_both_c_triad = """\
# \\version "2.20.0"
# \\score{
#   <<
#     \\new PianoStaff<<
#       \\new Staff{
#         \\override Staff.TimeSignature.stencil = ##f
#         \\omit Staff.BarLine
#         \\omit PianoStaff.SpanBar
#         \\time 30/4
#         \\set Staff.printKeyCancellation = ##f
#         \\clef treble
#         \\key c \\major
#         <c' e' g'> <d' f' a'> <e' g' b'> <f' a' c''> <g' b' d''> <a' c'' e''> <b' d'' f''> <c'' e'' g''>
#       }
#       \\new Staff{
#         \\override Staff.TimeSignature.stencil = ##f
#         \\omit Staff.BarLine
#         \\omit PianoStaff.SpanBar
#         \\time 30/4
#         \\set Staff.printKeyCancellation = ##f
#         \\clef bass
#         \\key c \\major
#         <c e g> <d f a> <e g b> <f a c'> <g b d'> <a c' e'> <b d' f'> <c' e' g'>
#       }
#     >>
#   >>
# }"""

#     def test_chord_from_scale_pattern_and_position_key(self):
#         son = chord_from_scale_pattern_and_position_key(
#             self.scale,
#             chord_pattern=triad,
#             position=3,
#         )
#         self.assertEqual(son, SetOfNotes(
#             [
#                 Note.from_name("F"),
#                 Note.from_name("A"),
#                 Note.from_name("C5"),
#             ],
#             Note.from_name("F"),
#         ))

#     def test_chord_succession_from_scale_pattern_and_position_key(self):
#         suc = chord_succession_from_scale_pattern_and_position_key(
#             self.scale,
#             chord_pattern=triad,
#             nb_of_chords=8,
#         )
#         self.assertEqual(suc,
#                           self.triad_right_succession
#                           )

#     def test_succession_for_hands_key_pattern_direction_right(self):
#         suc = succession_for_hands_key_pattern_direction(
#             "folder", Note.from_name("C"), self.triad_right_succession, triad, for_left_hand=False, for_right_hand=True,
#             direction="increasing", midi=False
#         )
#         expected = CardContent("C______right_triad_increasing", "folder/C______right_triad_increasing",
#                                       self.lily_right_c_triad)
#         self.assertEqual(suc, expected)

#     def test_succession_for_hands_key_pattern_direction_both(self):
#         suc = succession_for_hands_key_pattern_direction(
#             "folder", Note.from_name("C"), self.triad_right_succession, triad, for_left_hand=True, for_right_hand=True,
#             direction="increasing", midi=False
#         )
#         self.assertEqual(suc.lily_code, self.lily_both_c_triad)
#         self.assertEqual(suc,
#                           CardContent("C______both_triad_increasing", "folder/C______both_triad_increasing",
#                                       self.lily_both_c_triad)
#                           )

#     def test_succession_for_hands_key_pattern_direction_left(self):
#         suc = succession_for_hands_key_pattern_direction(
#             "folder", Note.from_name("C"), self.triad_right_succession, triad, for_left_hand=True, for_right_hand=False,
#             direction="increasing", midi=False
#         )
#         cc = CardContent("C______left_triad_increasing", "folder/C______left_triad_increasing",
#                                       self.lily_left_c_triad)
#         print(suc)
#         print(cc)
#         self.assertEqual(suc, cc)
