# import unittest

# from solfege.value.note.abstract_note import AlterationOutput, NoteOutput
# from instruments.piano.scales.test_fingering import TestFingering
# from pi.generate import *

# class TestScalesGenerate(unittest.TestCase):
#     maxDiff = None

#     test_folder = f"{test_folder}/test_generation"
#     ensure_folder(test_folder)
#     c_major = [
#         Note.from_name("C"),
#         Note.from_name("D"),
#         Note.from_name("E"),
#         Note.from_name("F"),
#         Note.from_name("G"),
#         Note.from_name("A"),
#         Note.from_name("B"),
#         Note.from_name("C5"),
#     ]
#     d_flat_major = [
#         Note.from_name("D♭"),
#         Note.from_name("E♭"),
#         Note.from_name("F"),
#         Note.from_name("G♭"),
#         Note.from_name("A♭"),
#         Note.from_name("B♭"),
#         Note.from_name("C5"),
#         Note.from_name("D5♭"),
#     ]
#     two_major_half_tone = c_major + list(reversed(d_flat_major))

#     def test_generation_two_way(self):
#         best_penalty = generate_best_fingering_for_melody(self.two_major_half_tone, for_right_hand=True)
#         fingerings = best_penalty.fingerings
#         all_fingering = ListPianoLilyable(
#             [LiteralPianoLilyable.make(key=Note.from_name("C"), right_hand=fingering, left_hand=None) for fingering in
#              fingerings],
#             bar_separator="||")
#         lily = all_fingering.lily()
#         ensure_folder(test_folder)
#         file = f"{test_folder}/generate_new_scale_and_half_tone"
#         delete_file_if_exists(f"{file}.ly")
#         compile_(lily, file, False, extension="pdf")  # ()

#     def test_generation_scale(self):
#         best_penalty = generate_best_fingering_for_scale(self.c_major, for_right_hand=True)
#         fingerings = best_penalty.fingerings
#         all_fingering = ListPianoLilyable(
#             [LiteralPianoLilyable.make(key=Note.from_name("C"), right_hand=fingering, left_hand=None) for fingering, _ in
#              fingerings],
#             bar_separator="||")
#         lily = all_fingering.lily()
#         ensure_folder(test_folder)
#         file = f"{test_folder}/generate_new_scale"
#         delete_file_if_exists(f"{file}.ly")
#         compile_(lily, file, False, extension="pdf")  # ()

#     def generation_helper(self, tonic: Note, scale_pattern: ScalePattern, for_right_hand: bool,
#                           expected: Fingering, key: Optional[Note] = None,
#                           show: bool = False):
#         key = key or tonic
#         scale = scale_pattern.generate(tonic, 1)
#         best_penalty, fingerings = generate_best_fingering_for_scale(scale.notes,
#                                                                      for_right_hand=for_right_hand)
#         self.assertEqual(len(fingerings), 1)
#         piano_notes, fingering = fingerings[0]
#         if show:
#             # scale = fingering.generate(first_played_note=tonic, number_of_octaves=2, scale_pattern=scale_pattern)
#             lily_code = lilypond_code_for_one_hand(key=key.get_name_up_to_octave(note_output=NoteOutput.LILY, alteration_output=AlterationOutput.LILY), notes_or_chords=piano_notes,
#                                                    for_right_hand=for_right_hand,
#                                                    midi=False)
#             test_file = f"{test_folder}/test"
#             ly_path = f"{test_file}.ly"
#             svg_path = f"{test_file}.svg"
#             delete_file_if_exists(svg_path)
#             delete_file_if_exists(ly_path)
#             cmd = compile_(lily_code, file_prefix=test_file, execute_lily=True, wav=False)
#             cmd()

#         self.assertEqual(fingering, expected)

#     def test_blues_A_right(self):
#         expected = (Fingering(for_right_hand=True).
#                     add_pinky_side(note=PianoNote.from_name("A", finger=5)).
#                     add(note=PianoNote.from_name("G", finger=4)).
#                     add(note=PianoNote.from_name("E", finger=1)).
#                     add(note=PianoNote.from_name("D#", finger=4)).
#                     add(note=PianoNote.from_name("D", finger=3)).
#                     add(note=PianoNote.from_name("C", finger=2)).
#                     add(note=PianoNote.from_name("A3", finger=1)))
#         tonic = Note.from_name("A3")
#         self.generation_helper(tonic=tonic, scale_pattern=blues, for_right_hand=True, expected=expected,
#                                show=False, key=Note.from_name("c"))

