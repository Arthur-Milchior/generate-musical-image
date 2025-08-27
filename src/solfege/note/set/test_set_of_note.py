import unittest
from solfege.interval.interval import Interval
from solfege.note.note import Note
from solfege.note.set.set_of_notes import SetOfNotes


class TestSetOfNotes(unittest.TestCase):
    C_minor = SetOfNotes(
        [Note.from_name("C"),
         Note.from_name("E♭"),
         Note.from_name("G"),
         ])

    F_minor = SetOfNotes(
        [Note.from_name("F"),
         Note.from_name("A♭"),
         Note.from_name("C5"),
         ])

    def test_eq(self):
        self.assertNotEqual(self.C_minor, self.F_minor)
        self.assertEqual(self.C_minor, self.C_minor)

    def test_add(self):
        self.assertEqual(self.C_minor + Interval.make(diatonic=3, chromatic=5), self.F_minor)
