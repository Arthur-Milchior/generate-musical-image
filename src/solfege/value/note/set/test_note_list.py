import unittest

from .note_list import *

class TestNoteList(unittest.TestCase):
    def test_find_note(self):
        c4_major = NoteList.make([(0, 0), (4, 2), (7, 4)])
        self.assertEqual(c4_major.find_note_from_list_up_to_octave(ChromaticNote(0)), Note.make(0, 0))
        self.assertEqual(c4_major.find_note_from_list_up_to_octave(ChromaticNote(-12)), Note.make(-12, -7))