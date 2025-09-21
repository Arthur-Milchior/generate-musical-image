import unittest
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import *

open_fret = Fret.make( 0, True)
not_played_fret = Fret.make( None, True)

class TestFrettedInstrumentAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(not_played_fret, not_played_fret)
        self.assertEqual(not_played_fret.add(Guitar, ChromaticInterval.make(4)), not_played_fret)
        self.assertNotEqual(not_played_fret, open_fret)
        self.assertNotEqual(open_fret.add(Guitar, ChromaticInterval.make(4)), open_fret)
        self.assertEqual(open_fret, open_fret)
        self.assertEqual(Fret.make(4, True).add(Guitar, ChromaticInterval.make(-5)), None)
        self.assertEqual(Fret.make(4, True).add(Guitar, ChromaticInterval.make(30)), None)
        self.assertEqual(Fret.make(4, True).add(Guitar, ChromaticInterval.make(5)), Fret.make(9, True))

    def test_lt(self):
        self.assertLess(open_fret, not_played_fret)
        self.assertLess(Fret.make(1, True), not_played_fret)
        self.assertLess(open_fret, Fret.make(1, True))

    def test_raise(self):
        #Fret.make("a", True)
        with self.assertRaises(AssertionError):
            Fret.make("a", True)

    def test_height(self):
        self.assertEqual(open_fret.height(), 0)
        self.assertEqual(Fret.make(1, True).height(), HEIGHT_OF_FIRST_FRET)
        self.assertEqual(Fret.make(2, True).height(), HEIGHT_OF_FIRST_FRET * RATIO_FRET_HEIGHT)
        for i in range(1, 24):
            self.assertAlmostEqual(Fret.make(i+1, True).height()/Fret.make(i, True).height(), RATIO_FRET_HEIGHT)

    def test_y(self):
        self.assertEqual(open_fret.y_fret(), MARGIN)
        self.assertEqual(Fret.make(1, True).y_fret(), HEIGHT_OF_FIRST_FRET + MARGIN)
        self.assertEqual(Fret.make(1, True).y_fret(), Fret.make(1, True).height() + MARGIN)
        self.assertAlmostEqual(Fret.make(1, True).y_fret() + Fret.make(2, True).height(), Fret.make(2, True).y_fret())
        for i in range(24):
            self.assertAlmostEqual(Fret.make(i, True).y_fret() + Fret.make(i+1, True).height(), Fret.make(i+1, True).y_fret())
