import unittest

from fretted_instrument.chord.chord_utils import enumerate_frets
from fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from fretted_instrument.position.fret.frets import Frets
from fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, empty_set_of_position
from fretted_instrument.position.string.strings import Strings

no_strings = Strings.make(Guitar, [])
last_string_only = Strings.make(Guitar, [Guitar.string(6)])

contradiction = Frets.make(Guitar, _closed_fret_interval=None, allow_not_played=False, allow_open=False)
empty_fret = Frets.make(Guitar, _closed_fret_interval=None, allow_not_played=False, allow_open=True)

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
            frozenset(enumerate_frets(Guitar, Strings.make(Guitar, last_string_only), Frets.make(Guitar, _closed_fret_interval=(1, 1), allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfPositionOnFrettedInstrument.make(Guitar, {(6, 1)}),
            })
        )

    def test_two_fret_two_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Guitar, Strings.make(Guitar, [Guitar.string(5), Guitar.string(6)]), Frets.make(Guitar, _closed_fret_interval=(1, 2), allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfPositionOnFrettedInstrument.make(Guitar, {(5, 1), (6, 1)}),
                SetOfPositionOnFrettedInstrument.make(Guitar, {(5, 1), (6, 2)}),
                SetOfPositionOnFrettedInstrument.make(Guitar, {(5, 2), (6, 1)}),
                SetOfPositionOnFrettedInstrument.make(Guitar, {(5, 2), (6, 2)}),
            })
        )
    