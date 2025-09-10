import unittest

from fretted_instrument.chord.chord_utils import enumerate_frets
from fretted_instrument.fretted_instrument.fretted_instruments import Gui_tar
from fretted_instrument.position.fret.frets import Frets
from fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, empty_set_of_position
from fretted_instrument.position.string.strings import Strings

no_strings = Strings.make(Gui_tar, [])
last_string_only = Strings.make(Gui_tar, [Gui_tar.string(6)])

contradiction = Frets.make(Gui_tar, _closed_fret_interval=None, allow_not_played=False, allow_open=False)
empty_fret = Frets.make(Gui_tar, _closed_fret_interval=None, allow_not_played=False, allow_open=True)

empty_set_of_fretted_instrument_position = empty_set_of_position(Gui_tar)
class TestGenerate(unittest.TestCase):
    def test_empty_set(self):
        self.assertEqual(
            frozenset(enumerate_frets(Gui_tar, last_string_only, contradiction)),
                      frozenset()
                      )
        
    def test_set_no_notes(self):
        actual = frozenset(enumerate_frets(Gui_tar, no_strings, contradiction))
        expected = frozenset({empty_set_of_fretted_instrument_position})
        self.assertEqual(actual, expected,)
        self.assertEqual(
            frozenset(enumerate_frets(Gui_tar, no_strings, empty_fret)),
            frozenset({empty_set_of_fretted_instrument_position})
        )

    def test_one_fret_one_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Gui_tar, Strings.make(Gui_tar, last_string_only), Frets.make(Gui_tar, _closed_fret_interval=(1, 1), allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfPositionOnFrettedInstrument.make(Gui_tar, {(6, 1)}),
            })
        )

    def test_two_fret_two_strings(self):
        self.assertEqual(
            frozenset(enumerate_frets(Gui_tar, Strings.make(Gui_tar, [Gui_tar.string(5), Gui_tar.string(6)]), Frets.make(Gui_tar, _closed_fret_interval=(1, 2), allow_not_played=False, allow_open=False))),
            frozenset({
                SetOfPositionOnFrettedInstrument.make(Gui_tar, {(5, 1), (6, 1)}),
                SetOfPositionOnFrettedInstrument.make(Gui_tar, {(5, 1), (6, 2)}),
                SetOfPositionOnFrettedInstrument.make(Gui_tar, {(5, 2), (6, 1)}),
                SetOfPositionOnFrettedInstrument.make(Gui_tar, {(5, 2), (6, 2)}),
            })
        )
    