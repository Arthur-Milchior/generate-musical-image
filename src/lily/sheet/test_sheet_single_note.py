import unittest

from lily import staff
from lily.sheet.lily_chord_sheet import LilyChordSheet
from lily.staff.lily_single_note_staff import LilySingleNoteStaff
from solfege.value.key.keys import key_of_C
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note

class TestLilySheetSingleNote(unittest.TestCase):
    def test_single_note(self):
        C4 = Note.make(0, 0)
        sheet = LilyChordSheet.make(staff=LilySingleNoteStaff.make(note=C4, clef=Clef.TREBLE, first_key=key_of_C))
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
    c'
  >
}"""
        self.assertEqual(actual_code, expected_code)

        actual_name = sheet.file_prefix()
        expected_name = "chord_C____________4"
        self.assertEqual(actual_name, expected_name)