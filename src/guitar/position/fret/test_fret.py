import unittest
from guitar.position.fret.fret import *

class TestGuitarAddString(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(NOT_PLAYED, NOT_PLAYED)
        self.assertEqual(NOT_PLAYED + ChromaticInterval(4), NOT_PLAYED)
        self.assertNotEqual(NOT_PLAYED, OPEN_FRET)
        self.assertNotEqual(OPEN_FRET + ChromaticInterval(4), OPEN_FRET)
        self.assertEqual(OPEN_FRET, OPEN_FRET)
        self.assertEqual(Fret(4) + ChromaticInterval(-5), None)
        self.assertEqual(Fret(4) + ChromaticInterval(30), None)
        self.assertEqual(Fret(4) + ChromaticInterval(5), Fret(9))

    def test_lt(self):
        self.assertLess(OPEN_FRET, NOT_PLAYED)
        self.assertLess(Fret(1), NOT_PLAYED)
        self.assertLess(OPEN_FRET, Fret(1))

    def test_raise(self):
        #Fret("a")
        with self.assertRaises(AssertionError):
            Fret("a")

    def test_height(self):
        self.assertEqual(OPEN_FRET.height(), 0)
        self.assertEqual(Fret(1).height(), HEIGHT_OF_FIRST_FRET)
        self.assertEqual(Fret(2).height(), HEIGHT_OF_FIRST_FRET * RATIO_FRET_HEIGHT)
        for i in range(1, 24):
            self.assertAlmostEqual(Fret(i+1).height()/Fret(i).height(), RATIO_FRET_HEIGHT)

    def test_y(self):
        self.assertEqual(OPEN_FRET.y_fret(), MARGIN)
        self.assertEqual(Fret(1).y_fret(), HEIGHT_OF_FIRST_FRET + MARGIN)
        self.assertEqual(Fret(1).y_fret(), Fret(1).height() + MARGIN)
        self.assertAlmostEqual(Fret(1).y_fret() + Fret(2).height(), Fret(2).y_fret())
        for i in range(24):
            self.assertAlmostEqual(Fret(i).y_fret() + Fret(i+1).height(), Fret(i+1).y_fret())