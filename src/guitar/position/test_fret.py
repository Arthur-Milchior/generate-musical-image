import unittest
from .fret import *

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