import unittest

from lily.staff.lily_single_note_staff import LilySingleNoteStaff
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from solfege.value.key.keys import key_of_C

class TestLilySingleNoteStaff(unittest.TestCase):
    def test_8_va(self):
        """`get_8_va` returns 0 within the treble staff's normal ambitus, and the number of octaves above F6
        otherwise."""
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("C4"), clef=Clef.TREBLE, first_key=key_of_C).get_8_va(), 0)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("E6"), clef=Clef.TREBLE, first_key=key_of_C).get_8_va(), 0)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("F6"), clef=Clef.TREBLE, first_key=key_of_C).get_8_va(), 1)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("E7"), clef=Clef.TREBLE, first_key=key_of_C).get_8_va(), 1)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("F7"), clef=Clef.TREBLE, first_key=key_of_C).get_8_va(), 2)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("A2"), clef=Clef.TREBLE, first_key=key_of_C).get_8_va(), 0)

    def test_8_vb(self):
        """`get_8_vb` returns 0 within the treble staff's normal ambitus, and the number of octaves below E3
        otherwise."""
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("D3"), clef=Clef.TREBLE, first_key=key_of_C).get_8_vb(), 1)


        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("C4"), clef=Clef.TREBLE, first_key=key_of_C).get_8_vb(), 0)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("E3"), clef=Clef.TREBLE, first_key=key_of_C).get_8_vb(), 0)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("E2"), clef=Clef.TREBLE, first_key=key_of_C).get_8_vb(), 1)
        self.assertEqual(LilySingleNoteStaff.make(note=Note.from_name("D2"), clef=Clef.TREBLE, first_key=key_of_C).get_8_vb(), 2)