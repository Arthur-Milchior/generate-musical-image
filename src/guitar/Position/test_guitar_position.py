
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
        self.assertEquals(GuitarPosition(string=1, fret=None).get_chromatic(), None)
        self.assertEquals(GuitarPosition(string=1, fret=0).get_chromatic(), ChromaticNote(value=-8))
        self.assertEquals(GuitarPosition(string=3, fret=3).get_chromatic(), ChromaticNote(value=5))

    def test_csv(self):
        self.assertEquals(GuitarPosition(string=1, fret=None).svg(), """
    <text x="" y="" font-size="30">x</text>""")
        self.assertEquals(GuitarPosition(string=1, fret=0).svg(), """
    <circle cx="" cy="" r="11" fill="white" stroke="black" stroke-width="3"/>""")
        self.assertEquals(GuitarPosition(string=1, fret=3).svg(), """
    <circle cx="" cy="" r="11" fill="black" stroke="black" stroke-width="3"/>""")

    def test_repr(self):
        self.assertEquals(repr(GuitarPosition(string=1, fret=None)), "Position(string=1, fret=None)")
        self.assertEquals(repr(GuitarPosition(string=1, fret=0)), "Position(string=1, fret=0")

    def test_eq(self):
        self.assertEquals(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=None))
        self.assertEquals(GuitarPosition(string=1, fret=8), GuitarPosition(string=1, fret=8))
        self.assertNotEquals(GuitarPosition(string=2, fret=8), GuitarPosition(string=1, fret=8))
        self.assertNotEquals(GuitarPosition(string=1, fret=7), GuitarPosition(string=1, fret=8))
        self.assertNotEquals(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=8))

    def test_lt(self):
        self.assertLess(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=1))
        self.assertLess(GuitarPosition(string=1, fret=1), GuitarPosition(string=1, fret=2))
        self.assertLess(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=1))
        self.assertLess(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=None))

    def test_le(self):
        self.assertEquals(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=None))
        self.assertEquals(GuitarPosition(string=1, fret=8), GuitarPosition(string=1, fret=8))
        self.assertLessEqual(GuitarPosition(string=1, fret=None), GuitarPosition(string=1, fret=1))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=1, fret=2))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=1))
        self.assertLessEqual(GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=None))
