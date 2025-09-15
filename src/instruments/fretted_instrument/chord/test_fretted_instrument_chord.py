import unittest

from instruments.fretted_instrument.chord.fretted_instrument_chord import *
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
        self.assertEqual(C4M.get_frets(Guitar), [not_played_fret, Guitar.fret(3), Guitar.fret(2), Guitar.fret(0), Guitar.fret(1), Guitar.fret(0)])

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
        self.assertEqual(C4M.playable(Guitar), Playable.EASY)
        self.assertEqual(open.playable(Guitar), Playable.EASY)
        self.assertEqual(diag.playable(Guitar), Playable.NO)
        self.assertEqual(ones.playable(Guitar), Playable.EASY)
        self.assertEqual(diag_two.playable(Guitar), Playable.NO)
        self.assertEqual(F4M.playable(Guitar), Playable.EASY)
        
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

    def test_svg(self):
        svg_content = F4M._svg_content(absolute=False, instrument=Guitar)
        expected = [
            '<line x1="43.5" y1="0" x2="43" y2="1164" stroke-width="5" stroke="black" /><!-- String 1-->',
       '<line x1="130.5" y1="0" x2="130" y2="1164" stroke-width="5" stroke="black" /><!-- String 2-->',
       '<line x1="217.5" y1="0" x2="217" y2="1164" stroke-width="5" stroke="black" /><!-- String 3-->',
       '<line x1="304.5" y1="0" x2="304" y2="1164" stroke-width="5" stroke="black" /><!-- String 4-->',
       '<line x1="391.5" y1="0" x2="391" y2="1164" stroke-width="5" stroke="black" /><!-- String 5-->',
       '<line x1="478.5" y1="0" x2="478" y2="1164" stroke-width="5" stroke="black" /><!-- String 6-->',
       '<line x1="0" y1="43" x2="522" y2="43" stroke-width="7" stroke="black" /><!--Fret 0-->',
       '<line x1="0" y1="423" x2="522" y2="423" stroke-width="7" stroke="black" /><!--Fret 1-->',
       '<line x1="0" y1="782" x2="522" y2="782" stroke-width="7" stroke="black" /><!--Fret 2-->',
       '<line x1="0" y1="1120" x2="522" y2="1120" stroke-width="7" stroke="black" /><!--Fret 3-->',
       '<circle cx="43" cy="233" r="32" fill="black" stroke="black" stroke-width="3"/><!-- String N° 1, position 1-->',
       '<circle cx="130" cy="951" r="32" fill="black" stroke="black" stroke-width="3"/><!-- String N° 2, position 3-->',
       '<circle cx="217" cy="951" r="32" fill="black" stroke="black" stroke-width="3"/><!-- String N° 3, position 3-->',
       '<circle cx="304" cy="602" r="32" fill="black" stroke="black" stroke-width="3"/><!-- String N° 4, position 2-->',
       '<circle cx="391" cy="233" r="32" fill="black" stroke="black" stroke-width="3"/><!-- String N° 5, position 1-->',
       '<circle cx="478" cy="233" r="32" fill="black" stroke="black" stroke-width="3"/><!-- String N° 6, position 1-->']
        self.assertEqual(expected, svg_content)
