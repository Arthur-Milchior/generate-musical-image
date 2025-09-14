import os

from lily.lily import compile_
from instruments.piano.chord_successions.generate import successions
from utils import util
from sh import shell
from consts import generate_root_folder

if __name__ == '__main__':
    shell("echo $(pwd)")
    folder_path = f"{generate_root_folder}/piano/chord_successions"
    util.ensure_folder(folder_path)
    notes = successions(folder_path, midi=False)
    anki_csv = "\n".join(
        note.to_anki() for note in notes
    )
    for note in notes:
        for succession in note.successions:
            compile_(succession.lily_code, file_prefix=succession.filepath, wav=False)
    save_file(f"{folder_path}/anki.csv", anki_csv)

#
#
# class TestChordSuccessionGenerationMain(unittest.TestCase):
#     maxDiff = None
#     test_chord_folder = f"{test_folder}/chord_successions"
#     prefix = f"{test_chord_folder}/triad_in_C_____"
#     svg = f"{prefix}.svg"
#     wav = f"{prefix}.wav"
#     ly = f"{prefix}.ly"
#     anki = f"{test_chord_folder}/anki.csv"
#     lyly_code = """\\version "2.20.0"
# \\header{
#   tagline=""
# }
# \\score{
#   \\layout{}
#   \\midi{}
#   \\new Staff{
#     \\clef treble
#     \\key c \\major
#     \\clef treble <
#       c'
#       e'
#       g'
#     > \\clef treble <
#       d'
#       f'
#       a'
#     > \\clef treble <
#       e'
#       g'
#       b'
#     > \\clef treble <
#       f'
#       a'
#       c''
#     > \\clef treble <
#       g'
#       b'
#       d''
#     > \\clef treble <
#       a'
#       c''
#       e''
#     > \\clef treble <
#       b'
#       d''
#       f''
#     > \\clef treble <
#       c''
#       e''
#       g''
#     >
#   }
# }"""
#     util.ensure_folder(test_chord_folder)
#
#     def clean_example(self):
#         delete_file_if_exists(self.svg)
#         delete_file_if_exists(self.wav)
#         delete_file_if_exists(self.ly)
#         delete_file_if_exists(self.anki)
#
#     def check_compiled_file_exists(self):
#         with open(self.ly) as file:
#             self.assertEqual(self.lyly_code, file.read())
#         self.assertTrue(os.path.exists(self.svg))
#         display_svg_file(self.svg)
#         shell(f"vlc {self.wav}&")
#
#     def test_generate_pattern_tonic(self):
#         output = generate_chord_successions_pattern_tonic(
#             two_octave_scales=TestChordSuccession.two_octave_major_c4_scale,
#             chord_pattern=triad,
#             folder_path=self.test_chord_folder,
#             execute_lily=True,
#             wav=True,
#             key=Note.from_name("C"),
#         )
#         self.check_compiled_file_exists()
#         self.assertEqual(output, f"Play the triads in the C   major scale,<img src='triad_in_C_____.svg'>")
#
#     def test_generate_pattern(self):
#         generate_chord_successions_pattern(
#             chord_pattern=triad,
#             folder_path=self.test_chord_folder,
#             execute_lily=True,
#             wav=True,
#         )
#         self.check_compiled_file_exists()
#
#     def test_generate(self):
#         generate_chord_successions(
#             folder_path=self.test_chord_folder,
#             execute_lily=True,
#             wav=True,
#         )
#         self.check_compiled_file_exists()
#         self.assertTrue(os.path.exists(f"{self.test_chord_folder}/anki.csv"))
