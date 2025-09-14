
import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.frets import Frets
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.string.string_deltas import *

def frets_make(*args, **kwargs):
    return Frets.make(*args, **kwargs)

instrument = Guitar

ALL_PLAYED = frets_make((1, Guitar.last_fret()), True)
ALL = frets_make(allow_not_played=True)
ALL_CLOSED = ALL_PLAYED.disallow_open()
FIRST_FOUR = frets_make((1, 4), True)

# AROUND_SEVEN = ALL_PLAYED.restrict_around(instrument.fret(7))
# AROUND_FIVE_SEVEN = AROUND_SEVEN.restrict_around(instrument.fret(5))
NOT_PLAYED_FRETS = frets_make(None, False, True)
CONTRADICTION = frets_make(None, False, False)
ONLY_OPEN = frets_make(None, allow_open=True, allow_not_played=False)
FOR_TRANSPOSABLE_CHORD = frets_make(closed_fret_interval=(1, 5), allow_not_played=True, allow_open=False)

highest_fret = Guitar.last_fret()
open_fret = Guitar.fret( value=0)
not_played_fret = Guitar.fret( value=None)

class TestFrettedInstrumentFrets(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(ALL_PLAYED, frets_make((1, Guitar.last_fret()), True))
        self.assertEqual(ALL_CLOSED, frets_make((1, Guitar.last_fret()), allow_open=False))
        self.assertEqual(FIRST_FOUR, frets_make((1, 4), True))
        # self.assertEqual(AROUND_SEVEN, frets_make((3, 11), True))
        # self.assertEqual(AROUND_FIVE_SEVEN, frets_make((3, 9), True))
        # self.assertEqual(AROUND_FIVE_SEVEN, frets_make().restrict_around(instrument.fret(5)).restrict_around(instrument.fret(7)))

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
        self.assertEqual(list(ALL_PLAYED), [instrument.fret(fret) for fret in range(0, 25)])
        self.assertEqual(list(ALL_CLOSED), [instrument.fret(fret) for fret in range(1, 25)])
        self.assertEqual(list(FIRST_FOUR), [instrument.fret(fret) for fret in range(0, 5)])

        # self.assertEqual(list(AROUND_SEVEN), [open_fret] + [instrument.fret(fret) for fret in range(3, 12)])
        # self.assertEqual(list(AROUND_FIVE_SEVEN), [open_fret] + [instrument.fret(fret) for fret in range(3, 10)])
        self.assertEqual(list(CONTRADICTION), [])
        self.assertEqual(list(NOT_PLAYED_FRETS), [not_played_fret])
        self.assertEqual(list(ONLY_OPEN), [open_fret])
        self.assertEqual(list(FOR_TRANSPOSABLE_CHORD), [not_played_fret, instrument.fret(1), instrument.fret(2), instrument.fret(3), instrument.fret(4), instrument.fret(5)])