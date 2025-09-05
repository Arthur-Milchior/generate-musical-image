import unittest

from guitar.chord.guitar_chord import *
from .test_constants import *

class TestGuitarChord(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(GuitarChord.make([NOT_PLAYED] * 6), GuitarChord.make([NOT_PLAYED] * 6))
        self.assertNotEqual(GuitarChord.make([NOT_PLAYED] * 6), open)

    def test_get_fret(self):
        self.assertEqual(open.get_fret(strings[0]), OPEN_FRET)

    def test_get_frets(self):
        self.assertEqual(C.get_frets(), [NOT_PLAYED, Fret(3), Fret(0), Fret(2), Fret(1), Fret(0)])

    def test_repr(self):
        self.assertEqual(repr(C), "GuitarChord.make([None, 3, 0, 2, 1, 0])")
        
    def test_is_open(self):
        self.assertTrue(open.is_open())
        self.assertTrue(diag.is_open())
        self.assertFalse(ones.is_open())
        self.assertTrue(C.is_open())
        self.assertFalse(F.is_open())
        
    def test_is_barred(self):
        self.assertFalse(open.is_barred())
        self.assertFalse(diag.is_barred())
        self.assertTrue(ones.is_barred())
        self.assertFalse(diag_two.is_barred())
        self.assertFalse(C.is_barred())
        self.assertTrue(F.is_barred())
        
    def test_is_playable(self):
        self.assertTrue(open.is_playable())
        self.assertFalse(diag.is_playable())
        self.assertTrue(ones.is_playable())
        self.assertFalse(diag_two.is_playable())
        self.assertTrue(C.is_playable())
        self.assertTrue(F.is_playable())
        
    def test_chord_pattern_is_redundant(self):
        self.assertFalse(open.chord_pattern_is_redundant())
        self.assertFalse(diag.chord_pattern_is_redundant())
        self.assertFalse(ones.chord_pattern_is_redundant())
        self.assertTrue(diag_two.chord_pattern_is_redundant())
        self.assertFalse(C.chord_pattern_is_redundant())
        self.assertFalse(F.chord_pattern_is_redundant())

    def test_has_not_played_in_the_middle(self):
        self.assertFalse(GuitarChord.make([1, 3, 3, 4, 1, 1]).has_not_played_in_middle())
        self.assertTrue(GuitarChord.make([1, 3, 3, None, 1, 1]).has_not_played_in_middle())
        self.assertFalse(GuitarChord.make([None, 3, 3, 4, 1, 1]).has_not_played_in_middle())
        self.assertFalse(GuitarChord.make([None, 3, 3, 4, 1, None]).has_not_played_in_middle())
        self.assertFalse(GuitarChord.make([1, 3, 3, 4, 1, None]).has_not_played_in_middle())