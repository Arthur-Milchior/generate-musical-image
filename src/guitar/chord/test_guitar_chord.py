import unittest

from guitar.chord.guitar_chord import *
from guitar.position.fret.fret import NOT_PLAYED
from .test_constants import *

CM_ = GuitarChord.make([None, 3, 2, 0, 1, None])
CM = GuitarChord.make([None, 3, 2, 0, 1, 0])

class TestGuitarChord(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(GuitarChord.make([NOT_PLAYED] * 6), GuitarChord.make([NOT_PLAYED] * 6))
        self.assertNotEqual(GuitarChord.make([NOT_PLAYED] * 6), open)

    def test_get_fret(self):
        self.assertEqual(open.get_fret(strings[0]), OPEN_FRET)

    def test_get_frets(self):
        self.assertEqual(C4M.get_frets(), [NOT_PLAYED, Fret(3), Fret(2), Fret(0), Fret(1), Fret(0)])

    def test_repr(self):
        self.assertEqual(repr(C4M), "GuitarChord.make([None, 3, 2, 0, 1, 0])")
        
    def test_is_open(self):
        self.assertTrue(open.is_open())
        self.assertTrue(diag.is_open())
        self.assertFalse(ones.is_open())
        self.assertTrue(C4M.is_open())
        self.assertFalse(F4M.is_open())
        
    def test_is_transposable(self):
        self.assertFalse(open.is_transposable())
        self.assertFalse(diag.is_transposable())
        self.assertTrue(ones.is_transposable())
        self.assertTrue(diag_two.is_transposable())
        self.assertFalse(C4M.is_transposable())
        self.assertTrue(F4M.is_transposable())
        
    def test_is_barred(self):
        self.assertEqual(open.is_barred(), Barred.NO)
        self.assertEqual(diag.is_barred(), Barred.NO)
        self.assertEqual(ones.is_barred(), Barred.FULLY)
        self.assertEqual(diag_two.is_barred(), Barred.NO)
        self.assertEqual(C4M.is_barred(), Barred.NO)
        self.assertEqual(F4M.is_barred(), Barred.FULLY)
        
    def test_is_playable(self):
        self.assertEqual(open.playable(), Playable.EASY)
        self.assertEqual(diag.playable(), Playable.NO)
        self.assertEqual(ones.playable(), Playable.EASY)
        self.assertEqual(diag_two.playable(), Playable.NO)
        self.assertEqual(C4M.playable(), Playable.EASY)
        self.assertEqual(F4M.playable(), Playable.EASY)
        
    def test_chord_pattern_is_redundant(self):
        self.assertFalse(open.chord_pattern_is_redundant())
        self.assertFalse(diag.chord_pattern_is_redundant())
        self.assertFalse(ones.chord_pattern_is_redundant())
        self.assertTrue(diag_two.chord_pattern_is_redundant())
        self.assertFalse(C4M.chord_pattern_is_redundant())
        self.assertFalse(F4M.chord_pattern_is_redundant())

    def test_has_not_played_in_the_middle(self):
        self.assertFalse(GuitarChord.make([1, 3, 3, 4, 1, 1]).has_not_played_in_middle())
        self.assertTrue(GuitarChord.make([1, 3, 3, None, 1, 1]).has_not_played_in_middle())
        self.assertFalse(GuitarChord.make([None, 3, 3, 4, 1, 1]).has_not_played_in_middle())
        self.assertFalse(GuitarChord.make([None, 3, 3, 4, 1, None]).has_not_played_in_middle())
        self.assertFalse(GuitarChord.make([1, 3, 3, 4, 1, None]).has_not_played_in_middle())
        
    def test_lt(self):
        self.assertLess(CM_, CM)
        self.assertLessEqual(CM_, CM)
        self.assertLessEqual(CM_, CM_)