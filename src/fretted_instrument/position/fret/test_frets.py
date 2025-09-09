
import unittest

from fretted_instrument.position.fret.frets import Frets
from fretted_instrument.position.fret.fret import HIGHEST_FRET, NOT_PLAYED 
from fretted_instrument.position.fret.fret import OPEN_FRET, Fret
from fretted_instrument.position.string.string_deltas import *

ALL_PLAYED = Frets.make()
ALL = Frets.make(allow_not_played=True)
ALL_CLOSED = ALL_PLAYED.disallow_open()
FIRST_FOUR = Frets.make((1, 4))
AROUND_SEVEN = ALL_PLAYED.restrict_around(Fret(7))
AROUND_FIVE_SEVEN = AROUND_SEVEN.restrict_around(Fret(5))
NOT_PLAYED_FRETS = Frets.make(None, False, True)
CONTRADICTION = Frets.make(None, False, False)
ONLY_OPEN = Frets.make(None, allow_open=True, allow_not_played=False)
FOR_TRANSPOSABLE_CHORD = Frets.make(closed_fret_interval=(1, 5), allow_not_played=True, allow_open=False)

class TestGuitarFrets(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(ALL_PLAYED, Frets.make((1, HIGHEST_FRET.value), True))
        self.assertEqual(ALL_CLOSED, Frets.make((1, HIGHEST_FRET.value), allow_open=False))
        self.assertEqual(FIRST_FOUR, Frets.make((1, 4), True))
        self.assertEqual(AROUND_SEVEN, Frets.make((3, 11), True))
        self.assertEqual(AROUND_FIVE_SEVEN, Frets.make((3, 9), True))
        self.assertEqual(AROUND_FIVE_SEVEN, Frets.make().restrict_around(Fret(5)).restrict_around(Fret(7)))

    def test_is_empty(self):
        self.assertFalse(ALL_PLAYED.is_empty())
        self.assertFalse(ONLY_OPEN.is_empty())
        self.assertTrue(NOT_PLAYED_FRETS.is_empty())
        self.assertTrue(CONTRADICTION.is_empty())

    def test_is_contradiction(self):
        self.assertFalse(ALL_PLAYED.is_contradiction())
        self.assertFalse(ONLY_OPEN.is_contradiction())
        self.assertFalse(NOT_PLAYED_FRETS.is_contradiction())
        self.assertTrue(CONTRADICTION.is_contradiction())

    def test_frets(self):
        self.assertEqual(list(ALL_PLAYED), [Fret(fret) for fret in range(0, 25)])
        self.assertEqual(list(ALL_CLOSED), [Fret(fret) for fret in range(1, 25)])
        self.assertEqual(list(FIRST_FOUR), [Fret(fret) for fret in range(0, 5)])
        self.assertEqual(list(AROUND_SEVEN), [OPEN_FRET] + [Fret(fret) for fret in range(3, 12)])
        self.assertEqual(list(AROUND_FIVE_SEVEN), [OPEN_FRET] + [Fret(fret) for fret in range(3, 10)])
        self.assertEqual(list(CONTRADICTION), [])
        self.assertEqual(list(NOT_PLAYED_FRETS), [NOT_PLAYED])
        self.assertEqual(list(ONLY_OPEN), [OPEN_FRET])
        self.assertEqual(list(FOR_TRANSPOSABLE_CHORD), [NOT_PLAYED, Fret(1), Fret(2), Fret(3), Fret(4), Fret(5)])