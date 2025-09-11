import unittest

from fretted_instrument.chord.fretted_instrument_chord import *
from .test_constants import *
from .test_constants import _make

CM_ = _make([None, 3, 2, 0, 1, None])
CM = _make([None, 3, 2, 0, 1, 0])

not_played_fret = Guitar.fret( value=None)

class TestFrettedInstrumentChord(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(_make([not_played_fret] * 6), _make([not_played_fret] * 6))
        self.assertNotEqual(_make([not_played_fret] * 6), open)

    def test_get_fret(self):
        self.assertEqual(open.get_fret(Guitar.string(1)), Guitar.fret( value=0))

    def test_get_frets(self):
        self.assertEqual(C4M.get_frets(), [not_played_fret, Guitar.fret(3), Guitar.fret(2), Guitar.fret(0), Guitar.fret(1), Guitar.fret(0)])

    def test_repr(self):
        self.assertEqual(repr(C4M), "FrettedInstrumentChord.make([None, 3, 2, 0, 1, 0])")
        
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
        self.assertEqual(C4M.playable(), Playable.EASY)
        self.assertEqual(open.playable(), Playable.EASY)
        self.assertEqual(diag.playable(), Playable.NO)
        self.assertEqual(ones.playable(), Playable.EASY)
        self.assertEqual(diag_two.playable(), Playable.NO)
        self.assertEqual(F4M.playable(), Playable.EASY)
        
    def test_chord_pattern_is_redundant(self):
        self.assertFalse(open.chord_pattern_is_redundant())
        self.assertFalse(diag.chord_pattern_is_redundant())
        self.assertFalse(ones.chord_pattern_is_redundant())
        self.assertTrue(diag_two.chord_pattern_is_redundant())
        self.assertFalse(C4M.chord_pattern_is_redundant())
        self.assertFalse(F4M.chord_pattern_is_redundant())

    def test_has_not_played_in_the_middle(self):
        self.assertFalse(_make([1, 3, 3, 4, 1, 1]).has_not_played_in_middle())
        self.assertTrue(_make([1, 3, 3, None, 1, 1]).has_not_played_in_middle())
        self.assertFalse(_make([None, 3, 3, 4, 1, 1]).has_not_played_in_middle())
        self.assertFalse(_make([None, 3, 3, 4, 1, None]).has_not_played_in_middle())
        self.assertFalse(_make([1, 3, 3, 4, 1, None]).has_not_played_in_middle())
        
    def test_lt(self):
        self.assertLess(CM_, CM)
        self.assertLessEqual(CM_, CM)
        self.assertLessEqual(CM_, CM_)