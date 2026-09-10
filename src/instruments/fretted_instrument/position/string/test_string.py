import unittest
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.string.string import *


class TestFrettedInstrumentAddString(unittest.TestCase):
    def test_eq(self) -> None:
        """Equality by string number, and `add`'s bounds-checking behavior."""
        self.assertEqual(Guitar.string(1), Guitar.string(1))
        self.assertNotEqual(Guitar.string(1), Guitar.string(2))
        self.assertEqual(Guitar.string(1).add(Guitar, 1), Guitar.string(2))
        self.assertEqual(Guitar.string(1).add(Guitar, -1), None)
        self.assertEqual(Guitar.string(1).add(Guitar,  6), None)

    def test_for_note(self) -> None:
        """`fret_for_note` finds the fret playing a note on a given string, or `None` if out of range."""
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("E3"), absolute=True), Fret.make(0, True))
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("D#3"), absolute=True), None)
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("F3"), absolute=True), Fret.make(1, True))
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("E5"), absolute=True), Fret.make(24, True))
        self.assertEqual(Guitar.string(1).fret_for_note(Guitar, ChromaticNote.from_name("F5"), absolute=True), None)

        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("E3"), absolute=True), None)
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("D#3"), absolute=True), None)
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("F3"), absolute=True), None)
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("E5"), absolute=True), Fret.make(19, True))
        self.assertEqual(Guitar.string(2).fret_for_note(Guitar, ChromaticNote.from_name("F5"), absolute=True), Fret.make(20, True))


    def test_lt(self) -> None:
        """Ordering follows the string number."""
        self.assertLess(Guitar.string(1), Guitar.string(2))