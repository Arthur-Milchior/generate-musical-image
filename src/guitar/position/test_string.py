import unittest
from guitar.position.string import *

class TestGuitarAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(String.E3, String.E3)
        self.assertNotEqual(String.E3, String.A3)
        self.assertEqual(String.E3 + 1, String.A3)
        self.assertEqual(String.E3 - 1, None)
        self.assertEqual(String.E3 + 6, None)

    def test_for_note(self):
        self.assertEqual(String.E3.fret_for_note(ChromaticNote.from_name("E3")), Fret(0))
        self.assertEqual(String.E3.fret_for_note(ChromaticNote.from_name("D#3")), None)
        self.assertEqual(String.E3.fret_for_note(ChromaticNote.from_name("F3")), Fret(1))
        self.assertEqual(String.E3.fret_for_note(ChromaticNote.from_name("E5")), Fret(24))
        self.assertEqual(String.E3.fret_for_note(ChromaticNote.from_name("F5")), None)

        self.assertEqual(String.A3.fret_for_note(ChromaticNote.from_name("E3")), None)
        self.assertEqual(String.A3.fret_for_note(ChromaticNote.from_name("D#3")), None)
        self.assertEqual(String.A3.fret_for_note(ChromaticNote.from_name("F3")), None)
        self.assertEqual(String.A3.fret_for_note(ChromaticNote.from_name("E5")), Fret(19))
        self.assertEqual(String.A3.fret_for_note(ChromaticNote.from_name("F5")), Fret(20))


    def test_lt(self):
        self.assertLess(String.E3, String.A3)