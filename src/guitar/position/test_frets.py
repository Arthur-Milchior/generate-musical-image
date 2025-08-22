
import unittest

from guitar.position.frets import Frets
from guitar.position.fret import HIGHEST_FRET 
from guitar.position.fret import OPEN_FRET, Fret
from .string_deltas import *

ALL = Frets()
ALL_CLOSED = ALL.disallow_open()
FIRST_FOUR = Frets(max_fret=(4))
AROUND_SEVEN = ALL.restrict_around(Fret(7))
AROUND_FIVE_SEVEN = AROUND_SEVEN.restrict_around(Fret(5))
EMPTY = Frets(5, 4, False)
ONLY_OPEN = Frets(5, 4)

class TestGuitarFrets(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(ALL, Frets(1, HIGHEST_FRET.value, True))
        self.assertEqual(ALL_CLOSED, Frets(1, HIGHEST_FRET.value, allow_open=False))
        self.assertEqual(FIRST_FOUR, Frets(1, 4, True))
        self.assertEqual(AROUND_SEVEN, Frets(3, 11, True))
        self.assertEqual(AROUND_FIVE_SEVEN, Frets(3, 9, True))
        self.assertEqual(AROUND_FIVE_SEVEN, Frets().restrict_around(Fret(5)).restrict_around(Fret(7)))

    def test_is_empty(self):
        self.assertFalse(ALL.is_empty())
        self.assertFalse(ONLY_OPEN.is_empty())
        self.assertTrue(EMPTY.is_empty())

    def test_frets(self):
        self.assertEqual(list(ALL), [Fret(fret) for fret in range(0, 25)])
        self.assertEqual(list(ALL_CLOSED), [Fret(fret) for fret in range(1, 25)])
        self.assertEqual(list(FIRST_FOUR), [Fret(fret) for fret in range(0, 5)])
        self.assertEqual(list(AROUND_SEVEN), [OPEN_FRET] + [Fret(fret) for fret in range(3, 12)])
        self.assertEqual(list(AROUND_FIVE_SEVEN), [OPEN_FRET] + [Fret(fret) for fret in range(3, 10)])
        self.assertEqual(list(EMPTY), [])
        self.assertEqual(list(ONLY_OPEN), [OPEN_FRET])