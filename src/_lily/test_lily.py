"""Tests for `_lily/lily.py`. `test_indent` still passes (`indent` is re-exported from `utils.util`), but
`test_chord`/`test_compile`/`test_chord_compile` rely on `chord`/`compile_`, which no longer exist there (see
`_lily/README.md`) — moot for now anyway since this module fails to even collect under pytest (a separate,
pre-existing `'lily' is not a package` import-path issue, reproducible on a clean checkout)."""
import unittest
from _lily.lily import *

from sh import shell

class TestLily(unittest.TestCase):
    def setUp(self):
        """Build the two hand fixtures (`c_pentatonic_minor_5th_right`/`_left`) shared by the tests below."""
        from instruments.piano.piano_note import PianoNote

        self.c_pentatonic_minor_5th_right = [
            PianoNote.make(_chromatic=0, _diatonic=0, finger=1),
            PianoNote.make(_chromatic=3, _diatonic=2, finger=2),
            PianoNote.make(_chromatic=7, _diatonic=4, finger=3),
            PianoNote.make(_chromatic=12, _diatonic=7, finger=5),
        ]

        self.c_pentatonic_minor_5th_left = [
            PianoNote.make(_chromatic=-12, _diatonic=-7, finger=5),
            PianoNote.make(_chromatic=-9, _diatonic=-5, finger=3),
            PianoNote.make(_chromatic=-5, _diatonic=-3, finger=2),
            PianoNote.make(_chromatic=0, _diatonic=0, finger=1),
        ]

    both_hand_lily = """\\version "2.20.0"
\\score{
  #\\midi{}
  \\layout{}
  \\new PianoStaff<<
    \\new Staff{
      \\override Staff.TimeSignature.stencil = ##f
      \\omit Staff.BarLine
      \\omit PianoStaff.SpanBar
      \\time 30/4
      \\clef treble
      \\key g \\major
      c'-1 ees'-2 g'-3 c''-5
    }
    \\new Staff{
      \\override Staff.TimeSignature.stencil = ##f
      \\omit Staff.BarLine
      \\omit PianoStaff.SpanBar
      \\time 30/4
      \\set Staff.printKeyCancellation = ##f
      \\clef bass
      \\key g \\major
      c-5 ees-3 g-2 c'-1
    }
  >>
}"""

    chords_lily = """\\version "2.20.0"
\\score{
  #\\midi{}
  \\layout{}
  \\new Staff{
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef bass
    \\key ees \\major
    \\clef treble <
      c'
      ees'
      g'
    > \\clef treble <
      f'
      aes'
      c''
    >
  }
}"""

    def test_indent(self):
        """indent() prefixes every line of its input with two spaces."""
        self.assertEqual(indent("""foo
  bar"""), """  foo
    bar""")

    #
    # def test_for_list_of_notes(self):
    #     from instruments.piano.pianonote import PianoNote
    #     self.assertEqual(_for_list_of_notes([PianoNote.make(_chromatic=0, _diatonic=0, finger=1)], ),
    #                       "c'-1")
    #     self.assertEqual(_for_list_of_notes(self.c_pentatonic_minor_5th_right, ),
    #                       "c'-1 ees'-2 g'-3 c''-5")
    #
    # #
    # #     def test_staff(self):
    # #         self.assertEqual(
    # #             _staff(key="g", fingering=self.c_pentatonic_minor_5th_right, for_right_hand=True, ),
    # #             """\\new Staff{
    # #   \\clef treble
    # #   \\key g \\major
    # #   c'-1 ees'-2 g'-3 c''-5
    # # }"""
    #     # #         )
    #
    #     def test_lilypond_for_right(self):
    #         generated = lilypond_code_for_one_hand(key="g", notes_or_chords=self.c_pentatonic_minor_5th_right,
    #                                                for_right_hand=True
    #                                                , midi=False)
    #         self.assertEqual(
    #             generated,
    #             """\\version "2.20.0"
    # \\header{
    #   tagline=""
    # }
    # \\score{
    #   \\layout{}
    #   \\new Staff{
    #     \\clef treble
    #     \\key g \\major
    #     c'-1 ees'-2 g'-3 c''-5
    #   }
    # }"""
    # #         )
    #
    #     def test_lilypond_for_left(self):
    #         generated = lilypond_code_for_one_hand(key="g", notes_or_chords=self.c_pentatonic_minor_5th_left,
    #                                                for_right_hand=False, midi=False)
    #         self.assertEqual(
    #             generated,
    #             """\\version "2.20.0"
    # \\header{
    #   tagline=""
    # }
    # \\score{
    #   \\layout{}
    #   \\new Staff{
    #     \\clef bass
    #     \\key g \\major
    #     c-5 ees-3 g-2 c'-1
    #   }
    # }"""
    #         )
    #
    #     def test_lilypond_both_hands(self):
    #         generated = lilypond_code_for_two_hands(key="g", left_fingering=self.c_pentatonic_minor_5th_left,
    #                                                 right_fingering=self.c_pentatonic_minor_5th_right, midi=False)
    #         self.assertEqual(
    #             generated, """\
    # \\version "2.20.0"
    # \\header{
    #   tagline=""
    # }
    # \\score{
    #   \\layout{}
    #   \\new PianoStaff<<
    #     \\new Staff{
    #       \\clef treble
    #       \\key g \\major
    #       c'-1 ees'-2 g'-3 c''-5
    #     }
    #     \\new Staff{
    #       \\clef bass
    #       \\key g \\major
    #       c-5 ees-3 g-2 c'-1
    #     }
    #   >>
    # }"""
    #         )
    #
    #     def test_lilypond_for_left_and_midi(self):
    #         generated = lilypond_code_for_one_hand(key="g", notes_or_chords=self.c_pentatonic_minor_5th_left,
    #                                                for_right_hand=True, midi=True)
    #         expected = """\\version "2.20.0"
    # \\header{
    #   tagline=""
    # }
    # \\score{
    #   \\layout{}
    #   \\midi{}
    #   \\new Staff{
    #     \\clef treble
    #     \\key g \\major
    #     c-5 ees-3 g-2 c'-1
    #   }
    # }"""
    #         self.assertEqual(
    #             generated,
    #             expected
    #         )
    #
    #     def test_lilypond_chords_generate(self):
    #         from solfege.value.note.set_of_notes import TestSetOfNotes
    #         chords = [TestSetOfNotes.C_minor, TestSetOfNotes.F_minor]
    #         generated = lilypond_code_for_one_hand(key="ees", notes_or_chords=chords,
    #                                                for_right_hand=False, midi=True)
    #         self.assertEqual(
    #             generated,
    #             self.chords_lily
    #         )
    #
    #     def test_lilypond_both_hands_and_midi(self):
    #         generated = lilypond_code_for_two_hands(key="g", left_fingering=self.c_pentatonic_minor_5th_left,
    #                                                 right_fingering=self.c_pentatonic_minor_5th_right, midi=True)
    #         self.assertEqual(
    #             generated, """\\version "2.20.0"
    # \\header{
    #   tagline=""
    # }
    # \\score{
    #   \\layout{}
    #   \\midi{}
    #   \\new PianoStaff<<
    #     \\new Staff{
    #       \\clef treble
    #       \\key g \\major
    #       c'-1 ees'-2 g'-3 c''-5
    #     }
    #     \\new Staff{
    #       \\clef bass
    #       \\key g \\major
    #       c-5 ees-3 g-2 c'-1
    #     }
    #   >>
    # }"""
    #         )

    def test_chord(self):
        """chord() renders a list of simultaneous notes as one LilyPond `<...>` chord on a single staff."""
        generated = chord(self.c_pentatonic_minor_5th_right, )
        self.assertEqual(generated,
                          """\\version "2.20.0"
\\score{
  \\new Staff{
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef treble <
      c'-1ees'-2g'-3c''-5
    >
  }
}""")

    def test_compile(self):
        """compile_() writes the .ly source for a two-hand piece to disk and returns a callable that renders it to audio (played back via `vlc`, so this test requires manual audio verification)."""
        prefix_path = "test_arpeggio"
        lily_path = f"{prefix_path}.ly"
        if os.path.isfile(lily_path):
            os.remove(lily_path)  # in case it remains from failed test
        cmd = compile_(self.both_hand_lily, prefix_path, wav=True)
        self.assertTrue(os.path.isfile(lily_path))
        with open(lily_path, "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, self.both_hand_lily)
        cmd()
        shell(f"vlc {prefix_path}.wav&")

    def test_chord_compile(self):
        """Like test_compile, but for a chord (`chords_lily`) rather than a melodic two-hand piece."""
        prefix_path = "test_chords"
        lily_path = f"{prefix_path}.ly"
        if os.path.isfile(lily_path):
            os.remove(lily_path)  # in case it remains from failed test
        cmd = compile_(self.chords_lily, prefix_path, wav=True)
        self.assertTrue(os.path.isfile(lily_path))
        with open(lily_path, "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, self.chords_lily)
        cmd()
        shell(f"vlc {prefix_path}.wav&")
