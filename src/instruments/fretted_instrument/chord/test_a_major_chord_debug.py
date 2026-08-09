"""Tests for A major chord x02225 using the shared A4M constant."""

import unittest
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import Barred, ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.chord.test_constants import A4M


class TestAMajorChordX02225(unittest.TestCase):
    """Tests for A major chord x02225 [5, 2, 2, 2, 0, x]."""

    def setUp(self):
        self.chord = A4M

    def test_get_frets_returns_expected_values(self):
        frets = self.chord.get_frets(Guitar)
        self.assertEqual([fret.value for fret in frets], [None, 0, 2, 2, 2, 5])

    def test_open_chord_metadata(self):
        self.assertTrue(self.chord.is_open())
        self.assertFalse(self.chord.is_transposable())
        self.assertEqual(self.chord.open_strings(), [Guitar.string(2)])

    def test_min_closed_strings(self):
        self.assertEqual(
            self.chord.strings_at_min_fret(allow_open=False),
            [Guitar.string(3), Guitar.string(4), Guitar.string(5)],
        )

    def test_has_not_played_in_middle_returns_false(self):
        self.assertFalse(self.chord.has_not_played_in_middle())

    def test_chord_pattern_is_redundant_returns_false(self):
        self.assertFalse(self.chord.chord_pattern_is_redundant())

    def test_is_barred_returns_partially(self):
        self.assertEqual(self.chord.is_barred(), Barred.PARTIALLY)

    def test_am_partial_bar_with_no_open_strings_between_min_closed(self):
        min_closed = self.chord.strings_at_min_fret(allow_open=False)
        open_strings = self.chord.open_strings()
        min_closed_string = min(min_closed)
        max_closed_string = max(min_closed)
        open_in_between = [s for s in open_strings if min_closed_string < s < max_closed_string]
        self.assertEqual(open_in_between, [])

    def test_hand_configuration(self):
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, self.chord)
        self.assertIsNotNone(hand)
        self.assertEqual(hand.barred, Barred.PARTIALLY)
        self.assertEqual(hand.one.fret.value, 2)
        self.assertEqual(hand.four.fret.value, 5)
        self.assertEqual(list(hand.opens), [Guitar.string(2)])

    def test_hand_playable_returns_easy(self):
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, self.chord)
        self.assertEqual(hand.playable(), Playable.EASY)

    def test_chord_playable_returns_easy(self):
        self.assertEqual(self.chord.playable(Guitar), Playable.EASY)


if __name__ == '__main__':
    unittest.main(verbosity=2)