#     def test_blues_D_right(self):
#         expected = (Fingering(for_right_hand=True).
#                     add_pinky_side(note=PianoNote.from_name("D5", finger=5)).
#                     add(note=PianoNote.from_name("C5", finger=4)).
#                     add(note=PianoNote.from_name("A", finger=1)).
#                     add(note=PianoNote.from_name("G#", finger=4)).
#                     add(note=PianoNote.from_name("G", finger=3)).
#                     add(note=PianoNote.from_name("F", finger=2)).
#                     add(note=PianoNote.from_name("D", finger=1)))
#         tonic = Note.from_name("D")
#         self.generation_helper(tonic=tonic, scale_pattern=blues, for_right_hand=True, expected=expected,
#                                show=True, key=Note.from_name("F"))

#     def test_pentatonic_major_right(self):
#         expected = (Fingering(for_right_hand=True).
#                     add_pinky_side(PianoNote.from_name("C# ", finger=5)).
#                     add(PianoNote.from_name("A# ", finger=3)).
#                     add(PianoNote.from_name("G# ", finger=2)).
#                     add(PianoNote.from_name("E# ", finger=1)).
#                     add(PianoNote.from_name("D# ", finger=2)).
#                     add(PianoNote.from_name("C# ", finger=1)))
#         self.generation_helper(tonic=Note.from_name("C#"), scale_pattern=pentatonic_major, for_right_hand=True,
#                                expected=expected, show=False)
#         # All black note

#     def test_minor_seventh_arpeggio_A_right(self):
#         expected = (Fingering(for_right_hand=True).
#                     add_pinky_side(PianoNote.from_name("A ", finger=5)).
#                     add(PianoNote.from_name("A ", finger=1)).
#                     add(PianoNote.from_name("C ", finger=2)).
#                     add(PianoNote.from_name("E ", finger=3)).
#                     add(PianoNote.from_name("G ", finger=4)))
#         self.generation_helper(tonic=Note.from_name("A"), scale_pattern=minor_seven.to_arpeggio_pattern(),
#                                for_right_hand=True, expected=expected, show=False)

#     def test_minor_seventh_arpeggio_A_left(self):
#         expected = (Fingering(for_right_hand=False).
#                     add_pinky_side(PianoNote.from_name("A ", finger=4)).
#                     add(PianoNote.from_name("G ", finger=1)).
#                     add(PianoNote.from_name("E ", finger=2)).
#                     add(PianoNote.from_name("C ", finger=3)).
#                     add(PianoNote.from_name("A ", finger=4))
#                     )
#         self.generation_helper(tonic=Note.from_name("A2"), scale_pattern=minor_seven.to_arpeggio_pattern(),
#                                for_right_hand=False, expected=expected, show=False, key=Note.from_name("C"))

#     def test_minor_melodic_right(self):
#         self.generation_helper(Note.from_name("C"), minor_melodic, True, TestFingeringSymbol.right_minor_melodic_fingering, show=False,
#                                key=Note.from_name("E♭"))

#     def test_minor_melodic_left(self):
#         self.generation_helper(Note.from_name("C"), minor_melodic, False, TestFingeringSymbol.left_minor_melodic_fingering,
#                                key=Note.from_name("E♭"))

#     def test_augmented_major_seventh_arpeggio_f_left(self):
#         expected = (Fingering(for_right_hand=False).
#                     add_pinky_side(PianoNote.from_name("F2 ", finger=4)).
#                     add(PianoNote.from_name("A ", finger=3)).
#                     add(PianoNote.from_name("C# ", finger=2)).
#                     add(PianoNote.from_name("E ", finger=1)).
#                     add(PianoNote.from_name("F ", finger=4)))
#         self.generation_helper(Note.from_name("F2"), scale_pattern=augmented_major_seventh_chord.to_arpeggio_pattern(),
#                                for_right_hand=False, show=False, expected=expected)

#     def test_blues_c_d(self):
#         notes = blues.generate(Note.from_name("C")).notes + list(reversed(blues.generate(Note.from_name("D♭")).notes))
#         compile_(LiteralPianoLilyable.make(key=Note.from_name("c"), right_hand=notes).lily(), f"{self.test_folder}/c_d_blues",
#                  wav=False)()
#         right = generate_best_fingering_for_melody(notes, for_right_hand=True)
#         left = generate_best_fingering_for_melody(notes, for_right_hand=False)
#         print(left)
#         print(right)
