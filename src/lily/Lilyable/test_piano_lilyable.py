class TestPianoLilyable(unittest.TestCase):
    maxDiff = None
    value = LiteralPianoLilyable("aes", "cis", "gis'", "IV")
    both_hand_annotated_expected = r"""\version "2.20.0"
\score{
#\midi{}
\layout{}
<<
\new Lyrics {
  \lyricmode{
    IV
  }
}
\new PianoStaff<<
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef treble
    \key aes \major
    gis'
  }
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \omit Staff.BarLine
    \omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef bass
    \key aes \major
    cis
  }
>>
>>
}"""

    expected_right_hand = r"""\version "2.20.0"
\score{
<<
\new Staff{
  \override Staff.TimeSignature.stencil = ##f
  \omit Staff.BarLine
  \omit PianoStaff.SpanBar
  \set Staff.printKeyCancellation = ##f
  \clef treble
  \key aes \major
  gis'
}
>>
}"""

    def test_both_hand(self):
        generated = LiteralPianoLilyable("aes", "cis", "gis'", None).lily_in_scale()
        expected = r"""\version "2.20.0"
\score{
<<
\new PianoStaff<<
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \omit Staff.BarLine
    \omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef treble
    \key aes \major
    gis'
  }
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \omit Staff.BarLine
    \omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef bass
    \key aes \major
    cis
  }
>>
>>
}"""
        self.assertEquals(expected, generated)

    def test_right_hand(self):
        generated = LiteralPianoLilyable("aes", None, "gis'", None).lily()
        self.assertEquals(self.expected_right_hand, generated)
        test_file_path = f"{test_folder}/piano_lily_right"
        compile_(generated, test_file_path, True, force_recompile=True)()

    def test_both_hand_annotation(self):
        generated = LiteralPianoLilyable("aes", "cis", "gis'", "IV").lily(True)
        self.assertEquals(self.both_hand_annotated_expected, generated)
        test_file_path = f"{test_folder}/piano_lily_both"
        compile_(generated, test_file_path, True, force_recompile=True)()

    def test_eq_diff_class(self):
        class MockPianoLilyable(PianoLilyable):

            def first_key(self) -> str:
                return "aes"

            def right_lily(self) -> Optional[str]:
                """The lily code for the right hand scale, without the aes key"""
                return "gis'"

            def left_lily(self) -> Optional[str]:
                """The lily code for the left hand scale, without the aes key"""
                return "cis"

            def annotations_lily(self) -> Optional[str]:
                """The lily code for the annotation"""
                return "IV"

        self.assertEquals(self.value.first_key(), "aes")
        self.assertEquals(self.value.right_lily(), "gis'")
        self.assertEquals(self.value.left_lily(), "cis")
        self.assertEquals(self.value.annotations_lily(), "IV")
        self.assertEquals(self.value, MockPianoLilyable())

    def test_eq(self):
        self.assertEquals(self.value, LiteralPianoLilyable("aes", "cis", "gis'", "IV"))
