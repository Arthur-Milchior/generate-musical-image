import unittest

from guitar.chord.hand_for_chord import HandForGuitarChord
from guitar.position.guitar_position import GuitarPosition
from utils.frozenlist import FrozenList
from guitar.position.string.string import StringFrozenList, strings
from guitar.chord.test_constants import *

class TestHandForGuitarChord(unittest.TestCase):
    def assertHandEqual(self, expected: HandForGuitarChord, actual: HandForGuitarChord):
        self.assertEqual(expected.one, actual.one)
        self.assertEqual(expected.two, actual.two)
        self.assertEqual(expected.barred, actual.barred)
        self.assertEqual(expected.three, actual.three)
        self.assertEqual(expected.four, actual.four)
        self.assertEqual(expected.zero_fret, actual.zero_fret)
        self.assertEqual(expected.opens, actual.opens)

    def test_make(self):
        self.assertHandEqual(
            HandForGuitarChord(
                one = GuitarPosition.make(5, 1),
                two = GuitarPosition.make(3, 2),
                four = GuitarPosition.make(2, 3),
                opens = StringFrozenList([strings[3], strings[5]]),
            ),
            HandForGuitarChord.make(C4M),
        )
        self.assertHandEqual(
            HandForGuitarChord(
                one = GuitarPosition.make(5, 1),
                two = GuitarPosition.make(3, 2),
                four = GuitarPosition.make(2, 3),
                opens = StringFrozenList([strings[3]]),
            ),
            HandForGuitarChord.make(C4M_),
        )
        self.assertHandEqual(
            HandForGuitarChord(
                one = GuitarPosition.make(1, 1),
                two = GuitarPosition.make(4, 2),
                three = GuitarPosition.make(2, 3),
                four = GuitarPosition.make(3, 3),
                barred = Barred.FULLY,
            ),
            HandForGuitarChord.make(F4M),
        )