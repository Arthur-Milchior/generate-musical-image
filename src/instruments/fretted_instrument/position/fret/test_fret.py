import unittest
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import *

open_fret = Fret( 0, True)
not_played_fret = Fret( None, True)

class TestFrettedInstrumentAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(not_played_fret, not_played_fret)
        self.assertEqual(not_played_fret.add(Guitar, ChromaticInterval(4)), not_played_fret)
        self.assertNotEqual(not_played_fret, open_fret)
        self.assertNotEqual(open_fret.add(Guitar, ChromaticInterval(4)), open_fret)
        self.assertEqual(open_fret, open_fret)
        self.assertEqual(Fret(4, True).add(Guitar, ChromaticInterval(-5)), None)
        self.assertEqual(Fret(4, True).add(Guitar, ChromaticInterval(30)), None)
        self.assertEqual(Fret(4, True).add(Guitar, ChromaticInterval(5)), Fret(9, True))

    def test_lt(self):
        self.assertLess(open_fret, not_played_fret)
        self.assertLess(Fret(1, True), not_played_fret)
        self.assertLess(open_fret, Fret(1, True))

    def test_raise(self):
        #Fret("a", True)
        with self.assertRaises(AssertionError):
            Fret("a", True)

    def test_height(self):
        self.assertEqual(open_fret.height(), 0)
        self.assertEqual(Fret(1, True).height(), HEIGHT_OF_FIRST_FRET)
        self.assertEqual(Fret(2, True).height(), HEIGHT_OF_FIRST_FRET * RATIO_FRET_HEIGHT)
        for i in range(1, 24):
            self.assertAlmostEqual(Fret(i+1, True).height()/Fret(i, True).height(), RATIO_FRET_HEIGHT)

    def test_y(self):
        self.assertEqual(open_fret.y_fret(), MARGIN)
        self.assertEqual(Fret(1, True).y_fret(), HEIGHT_OF_FIRST_FRET + MARGIN)
        self.assertEqual(Fret(1, True).y_fret(), Fret(1, True).height() + MARGIN)
        self.assertAlmostEqual(Fret(1, True).y_fret() + Fret(2, True).height(), Fret(2, True).y_fret())
        for i in range(24):
            self.assertAlmostEqual(Fret(i, True).y_fret() + Fret(i+1, True).height(), Fret(i+1, True).y_fret())
