import unittest

from solfege.value.note.note_alteration import NoteAlteration


class TestAlterationNote(unittest.TestCase):
    def test_from_name(self) -> None:
        """`from_name` parses known alteration symbols and rejects unknown ones."""
        self.assertEqual(NoteAlteration.from_name("𝄪"), NoteAlteration.make(2))
        self.assertEqual(NoteAlteration.from_name("#"), NoteAlteration.make(1))
        with self.assertRaises(Exception):
            self.assertEqual(NoteAlteration.from_name("###"), NoteAlteration.make(1))
