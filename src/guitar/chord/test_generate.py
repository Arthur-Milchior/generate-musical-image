import unittest

from guitar.position.fret import Fret
from guitar.position.string import strings

from guitar.chord.chord_utils import *

no_strings = Strings([])
last_string = Strings([strings[5]])

contradiction = Frets(min_fret=5, max_fret=4, allow_not_played=False, allow_open=False)
empty_fret = Frets(min_fret=5, max_fret=4, allow_not_played=False, allow_open=True)

class TestGenerate(unittest.TestCase):
    def test_empty_set(self):
        self.assertEqual(
            frozenset(enumerate_frets(last_string, contradiction)),
                      frozenset()
                      )
        
    def test_set_no_notes(self):
        actual = frozenset(enumerate_frets(no_strings, contradiction))
        expected = frozenset({SetOfGuitarPositions()})
        self.assertEqual(actual, expected,)
        self.assertEqual(
            frozenset(enumerate_frets(no_strings, empty_fret)),
            frozenset({SetOfGuitarPositions()})
        )

    def test_one_fret_one_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Strings([strings[5]]), Frets(min_fret=1, max_fret=1, allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfGuitarPositions.make({(5, 1)}),
            })
        )

    def test_two_fret_two_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Strings([strings[4], strings[5]]), Frets(min_fret=1, max_fret=2, allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfGuitarPositions.make({(4, 1), (5, 1)}),
                SetOfGuitarPositions.make({(4, 1), (5, 2)}),
                SetOfGuitarPositions.make({(4, 2), (5, 1)}),
                SetOfGuitarPositions.make({(4, 2), (5, 2)}),
            })
        )
    