import unittest
from fretted_instrument.fretted_instrument.fretted_instruments import Gui_tar
from fretted_instrument.position.string.string import *


class TestFrettedInstrumentAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(Gui_tar.string(1), Gui_tar.string(1))
        self.assertNotEqual(Gui_tar.string(1), Gui_tar.string(2))
        self.assertEqual(Gui_tar.string(1) + 1, Gui_tar.string(2))
        self.assertEqual(Gui_tar.string(1) - 1, None)
        self.assertEqual(Gui_tar.string(1) + 6, None)

    def test_for_note(self):
        self.assertEqual(Gui_tar.string(1).fret_for_note(ChromaticNote.from_name("E3")), Gui_tar.fret(0))
        self.assertEqual(Gui_tar.string(1).fret_for_note(ChromaticNote.from_name("D#3")), None)
        self.assertEqual(Gui_tar.string(1).fret_for_note(ChromaticNote.from_name("F3")), Gui_tar.fret(1))
        self.assertEqual(Gui_tar.string(1).fret_for_note(ChromaticNote.from_name("E5")), Gui_tar.fret(24))
        self.assertEqual(Gui_tar.string(1).fret_for_note(ChromaticNote.from_name("F5")), None)

        self.assertEqual(Gui_tar.string(2).fret_for_note(ChromaticNote.from_name("E3")), None)
        self.assertEqual(Gui_tar.string(2).fret_for_note(ChromaticNote.from_name("D#3")), None)
        self.assertEqual(Gui_tar.string(2).fret_for_note(ChromaticNote.from_name("F3")), None)
        self.assertEqual(Gui_tar.string(2).fret_for_note(ChromaticNote.from_name("E5")), Gui_tar.fret(19))
        self.assertEqual(Gui_tar.string(2).fret_for_note(ChromaticNote.from_name("F5")), Gui_tar.fret(20))


    def test_lt(self):
        self.assertLess(Gui_tar.string(1), Gui_tar.string(2))