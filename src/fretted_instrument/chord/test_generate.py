from typing import Set, Tuple
import unittest

from fretted_instrument.chord.chord_utils import enumerate_frets
from fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.fret.frets import Frets
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, empty_set_of_position
from fretted_instrument.position.string.strings import Strings

no_strings = Strings.make([])
last_string_only = Strings.make([Guitar.string(6)])

contradiction = Frets.make(closed_fret_interval=None, allow_not_played=False, allow_open=False)
empty_fret = Frets.make(closed_fret_interval=None, allow_not_played=False, allow_open=True)

def set_of_pos_make(arg: Set[Tuple[int, int]]):
    poss = set()
    for string, fret in arg:
        poss.add(PositionOnFrettedInstrument.make(string=Guitar.string(string), fret=Fret(fret)))
    return SetOfPositionOnFrettedInstrument.make(poss)

empty_set_of_fretted_instrument_position = empty_set_of_position(Guitar)
class TestGenerate(unittest.TestCase):
    def test_empty_set(self):
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, last_string_only, contradiction)),
                      frozenset()
                      )
        
    def test_set_no_notes(self):
        actual = frozenset(enumerate_frets(Guitar, no_strings, contradiction))
        expected = frozenset({empty_set_of_fretted_instrument_position})
        self.assertEqual(actual, expected,)
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, no_strings, empty_fret)),
            frozenset({empty_set_of_fretted_instrument_position})
        )

    def test_one_fret_one_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, Strings.make(last_string_only), Frets.make(closed_fret_interval=(1, 1), allow_not_played=False, allow_open=False))),
            frozenset({
                set_of_pos_make({(6, 1)}),
            })
        )

    def test_two_fret_two_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, Strings.make([Guitar.string(5), Guitar.string(6)]), Frets.make(closed_fret_interval=(1, 2), allow_not_played=False, allow_open=False))),
            frozenset({
                set_of_pos_make({(5, 1), (6, 1)}),
                set_of_pos_make({(5, 1), (6, 2)}),
                set_of_pos_make({(5, 2), (6, 1)}),
                set_of_pos_make({(5, 2), (6, 2)}),
            })
        )
    