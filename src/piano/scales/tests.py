import os
import pathlib
import unittest

from lily.svg import display_svg_file
from piano.pianonote import PianoNote
from piano.scales import fingering, generate, penalty
from piano.scales.__main__ import \
    generate_score_fixed_pattern_first_note_direction_number_of_octaves_left_or_right_or_both, \
    INCREASING, generate_score_fixed_pattern_first_note_direction_number_of_octaves, \
    generate_score_fixed_pattern_first_note_number_of_octaves, generate_score_fixed_pattern_first_note, \
    ScoreFixedPatternFirstNote, MissingFingering, generate_score_fixed_pattern
from piano.scales.fingering import Fingering
from solfege.chord.chord_pattern import minor_triad
from solfege.note import Note
from utils import util
from utils.constants import test_folder
from utils.util import tests_modules

tests_modules([fingering, generate, penalty])


class TestGeneration(unittest.TestCase):
    maxDiff = None
    execute_lily = True
    folder_scale = f"{test_folder}/Minor_arpeggio"
    folder_note_scale = f"{folder_scale}/F_____"
    pathlib.Path(folder_note_scale).mkdir(parents=True, exist_ok=True)
    scale_lowest_note = Note("F3")
    file_prefix_both_hands = f"{folder_note_scale}/Minor_arpeggio-F_____-two_hands-1-increasing"
    file_prefix_left_hand = f"{folder_note_scale}/Minor_arpeggio-F_____-left_hand-1-increasing"
    lilypond_path_both_hands = f"{file_prefix_both_hands}.ly"
    lilypond_path_left_hand = f"{file_prefix_left_hand}.ly"
    svg_both_hands_path = f"{file_prefix_both_hands}.svg"
    wav_both_hands_path = f"{file_prefix_both_hands}.wav"
    svg_left_hand_path = f"{file_prefix_left_hand}.svg"
    lily_code_both_hands = """\\version "2.20.0"
\\score{
  \\midi{}
  \\layout{}
  <<
    \\new PianoStaff<<
      \\new Staff{
        \\set Staff.printKeyCancellation = ##f
        \\clef treble
        \\key aes \\major
        f-1 aes-2 c'-4 f'-5
      }
      \\new Staff{
        \\set Staff.printKeyCancellation = ##f
        \\clef bass
        \\key aes \\major
        f,-5 aes,-4 c-2 f-1
      }
    >>
  >>
}"""
    lily_code_left_hand = """\\version "2.20.0"
\\score{
  \\midi{}
  \\layout{}
  <<
    \\new Staff{
      \\set Staff.printKeyCancellation = ##f
      \\clef bass
      \\key aes \\major
      f,-5 aes,-4 c-2 f-1
    }
  >>
}"""
    left_fingering = (Fingering(for_right_hand=False)
    .add_pinky_side(
        Note(chromatic=5, diatonic=3), finger=5)
    .add(
        Note(chromatic=8, diatonic=5), finger=4)
    .add(
        Note(chromatic=12, diatonic=7), finger=2)
    .add(
        Note(chromatic=17, diatonic=10), finger=1))
    right_fingering = (Fingering(for_right_hand=True)
    .add_pinky_side(
        Note(chromatic=17, diatonic=10), finger=5)
    .add(
        Note(chromatic=12, diatonic=7), finger=4)
    .add(
        Note(chromatic=8, diatonic=5), finger=2)
    .add(
        Note(chromatic=5, diatonic=3), finger=1))

    def clean_example(self):
        util.delete_file_if_exists(self.lilypond_path_both_hands)
        util.delete_file_if_exists(self.svg_both_hands_path)
        util.delete_file_if_exists(self.lilypond_path_left_hand)
        util.delete_file_if_exists(self.svg_left_hand_path)

    scale_note_index_path = f"{folder_note_scale}/index.html"
    scale_index_path = f"{folder_scale}/index.html"
    index_path = f"{test_folder}/index.html"
    anki_path = f"{folder_scale}/anki.csv"
    anki_csv = """Minor arpeggio,A  ,<img src='Minor_arpeggio-A_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-A_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-A_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-A_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-A_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-A_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-A_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-A_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-A_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-A_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-A_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-A_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-A_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-A_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-A_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-A_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-A_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-A_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-A_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-A_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-A_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-A_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-A_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-A_____-two_hands-2-reverse.svg'>
Minor arpeggio,D  ,<img src='Minor_arpeggio-D_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-D_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-D_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-D_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-D_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-D_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-D_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-D_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-D_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-D_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-D_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-D_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-D_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-D_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-D_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-D_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-D_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-D_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-D_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-D_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-D_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-D_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-D_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-D_____-two_hands-2-reverse.svg'>
Minor arpeggio,E  ,<img src='Minor_arpeggio-E_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-E_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-E_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-E_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-E_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-E_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-E_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-E_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-E_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-E_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-E_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-E_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-E_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-E_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-E_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-E_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-E_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-E_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-E_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-E_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-E_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-E_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-E_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-E_____-two_hands-2-reverse.svg'>
Minor arpeggio,G  ,<img src='Minor_arpeggio-G_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-G_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-G_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-G_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-G_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-G_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-G_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-G_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-G_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-G_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-G_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-G_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-G_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-G_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-G_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-G_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-G_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-G_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-G_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-G_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-G_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-G_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-G_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-G_____-two_hands-2-reverse.svg'>
Minor arpeggio,B  ,<img src='Minor_arpeggio-B_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-B_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-B_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-B_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-B_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-B_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-B_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-B_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-B_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-B_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-B_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-B_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-B_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-B_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-B_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-B_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-B_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-B_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-B_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-B_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-B_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-B_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-B_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-B_____-two_hands-2-reverse.svg'>
Minor arpeggio,C  ,<img src='Minor_arpeggio-C_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-C_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-C_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-C_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-C_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-C_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-C_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-C_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-C_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-C_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-C_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-C_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-C_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-C_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-C_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-C_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-C_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-C_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-C_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-C_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-C_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-C_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-C_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-C_____-two_hands-2-reverse.svg'>
Minor arpeggio,F# ,<img src='Minor_arpeggio-Fsharp-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-1-total.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-1-total.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-1-total.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-2-total.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-2-total.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-2-total.svg'>,<img src='Minor_arpeggio-Fsharp-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Fsharp-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Fsharp-two_hands-2-reverse.svg'>
Minor arpeggio,F  ,<img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-F_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-reverse.svg'>
Minor arpeggio,C# ,<img src='Minor_arpeggio-Csharp-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-1-total.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-1-total.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-1-total.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-2-total.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-2-total.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-2-total.svg'>,<img src='Minor_arpeggio-Csharp-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Csharp-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Csharp-two_hands-2-reverse.svg'>
Minor arpeggio,B♭ ,<img src='Minor_arpeggio-Bflat_-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-1-total.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-1-total.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-1-total.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-2-total.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-2-total.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-2-total.svg'>,<img src='Minor_arpeggio-Bflat_-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Bflat_-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Bflat_-two_hands-2-reverse.svg'>
Minor arpeggio,G# ,<img src='Minor_arpeggio-Gsharp-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-1-total.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-1-total.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-1-total.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-2-total.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-2-total.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-2-total.svg'>,<img src='Minor_arpeggio-Gsharp-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Gsharp-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Gsharp-two_hands-2-reverse.svg'>
Minor arpeggio,D# ,<img src='Minor_arpeggio-Dsharp-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-1-total.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-1-total.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-1-total.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-2-total.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-2-total.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-2-total.svg'>,<img src='Minor_arpeggio-Dsharp-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Dsharp-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-Dsharp-two_hands-2-reverse.svg'>"""
    scale_index_code = """<html>
  <head>
    <title>
      Fingerings of Minor arpeggio
    </title>
  </head>
  <body>
    <header>
      <h1>
        Fingerings of Minor arpeggio
      </h1>
    </header>
    <ul>
      <li><a href='A♭'>A♭</a></li>
      <li><a href='B♭'>B♭</a></li>
      <li><a href='F'>F</a></li>
      <li><a href='C'>C</a></li>
      <li><a href='G'>G</a></li>
      <li><a href='D'>D</a></li>
      <li><a href='A'>A</a></li>
      <li><a href='E'>E</a></li>
      <li><a href='B'>B</a></li>
      <li><a href='F#'>F#</a></li>
      <li><a href='C#'>C#</a></li>
      <li><a href='G#'>G#</a></li>
      <li><a href='A#'>A#</a></li>    </ul>
    <footer>
      <a href="../about.html"/>About</a><br/>
      <a href='..'>Other scales</a>
    </footer>
  </body>
</html>"""
    index_code = """"""
    scale_note_index_code = """\
<html>
  <head>
    <title>
      Fingerings of F   Minor arpeggio
    </title>
  </head>
  <body>
    <header>
      <h1>
        Fingerings of F   Minor arpeggio
      </h1>
    </header>
    <ul>
      <li><a href='Minor_arpeggio-F_____-left_hand-1-increasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-1-increasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-1-increasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-1-decreasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-decreasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-1-decreasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-decreasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-1-decreasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-decreasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-1-total.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-total.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-1-total.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-total.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-1-total.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-total.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-1-reverse.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-reverse.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-1-reverse.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-reverse.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-1-reverse.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-reverse.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-2-increasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-2-increasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-2-increasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-2-increasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-2-increasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-2-increasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-2-decreasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-2-decreasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-2-decreasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-2-decreasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-2-decreasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-2-decreasing.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-2-total.ly'/><img src='Minor_arpeggio-F_____-left_hand-2-total.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-2-total.ly'/><img src='Minor_arpeggio-F_____-right_hand-2-total.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-2-total.ly'/><img src='Minor_arpeggio-F_____-two_hands-2-total.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-left_hand-2-reverse.ly'/><img src='Minor_arpeggio-F_____-left_hand-2-reverse.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-right_hand-2-reverse.ly'/><img src='Minor_arpeggio-F_____-right_hand-2-reverse.svg'></a></li>
      <li><a href='Minor_arpeggio-F_____-two_hands-2-reverse.ly'/><img src='Minor_arpeggio-F_____-two_hands-2-reverse.svg'></a></li>    </ul>
    <footer>
      <a href="../../about.html"/>About</a><br/>
      <a href='..'>Same scale with other first note</a>
      <a href='../..'>Other scales</a>
    </footer>
  </body>
</html>"""

    minor_arpeggio = minor_triad.to_arpeggio_pattern()

    def check_anki_exists(self):
        with open(self.anki_path) as file:
            self.assertEquals(self.anki_csv, file.read())

    def check_scale_note_index_exists(self):
        with open(self.scale_note_index_path) as file:
            self.assertEquals(self.scale_note_index_code, file.read())
        self.assertTrue(os.path.exists(self.scale_note_index_path))
        os.system(f"chromium {self.scale_note_index_path}")

    def check_scale_index_exists(self):
        pass
        # self.assertTrue(os.path.exists(self.scale_index_path))
        # with open(self.scale_index_path) as file:
        #     self.assertEquals(self.scale_index_code, file.read())
        # os.system(f"chromium {self.scale_index_path}")

    def check_index_exists(self):
        pass
        # self.assertTrue(os.path.exists(self.index_path))
        # with open(self.index_path) as file:
        #     self.assertEquals(self.index_code, file.read())
        # os.system(f"chromium {self.index_path}")

    def check_pentatonic_major_two_hands_increasing_F_exists(self, expect_compiled: bool):
        with open(self.lilypond_path_both_hands) as file:
            self.assertEquals(self.lily_code_both_hands, file.read())
        if expect_compiled:
            self.assertTrue(os.path.exists(self.svg_both_hands_path))
            self.assertTrue(os.path.exists(self.wav_both_hands_path))
            display_svg_file(self.svg_both_hands_path)

    def check_pentatonic_major_left_hand_increasing_F_exists(self, expect_compiled: bool):
        with open(self.lilypond_path_left_hand) as file:
            self.assertEquals(self.lily_code_left_hand, file.read())
        if expect_compiled:
            self.assertTrue(os.path.exists(self.svg_left_hand_path))
            display_svg_file(self.svg_left_hand_path)

    def test_generate_score_fixed_pattern_first_note_direction_number_of_octaves_left_or_right_or_both(self):
        self.clean_example()
        output_both_hands = generate_score_fixed_pattern_first_note_direction_number_of_octaves_left_or_right_or_both(
            scale_name="Minor_arpeggio", folder_path=self.folder_note_scale, scale_lowest_note=self.scale_lowest_note,
            show_right=True,
            show_left=True,
            number_of_octaves=1, direction=INCREASING, lily_code=self.lily_code_both_hands,
            execute_lily=self.execute_lily,
            wav=True)
        _ = generate_score_fixed_pattern_first_note_direction_number_of_octaves_left_or_right_or_both(
            scale_name="Minor_arpeggio", folder_path=self.folder_note_scale,
            scale_lowest_note=self.scale_lowest_note.add_octave(-1),
            show_right=False,
            show_left=True,
            number_of_octaves=1, direction=INCREASING, lily_code=self.lily_code_left_hand,
            execute_lily=self.execute_lily,
            wav=True)
        self.assertEquals(output_both_hands.image_tag, f"<img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'>")
        self.assertEquals(output_both_hands.html_line,
                          f"<li><a href='Minor_arpeggio-F_____-two_hands-1-increasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'></a></li>")
        self.check_pentatonic_major_two_hands_increasing_F_exists(expect_compiled=self.execute_lily)
        self.check_pentatonic_major_left_hand_increasing_F_exists(expect_compiled=self.execute_lily)

    def test_generate_score_fixed_pattern_first_note_direction_number_of_octaves(self):
        self.clean_example()
        output = generate_score_fixed_pattern_first_note_direction_number_of_octaves(key="aes",
                                                                                     scale_lowest_note=self.scale_lowest_note,
                                                                                     left_scale_fingering=[
                                                                                         PianoNote(chromatic=-19,
                                                                                                   diatonic=-11,
                                                                                                   finger=5),
                                                                                         PianoNote(chromatic=-16,
                                                                                                   diatonic=-9,
                                                                                                   finger=4),
                                                                                         PianoNote(chromatic=-12,
                                                                                                   diatonic=-7,
                                                                                                   finger=2),
                                                                                         PianoNote(chromatic=-7,
                                                                                                   diatonic=-4,
                                                                                                   finger=1),
                                                                                     ],
                                                                                     right_scale_fingering=[
                                                                                         PianoNote(chromatic=-7,
                                                                                                   diatonic=-4,
                                                                                                   finger=1),
                                                                                         PianoNote(chromatic=-4,
                                                                                                   diatonic=-2,
                                                                                                   finger=2),
                                                                                         PianoNote(chromatic=0,
                                                                                                   diatonic=0,
                                                                                                   finger=4),
                                                                                         PianoNote(chromatic=5,
                                                                                                   diatonic=3,
                                                                                                   finger=5),
                                                                                     ],
                                                                                     scale_name="Minor_arpeggio",
                                                                                     folder_path=self.folder_note_scale,
                                                                                     number_of_octaves=1,
                                                                                     direction=INCREASING,
                                                                                     execute_lily=self.execute_lily,
                                                                                     wav=True
                                                                                     )
        self.assertEquals(output.image_tags,
                          ["<img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'>",
                           "<img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'>",
                           "<img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'>"])
        self.assertEquals(output.html_lines, [
            "<li><a href='Minor_arpeggio-F_____-left_hand-1-increasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-right_hand-1-increasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-two_hands-1-increasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'></a></li>"])
        self.check_pentatonic_major_two_hands_increasing_F_exists(expect_compiled=self.execute_lily)
        self.check_pentatonic_major_left_hand_increasing_F_exists(expect_compiled=self.execute_lily)

    def test_generate_score_fixed_pattern_first_note_number_of_octaves(self):
        self.clean_example()
        output = generate_score_fixed_pattern_first_note_number_of_octaves(key="aes",
                                                                           right_hand_lowest_note=self.scale_lowest_note,
                                                                           scale_pattern=minor_triad.to_arpeggio_pattern(),
                                                                           folder_path=self.folder_note_scale,
                                                                           number_of_octaves=1,
                                                                           left_fingering=self.left_fingering,
                                                                           right_fingering=self.right_fingering,
                                                                           execute_lily=self.execute_lily,
                                                                           wav=True
                                                                           )
        self.assertEquals(output.image_tags,
                          [
                              "<img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'>",
                              "<img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'>",
                              "<img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'>",
                              "<img src='Minor_arpeggio-F_____-left_hand-1-decreasing.svg'>",
                              "<img src='Minor_arpeggio-F_____-right_hand-1-decreasing.svg'>",
                              "<img src='Minor_arpeggio-F_____-two_hands-1-decreasing.svg'>",
                              "<img src='Minor_arpeggio-F_____-left_hand-1-total.svg'>",
                              "<img src='Minor_arpeggio-F_____-right_hand-1-total.svg'>",
                              "<img src='Minor_arpeggio-F_____-two_hands-1-total.svg'>",
                              "<img src='Minor_arpeggio-F_____-left_hand-1-reverse.svg'>",
                              "<img src='Minor_arpeggio-F_____-right_hand-1-reverse.svg'>",
                              "<img src='Minor_arpeggio-F_____-two_hands-1-reverse.svg'>",
                          ])
        self.assertEquals(output.html_lines, [
            "<li><a href='Minor_arpeggio-F_____-left_hand-1-increasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-right_hand-1-increasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-two_hands-1-increasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-left_hand-1-decreasing.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-decreasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-right_hand-1-decreasing.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-decreasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-two_hands-1-decreasing.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-decreasing.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-left_hand-1-total.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-total.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-right_hand-1-total.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-total.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-two_hands-1-total.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-total.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-left_hand-1-reverse.ly'/><img src='Minor_arpeggio-F_____-left_hand-1-reverse.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-right_hand-1-reverse.ly'/><img src='Minor_arpeggio-F_____-right_hand-1-reverse.svg'></a></li>",
            "<li><a href='Minor_arpeggio-F_____-two_hands-1-reverse.ly'/><img src='Minor_arpeggio-F_____-two_hands-1-reverse.svg'></a></li>",
        ])
        self.check_pentatonic_major_two_hands_increasing_F_exists(expect_compiled=self.execute_lily)
        self.check_pentatonic_major_left_hand_increasing_F_exists(expect_compiled=self.execute_lily)

    def test_generate_score_fixed_pattern_first_note(self):
        self.clean_example()
        output = generate_score_fixed_pattern_first_note(key="aes",
                                                         right_hand_lowest_note=self.scale_lowest_note,
                                                         scale_pattern=self.minor_arpeggio,
                                                         folder_path=self.folder_note_scale,
                                                         execute_lily=self.execute_lily,
                                                         wav=True,
                                                         )
        self.assertIsInstance(output,
                              ScoreFixedPatternFirstNote)
        self.assertEquals(output.anki_note_as_csv,

                          "Minor arpeggio,F  ,<img src='Minor_arpeggio-F_____-left_hand-1-increasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-increasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-increasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-decreasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-decreasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-1-total.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-total.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-total.svg'>,<img src='Minor_arpeggio-F_____-left_hand-1-reverse.svg'>,<img src='Minor_arpeggio-F_____-right_hand-1-reverse.svg'>,<img src='Minor_arpeggio-F_____-two_hands-1-reverse.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-increasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-increasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-increasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-decreasing.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-decreasing.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-total.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-total.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-total.svg'>,<img src='Minor_arpeggio-F_____-left_hand-2-reverse.svg'>,<img src='Minor_arpeggio-F_____-right_hand-2-reverse.svg'>,<img src='Minor_arpeggio-F_____-two_hands-2-reverse.svg'>",
                          )
        self.assertEquals(output.html_link_for_this_starting_note, "<li><a href='F_____'>F  </a></li>")
        self.check_pentatonic_major_two_hands_increasing_F_exists(expect_compiled=self.execute_lily)
        self.check_pentatonic_major_left_hand_increasing_F_exists(expect_compiled=self.execute_lily)
        self.check_scale_note_index_exists()

    # def test_fail_generate_score_fixed_pattern_first_note(self):
    #     output = generate_score_fixed_pattern_first_note(key="ges",
    #                                                      right_hand_lowest_note=Note(chromatic=3, diatonic=2),
    #                                                      scale_pattern=minor_arpeggio,
    #                                                      folder_path=self.folder_note_scale,
    #                                                      execute_lily=self.execute_lily,
    #                                                      wav=True,
    #                                                      )
    #     self.assertIsInstance(output, List)
    #     self.assertEquals(output,
    #                       [
    #                           MissingFingering(scale_pattern=minor_arpeggio,
    #                                            note=Note(chromatic=3, diatonic=2), for_right_hand=False),
    #                           MissingFingering(scale_pattern=minor_arpeggio,
    #                                            note=Note(chromatic=3, diatonic=2), for_right_hand=True),
    #                       ])

    def test_generate_score_fixed_pattern(self):
        minor_arpeggio = minor_triad.to_arpeggio_pattern()
        self.clean_example()
        output = (generate_score_fixed_pattern(scale_pattern=minor_arpeggio, folder_path=self.folder_scale,
                                               execute_lily=self.execute_lily, wav=True))
        self.assertEquals(output.html_link_for_this_scale_pattern,
                          "<li><a href='Minor_arpeggio'>Minor arpeggio</a></li>")
        self.assertEquals(output.missing_scores, [])
        self.check_anki_exists()
        self.check_scale_index_exists()
        self.check_scale_note_index_exists()
        self.check_pentatonic_major_two_hands_increasing_F_exists(expect_compiled=self.execute_lily)
        self.check_pentatonic_major_left_hand_increasing_F_exists(expect_compiled=self.execute_lily)
    #
    # def test_generate_score(self):
    #     # test generating all scores. Deactivated because FAR TOO SLOW
    #     self.clean_example()
    #     generate_scores(test_folder, execute_lily=self.execute_lily, wav=True)
    #     self.check_anki_exists()
    #     self.check_index_exists()
    #     self.check_scale_index_exists()
    #     self.check_scale_note_index_exists()
    #     self.check_pentatonic_major_two_hands_increasing_F_exists(expect_compiled=self.execute_lily)
    #     self.check_pentatonic_major_left_hand_increasing_F_exists(expect_compiled=self.execute_lily)
