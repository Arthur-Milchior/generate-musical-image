import unittest

from guitar.chord.guitar_chord import *

open = GuitarChord.make([OPEN_FRET] * 6)
ones = GuitarChord.make([Fret(1)] * 6)
diag = GuitarChord.make([Fret(i) for i in range(6)])
diag_two = GuitarChord.make([Fret(i+2) for i in range(6)])

class TestGuitarChord(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(GuitarChord.make([NOT_PLAYED] * 6), GuitarChord.make([NOT_PLAYED] * 6))
        self.assertNotEqual(GuitarChord.make([NOT_PLAYED] * 6), open)

    def test_get_fret(self):
        self.assertEqual(open.get_fret(strings[0]), OPEN_FRET)
        
    def test_is_open(self):
        self.assertTrue(open.is_open())
        self.assertTrue(diag.is_open())
        self.assertFalse(ones.is_open())
        self.assertFalse(diag_two.is_open())
        
    def test_is_barred(self):
        self.assertFalse(open.is_barred())
        self.assertFalse(diag.is_barred())
        self.assertTrue(ones.is_barred())
        self.assertFalse(diag_two.is_barred())
        
    def test_is_playable(self):
        self.assertTrue(open.is_playable())
        self.assertFalse(diag.is_playable())
        self.assertTrue(ones.is_playable())
        self.assertFalse(diag_two.is_playable())