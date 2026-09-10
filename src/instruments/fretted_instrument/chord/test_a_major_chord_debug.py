"""Tests for A major chord x02225 using the shared A4M constant."""

import unittest
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import Barred, ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.chord.playable import Playable
from instruments.fretted_instrument.chord.test_constants import A4M_high_G, A4Mt


class TestAMajorChordHighG(unittest.TestCase):
    """Tests for A major chord x02225 [5, 2, 2, 2, 0, x]."""

    chord: ChordOnFrettedInstrument
    """The chord fixture under test, set by `setUp`."""

    def setUp(self) -> None:
        """Use the high-G-voicing A major chord as the fixture under test."""
        self.chord = A4M_high_G

    def test_get_frets_returns_expected_values(self) -> None:
        """`get_frets` reports the exact fret (or not-played) per string for x02225."""
        frets = self.chord.get_frets(Guitar)
        self.assertEqual([fret.value for fret in frets], [None, 0, 2, 2, 2, 5])

    def test_open_chord_metadata(self) -> None:
        """The chord is open (contains an open string) and not transposable, with string 2 open."""
        self.assertTrue(self.chord.is_open())
        self.assertFalse(self.chord.is_transposable())
        self.assertEqual(self.chord.open_strings(), [Guitar.string(2)])

    def test_min_closed_strings(self) -> None:
        """The lowest closed fret (fret 2) is shared by strings 3, 4 and 5."""
        self.assertEqual(
            self.chord.strings_at_min_fret(allow_open=False),
            [Guitar.string(3), Guitar.string(4), Guitar.string(5)],
        )

    def test_has_not_played_in_middle_returns_false(self) -> None:
        """No not-played string is sandwiched between played strings."""
        self.assertFalse(self.chord.has_not_played_in_middle())

    def test_chord_pattern_is_redundant_returns_false(self) -> None:
        """The fingering isn't redundant (its minimum fret isn't above 1, once open strings are allowed)."""
        self.assertFalse(self.chord.chord_pattern_is_redundant())

    def test_is_barred_returns_partially(self) -> None:
        """Strings 3-5 share the lowest closed fret but an open string (2) sits inside that range, so the bar
        need only be partial."""
        self.assertEqual(self.chord.is_barred(), Barred.PARTIALLY)

    def test_am_partial_bar_with_no_open_strings_between_min_closed(self) -> None:
        """No open string falls strictly between the lowest and highest string sharing the minimum closed fret."""
        min_closed = self.chord.strings_at_min_fret(allow_open=False)
        open_strings = self.chord.open_strings()
        min_closed_string = min(min_closed)
        max_closed_string = max(min_closed)
        open_in_between = [s for s in open_strings if min_closed_string < s < max_closed_string]
        self.assertEqual(open_in_between, [])

    def test_hand_configuration(self) -> None:
        """`compute_hand` assigns finger 1 to fret 2, finger 4 to fret 5, and leaves string 2 open."""
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, self.chord)
        self.assertIsNotNone(hand)
        self.assertEqual(hand.barred, Barred.PARTIALLY)
        self.assertEqual(hand.one.fret.value, 2)
        self.assertEqual(hand.four.fret.value, 5)
        self.assertEqual(list(hand.opens), [Guitar.string(2)])

    def test_hand_playable_returns_easy(self) -> None:
        """The computed hand configuration is playable without unusual finger stretch."""
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, self.chord)
        self.assertEqual(hand.playable(), Playable.EASY)

    def test_chord_playable_returns_easy(self) -> None:
        """`ChordOnFrettedInstrument.playable` reports `EASY` for this fingering."""
        self.assertEqual(self.chord.playable(Guitar), Playable.EASY)
class TestAMajorChordTransposable(unittest.TestCase):
    """Tests for A major chord transposable"""

    chord: ChordOnFrettedInstrument
    """The chord fixture under test, set by `setUp`."""

    def setUp(self) -> None:
        """Use the fully-barred, transposable A major chord as the fixture under test."""
        self.chord = A4Mt

    def test_get_frets_returns_expected_values(self) -> None:
        """`get_frets` reports the exact fret (or not-played) per string for 542220."""
        frets = self.chord.get_frets(Guitar)
        self.assertEqual([fret.value for fret in frets], [5, 4, 2, 2, 2, None])

    def test_open_chord_metadata(self) -> None:
        """The chord is transposable (no open string) and reports no open strings."""
        self.assertFalse(self.chord.is_open())
        self.assertTrue(self.chord.is_transposable())
        self.assertEqual(self.chord.open_strings(), [])

    def test_min_closed_strings(self) -> None:
        """The lowest closed fret (fret 2) is shared by strings 3, 4 and 5."""
        self.assertEqual(
            self.chord.strings_at_min_fret(allow_open=False),
            [Guitar.string(3), Guitar.string(4), Guitar.string(5)],
        )

    def test_has_not_played_in_middle_returns_false(self) -> None:
        """No not-played string is sandwiched between played strings."""
        self.assertFalse(self.chord.has_not_played_in_middle())

    def test_chord_pattern_is_redundant_returns_false(self) -> None:
        """Being fully transposable (no open strings), the fingering is redundant: it can be played identically
        one fret lower/higher elsewhere on the neck."""
        self.assertTrue(self.chord.chord_pattern_is_redundant())

    def test_is_barred(self) -> None:
        """With no open strings escaping the lowest closed fret, the chord requires a full bar."""
        self.assertEqual(self.chord.is_barred(), Barred.FULLY)

    def test_hand_configuration(self) -> None:
        """`compute_hand` bars finger 1 at fret 2, and assigns fingers 3 and 4 to frets 4 and 5, with no open strings."""
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, self.chord)
        self.assertIsNotNone(hand)
        self.assertEqual(hand.barred, Barred.FULLY)
        self.assertEqual(hand.one.fret.value, 2)
        self.assertEqual(hand.three.fret.value, 4)
        self.assertEqual(hand.four.fret.value, 5)
        self.assertEqual(list(hand.opens), [])

    def test_hand_playable_returns_easy(self) -> None:
        """The computed hand configuration is playable without unusual finger stretch."""
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, self.chord)
        self.assertEqual(hand.playable(), Playable.EASY)

    def test_chord_playable_returns_easy(self) -> None:
        """`ChordOnFrettedInstrument.playable` reports `EASY` for this fingering."""
        self.assertEqual(self.chord.playable(Guitar), Playable.EASY)

    def test_order(self) -> None:
        """The open, high-G voicing sorts as easier to play than the fully-barred transposable voicing."""
        self.assertLess(A4M_high_G.best_chord_key(), self.chord.best_chord_key())


if __name__ == '__main__':
    unittest.main(verbosity=2)
