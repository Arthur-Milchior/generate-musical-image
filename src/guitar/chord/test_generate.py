import unittest

from guitar.position.string.string import strings
from guitar.chord.chord_utils import *

no_strings = Strings([])
last_string = Strings([strings[5]])

contradiction = Frets.make(closed_fret_interval=None, allow_not_played=False, allow_open=False)
empty_fret = Frets.make(closed_fret_interval=None, allow_not_played=False, allow_open=True)

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
            frozenset(enumerate_frets(Strings([strings[5]]), Frets.make(closed_fret_interval=(1, 1), allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfGuitarPositions.make({(6, 1)}),
            })
        )

    def test_two_fret_two_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Strings([strings[4], strings[5]]), Frets.make(closed_fret_interval=(1, 2), allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfGuitarPositions.make({(5, 1), (6, 1)}),
                SetOfGuitarPositions.make({(5, 1), (6, 2)}),
                SetOfGuitarPositions.make({(5, 2), (6, 1)}),
                SetOfGuitarPositions.make({(5, 2), (6, 2)}),
            })
        )
    