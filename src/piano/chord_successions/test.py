import os
import unittest

import util
from piano.chord_successions.__main__ import generate_chord_successions_pattern_fundamental, \
    generate_chord_successions_pattern, generate_chord_successions
from piano.chord_successions.generate import TestChordSuccession, triad
from util import delete_file_if_exists


class TestGeneration(unittest.TestCase):
    test_folder = "test_files"
    prefix = f"{test_folder}/triad_in_C"
    svg = f"{prefix}.svg"
    wav = f"{prefix}.wav"
    ly = f"{prefix}.ly"
    anki = f"{test_folder}/anki.csv"
    lyly_code = """%%right hand fingering:['', '', '', '', '', '', '', '']
\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\layout{}
  \\midi{}
  \\new Staff{
    \\clef treble
    \\key c \\major
    \\clef treble <
      c'
      e'
      g'
    > \\clef treble <
      d'
      f'
      a'
    > \\clef treble <
      e'
      g'
      b'
    > \\clef treble <
      f'
      a'
      c''
    > \\clef treble <
      g'
      b'
      d''
    > \\clef treble <
      a'
      c''
      e''
    > \\clef treble <
      b'
      d''
      f''
    > \\clef treble <
      c''
      e''
      g''
    >
  }
}"""
    util.ensure_folder(test_folder)

    def clean_example(self):
        delete_file_if_exists(self.svg)
        delete_file_if_exists(self.wav)
        delete_file_if_exists(self.ly)
        delete_file_if_exists(self.anki)

    def check_compiled_file_exists(self):
        with open(self.ly) as file:
            self.assertEquals(self.lyly_code, file.read())
        self.assertTrue(os.path.exists(self.svg))
        os.system(f"eog {self.svg}")
        os.system(f"vlc {self.wav}")

    def test_generate_pattern_fundamental(self):
        output = generate_chord_successions_pattern_fundamental(
            two_octave_scales=TestChordSuccession.two_octave_major_c4_scale,
            chord_pattern=triad,
            folder_path=self.test_folder,
            execute_lily=True,
            wav=True,
            key_file="C",
            key_lily="c"
        )
        self.check_compiled_file_exists()
        self.assertEquals(output, f"triad,C,<img src='{self.svg}'>")

    def test_generate_pattern(self):
        generate_chord_successions_pattern(
            chord_pattern=triad,
            folder_path=self.test_folder,
            execute_lily=True,
            wav=True,
        )
        self.check_compiled_file_exists()

    def test_generate(self):
        generate_chord_successions(
            folder_path=self.test_folder,
            execute_lily=True,
            wav=True,
        )
        self.check_compiled_file_exists()
        self.assertTrue(os.path.exists(f"{self.test_folder}/anki.csv"))
