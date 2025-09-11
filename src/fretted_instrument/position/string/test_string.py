import unittest
from fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from fretted_instrument.position.string.string import *


class TestFrettedInstrumentAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(Guitar.string(1), Guitar.string(1))
        self.assertNotEqual(Guitar.string(1), Guitar.string(2))
        self.assertEqual(Guitar.string(1).add(Guitar, 1), Guitar.string(2))
        self.assertEqual(Guitar.string(1).add(Guitar, -1), None)
        self.assertEqual(Guitar.string(1).add(Guitar,  6), None)

    def test_for_note(self):
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("E3")), Guitar.fret(0))
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("D#3")), None)
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("F3")), Guitar.fret(1))
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("E5")), Guitar.fret(24))
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("F5")), None)

        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("E3")), None)
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("D#3")), None)
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("F3")), None)
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("E5")), Guitar.fret(19))
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("F5")), Guitar.fret(20))


    def test_lt(self):
        self.assertLess(Guitar.string(1), Guitar.string(2))