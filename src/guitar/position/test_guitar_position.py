
import unittest
from .guitar_position import *

class TestPosition(unittest.TestCase):
    def test_fail_init(self):
        with self.assertRaises(Exception):
            GuitarPosition(string=0, fret=4)
        with self.assertRaises(Exception):
            GuitarPosition(string=1, fret=-1)
        with self.assertRaises(Exception):
            GuitarPosition(string=7, fret=4)

    def test_get_chromatic(self):
        self.assertEqual(GuitarPosition(string=1, fret=None).get_chromatic(), None)
        self.assertEqual(GuitarPosition(string=1, fret=0).get_chromatic(), ChromaticNote(value=-8))
        self.assertEqual(GuitarPosition(string=3, fret=3).get_chromatic(), ChromaticNote(value=5))

    def test_csv(self):
        self.assertEqual(GuitarPosition(string=1, fret=None).svg(), """
    <text x="15" y="16" font-size="30">x</text>""")
        self.assertEqual(GuitarPosition(string=1, fret=0).svg(), """
    <circle cx="15" cy="25" r="11" fill="white" stroke="black" stroke-width="3"/>""")
        self.assertEqual(GuitarPosition(string=1, fret=3).svg(), """
    <circle cx="15" cy="150" r="11" fill="black" stroke="black" stroke-width="3"/>""")

    def test_repr(self):
        self.assertEqual(repr(GuitarPosition(string=1, fret=None)), "GuitarPosition(string=1, fret=None)")
        self.assertEqual(repr(GuitarPosition(string=1, fret=0)), "GuitarPosition(string=1, fret=0)")

    def test_eq(self):
        self.assertEqual(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=None))
        self.assertEqual(GuitarPosition(string=1, fret=8), GuitarPosition(string=1, fret=8))
        self.assertNotEqual(GuitarPosition(string=2, fret=8), GuitarPosition(string=1, fret=8))
        self.assertNotEqual(GuitarPosition(string=1, fret=7), GuitarPosition(string=1, fret=8))
        self.assertNotEqual(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=8))

    def test_lt(self):
        self.assertLess( GuitarPosition(string=1, fret=1), GuitarPosition(string=1, fret=None))
        self.assertLess(GuitarPosition(string=1, fret=1), GuitarPosition(string=1, fret=2))
        self.assertLess(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=1))
        self.assertLess(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=None))

    def test_le(self):
        self.assertEqual(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=None))
        self.assertEqual(GuitarPosition(string=1, fret=8), GuitarPosition(string=1, fret=8))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=1, fret=None))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=1, fret=2))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=1))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=None))
