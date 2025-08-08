import unittest
from .note import *

class TestNoteWithTonic(unittest.TestCase):
    C4 = NoteWithTonic(chromatic=0, diatonic = 0, tonic=True)
    D4 = NoteWithTonic(chromatic=2, diatonic = 1, tonic=C4)
    B3 = NoteWithTonic(chromatic=-1, diatonic = -1, tonic=C4)
    E4 = NoteWithTonic(chromatic=4, diatonic = 2, tonic=C4)
    F4 = NoteWithTonic(chromatic=5, diatonic = 3, tonic=C4)
    C5 = NoteWithTonic(chromatic=12, diatonic = 7, tonic=C4)
    B4 = NoteWithTonic(chromatic=11, diatonic = 6, tonic=C4)
    D3 = NoteWithTonic(chromatic=-10, diatonic = 6, tonic=C4)
    C3 = NoteWithTonic(chromatic=-12, diatonic = -7, tonic=C4)
    B2 = NoteWithTonic(chromatic=-13, diatonic = -8, tonic=C4)
    def test_eq(self):
        zero = NoteWithTonic(chromatic=0, diatonic=0, tonic=True)
        self.assertEqual(zero.get_chromatic().get_number(), 0)
        self.assertEqual(zero.get_diatonic().get_number(), 0)
        self.assertEqual(zero.get_tonic(), zero)

    def test_add_octave(self):
        self.assertEqual(self.C5.add_octave(-1), self.C4)
        self.assertEqual(self.C4.add_octave(1), self.C5)
        self.assertEqual(self.C5.add_octave(-2), self.C3)
        self.assertEqual(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        self.assertEqual(self.C5.get_in_base_octave(), self.C4)
        self.assertEqual(self.C3.get_in_base_octave(), self.C4)
        self.assertEqual(self.C4.get_in_base_octave(), self.C4)
        self.assertEqual(self.D4.get_in_base_octave(), self.D4)
        self.assertEqual(self.B3.get_in_base_octave(), self.B4)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.D4.equals_modulo_octave(self.C4))
        self.assertFalse(self.D4.equals_modulo_octave(self.C5))
        self.assertFalse(self.D4.equals_modulo_octave(self.C3))
        self.assertFalse(self.D4.equals_modulo_octave(self.B3))
        self.assertTrue(self.C4.equals_modulo_octave(self.C4))
        self.assertTrue(self.C4.equals_modulo_octave(self.C5))
        self.assertTrue(self.C4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C5.equals_modulo_octave(self.C3))
