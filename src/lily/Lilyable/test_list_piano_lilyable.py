import unittest

from lily.Lilyable.test_piano_lilyable import TestPianoLilyable
from lily.Lilyable.list_piano_lilyable import *

class TestList(unittest.TestCase):
    maxDiff = None
    value = ListPianoLilyable(
        [
            TestPianoLilyable.value,
            LiteralPianoLilyable("aes", "gauche", "droit", "am"),
            LiteralPianoLilyable("c", "izquierda", "derecha", "b"),
        ],
    )

    def test_lily(self):
        lily = self.value.lily()
        self.assertEqual(r"""\version "2.20.0"
\score{
  <<
    \new Lyrics {
      \lyricmode{
        IV am b
      }
    }
    \new PianoStaff<<
      \new Staff{
        \override Staff.TimeSignature.stencil = ##f
        \omit Staff.BarLine
        \omit PianoStaff.SpanBar
        \set Staff.printKeyCancellation = ##f
        \clef treble
        \key aes \major
        gis' droit \key c \major derecha
      }
      \new Staff{
        \override Staff.TimeSignature.stencil = ##f
        \omit Staff.BarLine
        \omit PianoStaff.SpanBar
        \set Staff.printKeyCancellation = ##f
        \clef bass
        \key aes \major
        cis gauche \key c \major izquierda
      }
    >>
  >>
}""", lily)
        self.assertEqual(self.value.first_key(), "aes")
        self.assertEqual(self.value.right_lily(), r"""gis' droit \key c \major derecha""")
        self.assertEqual(self.value.left_lily(), r"""cis gauche \key c \major izquierda""")
        self.assertEqual(self.value.annotations_lily(), """IV am b""")

    def test_eq(self):
        expected = LiteralPianoLilyable("aes", r"""cis gauche \key c \major izquierda""", """gis' droit \key c \major derecha""", """IV am b""")
        self.assertEqual(self.value, expected)
