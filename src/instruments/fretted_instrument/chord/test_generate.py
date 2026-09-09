from typing import Set, Tuple
import unittest

from instruments.fretted_instrument.chord.chord_utils import enumerate_frets
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fret.frets import Frets
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, empty_set_of_position
from instruments.fretted_instrument.position.string.strings import Strings

no_strings = Strings.make([])
last_string_only = Strings.make([Guitar.string(6)])

contradiction = Frets.make(closed_fret_interval=None, allow_not_played=False, allow_open=False, absolute=True)
empty_fret = Frets.make(closed_fret_interval=None, allow_not_played=False, allow_open=True, absolute=True)

def set_of_pos_make(arg: Set[Tuple[int, int]]):
    """Build an absolute `SetOfPositionOnFrettedInstrument` on Guitar from a set of (string number, fret
    value) pairs, for use as a test fixture."""
    poss = set()
    for string, fret in arg:
        poss.add(PositionOnFrettedInstrument.make(string=Guitar.string(string), fret=Fret.make(fret, True)))
    return SetOfPositionOnFrettedInstrument.make(poss, absolute=True)

empty_set_of_fretted_instrument_position = empty_set_of_position(Guitar, True)
class TestGenerate(unittest.TestCase):
    def test_empty_set(self):
        """A contradictory fret range on a single string enumerates to no positions at all."""
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, strings=last_string_only, frets=contradiction)),
                      frozenset()
                      )
        
    def test_set_no_notes(self):
        """Enumerating over no strings always yields exactly the empty set of positions, regardless of the
        fret constraint (even a contradictory one)."""
        actual = frozenset(enumerate_frets(Guitar, strings=no_strings, frets=contradiction))
        expected = frozenset({empty_set_of_fretted_instrument_position})
        self.assertEqual(actual, expected,)
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, strings=no_strings, frets=empty_fret)),
            frozenset({empty_set_of_fretted_instrument_position})
        )

    def test_one_fret_one_strings(self):
        """One string with a single allowed fret enumerates to exactly one position set."""
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, strings=Strings.make(last_string_only), frets=Frets.make(closed_fret_interval=(1, 1), allow_not_played=False, allow_open=False, absolute=True))),
            frozenset({
                set_of_pos_make({(6, 1)}),
            })
        )

    def test_two_fret_two_strings(self):
        """Two strings each allowing 2 frets enumerate to all 4 combinations of fret choices."""
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, strings=Strings.make([Guitar.string(5), Guitar.string(6)]), frets=Frets.make(closed_fret_interval=(1, 2), allow_not_played=False, allow_open=False, absolute=True))),
            frozenset({
                set_of_pos_make({(5, 1), (6, 1)}),
                set_of_pos_make({(5, 1), (6, 2)}),
                set_of_pos_make({(5, 2), (6, 1)}),
                set_of_pos_make({(5, 2), (6, 2)}),
            })
        )
    