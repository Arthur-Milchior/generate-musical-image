import unittest
from .generate import *

class TestChordSuccession(unittest.TestCase):
    maxDiff = None

    scale = Scale([
        Note("C"),
        Note("D"),
        Note("E"),
        Note("F"),
        Note("G"),
        Note("A"),
        Note("B"),
        Note("C5"),
        Note("D5"),
        Note("E5"),
        Note("F5"),
        Note("G5"),
        Note("A5"),
        Note("B5"),
        Note("C6"),
    ], pattern=major_scale)

    triad_right_succession = [
        SetOfNotes(
            [
                Note("C"),
                Note("E"),
                Note("G"),
            ],
            Note("C"),
        ),
        SetOfNotes(
            [
                Note("D"),
                Note("F"),
                Note("A"),
            ],
            Note("D"),
        ),
        SetOfNotes(
            [
                Note("E"),
                Note("G"),
                Note("B"),
            ],
            Note("E"),
        ),
        SetOfNotes(
            [
                Note("F"),
                Note("A"),
                Note("C5"),
            ],
            Note("F"),
        ),
        SetOfNotes(
            [
                Note("G"),
                Note("B"),
                Note("D5"),
            ],
            Note("G"),
        ),
        SetOfNotes(
            [
                Note("A"),
                Note("C5"),
                Note("E5"),
            ],
            Note("A"),
        ),
        SetOfNotes(
            [
                Note("B"),
                Note("D5"),
                Note("F5"),
            ],
            Note("B"),
        ),
        SetOfNotes(
            [
                Note("C5"),
                Note("E5"),
                Note("G5"),
            ],
            Note("C5"),
        ),
    ]

    lily_right_c_triad = """\
\\version "2.20.0"
\\score{
  <<
    \\new Staff{
      \\override Staff.TimeSignature.stencil = ##f
      \\omit Staff.BarLine
      \\omit PianoStaff.SpanBar
      \\time 30/4
      \\set Staff.printKeyCancellation = ##f
      \\clef treble
      \\key c \\major
      <c' e' g'> <d' f' a'> <e' g' b'> <f' a' c''> <g' b' d''> <a' c'' e''> <b' d'' f''> <c'' e'' g''>
    }
  >>
}"""

    lily_left_c_triad = """\
\\version "2.20.0"
\\score{
  <<
    \\new Staff{
      \\override Staff.TimeSignature.stencil = ##f
      \\omit Staff.BarLine
      \\omit PianoStaff.SpanBar
      \\time 30/4
      \\set Staff.printKeyCancellation = ##f
      \\clef bass
      \\key c \\major
      <c e g> <d f a> <e g b> <f a c'> <g b d'> <a c' e'> <b d' f'> <c' e' g'>
    }
  >>
}"""

    lily_both_c_triad = """\
\\version "2.20.0"
\\score{
  <<
    \\new PianoStaff<<
      \\new Staff{
        \\override Staff.TimeSignature.stencil = ##f
        \\omit Staff.BarLine
        \\omit PianoStaff.SpanBar
        \\time 30/4
        \\set Staff.printKeyCancellation = ##f
        \\clef treble
        \\key c \\major
        <c' e' g'> <d' f' a'> <e' g' b'> <f' a' c''> <g' b' d''> <a' c'' e''> <b' d'' f''> <c'' e'' g''>
      }
      \\new Staff{
        \\override Staff.TimeSignature.stencil = ##f
        \\omit Staff.BarLine
        \\omit PianoStaff.SpanBar
        \\time 30/4
        \\set Staff.printKeyCancellation = ##f
        \\clef bass
        \\key c \\major
        <c e g> <d f a> <e g b> <f a c'> <g b d'> <a c' e'> <b d' f'> <c' e' g'>
      }
    >>
  >>
}"""

    def test_chord_from_scale_pattern_and_position_key(self):
        son = chord_from_scale_pattern_and_position_key(
            self.scale,
            chord_pattern=triad,
            position=3,
        )
        self.assertEqual(son, SetOfNotes(
            [
                Note("F"),
                Note("A"),
                Note("C5"),
            ],
            Note("F"),
        ))

    def test_chord_succession_from_scale_pattern_and_position_key(self):
        suc = chord_succession_from_scale_pattern_and_position_key(
            self.scale,
            chord_pattern=triad,
            nb_of_chords=8,
        )
        self.assertEqual(suc,
                          self.triad_right_succession
                          )

    def test_succession_for_hands_key_pattern_direction_right(self):
        suc = succession_for_hands_key_pattern_direction(
            "folder", Note("C"), self.triad_right_succession, triad, for_left_hand=False, for_right_hand=True,
            direction="increasing", midi=False
        )
        expected = CardContent("C______right_triad_increasing", "folder/C______right_triad_increasing",
                                      self.lily_right_c_triad)
        self.assertEqual(suc, expected)

    def test_succession_for_hands_key_pattern_direction_both(self):
        suc = succession_for_hands_key_pattern_direction(
            "folder", Note("C"), self.triad_right_succession, triad, for_left_hand=True, for_right_hand=True,
            direction="increasing", midi=False
        )
        self.assertEqual(suc.lily_code, self.lily_both_c_triad)
        self.assertEqual(suc,
                          CardContent("C______both_triad_increasing", "folder/C______both_triad_increasing",
                                      self.lily_both_c_triad)
                          )

    def test_succession_for_hands_key_pattern_direction_left(self):
        suc = succession_for_hands_key_pattern_direction(
            "folder", Note("C"), self.triad_right_succession, triad, for_left_hand=True, for_right_hand=False,
            direction="increasing", midi=False
        )
        cc = CardContent("C______left_triad_increasing", "folder/C______left_triad_increasing",
                                      self.lily_left_c_triad)
        print(suc)
        print(cc)
        self.assertEqual(suc, cc)
