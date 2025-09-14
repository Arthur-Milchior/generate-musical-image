import unittest
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import *

open_fret = Guitar.fret( value=0)
not_played_fret = Guitar.fret( value=None)

class TestFrettedInstrumentAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(not_played_fret, not_played_fret)
        self.assertEqual(not_played_fret.add(Guitar, ChromaticInterval(4)), not_played_fret)
        self.assertNotEqual(not_played_fret, open_fret)
        self.assertNotEqual(open_fret.add(Guitar, ChromaticInterval(4)), open_fret)
        self.assertEqual(open_fret, open_fret)
        self.assertEqual(Guitar.fret(4).add(Guitar, ChromaticInterval(-5)), None)
        self.assertEqual(Guitar.fret(4).add(Guitar, ChromaticInterval(30)), None)
        self.assertEqual(Guitar.fret(4).add(Guitar, ChromaticInterval(5)), Guitar.fret(9))

    def test_lt(self):
        self.assertLess(open_fret, not_played_fret)
        self.assertLess(Guitar.fret(1), not_played_fret)
        self.assertLess(open_fret, Guitar.fret(1))

    def test_raise(self):
        #instrument.fret("a")
        with self.assertRaises(AssertionError):
            Guitar.fret("a")

    def test_height(self):
        self.assertEqual(open_fret.height(), 0)
        self.assertEqual(Guitar.fret(1).height(), HEIGHT_OF_FIRST_FRET)
        self.assertEqual(Guitar.fret(2).height(), HEIGHT_OF_FIRST_FRET * RATIO_FRET_HEIGHT)
        for i in range(1, 24):
            self.assertAlmostEqual(Guitar.fret(i+1).height()/Guitar.fret(i).height(), RATIO_FRET_HEIGHT)

    def test_y(self):
        self.assertEqual(open_fret.y_fret(), MARGIN)
        self.assertEqual(Guitar.fret(1).y_fret(), HEIGHT_OF_FIRST_FRET + MARGIN)
        self.assertEqual(Guitar.fret(1).y_fret(), Guitar.fret(1).height() + MARGIN)
        self.assertAlmostEqual(Guitar.fret(1).y_fret() + Guitar.fret(2).height(), Guitar.fret(2).y_fret())
        for i in range(24):
            self.assertAlmostEqual(Guitar.fret(i).y_fret() + Guitar.fret(i+1).height(), Guitar.fret(i+1).y_fret())