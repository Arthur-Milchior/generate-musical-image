import unittest

from lily import staff
from lily.sheet.lily_chord_sheet import LilyChordSheet
from lily.staff.lily_chord_staff import LilyChordStaff
from solfege.value.key.keys import key_of_C
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note

class TestLilyChordSheet(unittest.TestCase):
    def test_single_note(self):
        sheet = LilyChordSheet.make(staff=LilyChordStaff.make(notes=["C4", "E4", "G4"], clef=Clef.TREBLE, first_key=key_of_C))
        actual_code = sheet.lily_code()
        expected_code = """\\version "2.24.3"
\\new Staff{
  \\override Staff.TimeSignature.stencil = ##f
  \\omit Staff.BarLine
  \\omit PianoStaff.SpanBar
  \\time 30/4
  \\set Staff.printKeyCancellation = ##f
  \\clef treble
  \\key c \major
  <
    c' e' g'
  >
}"""
        self.assertEqual(actual_code, expected_code)

        actual_name = sheet.file_prefix()
        expected_name = "chord_C____________4_E____________4_G____________4"
        self.assertEqual(actual_name, expected_name)