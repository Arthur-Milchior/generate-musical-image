import unittest

from instruments.fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from utils.frozenlist import FrozenList
from instruments.fretted_instrument.position.string.string import StringFrozenList
from instruments.fretted_instrument.chord.test_constants import *

strings = list(Guitar.strings())

def position_make(string, fret):
    """Build a `PositionOnFrettedInstrument` on Guitar, accepting either a `String`/`Fret` or a plain
    int (string number / absolute fret value) for either argument."""
    if isinstance(string, int):
        string = Guitar.string(string)
    if isinstance(fret, int):
        fret = Fret.make(fret, True)
    return PositionOnFrettedInstrument.make(string=string, fret=fret)

class TestHandForFrettedInstrumentChord(unittest.TestCase):
    def assertHandEqual(self, expected: HandForChordForFrettedInstrument, actual: HandForChordForFrettedInstrument):
        """Assert that two `HandForChordForFrettedInstrument` instances assign the same position to each
        finger, the same barre status, and the same open strings."""
        self.assertEqual(expected.one, actual.one)
        self.assertEqual(expected.two, actual.two)
        self.assertEqual(expected.barred, actual.barred)
        self.assertEqual(expected.three, actual.three)
        self.assertEqual(expected.four, actual.four)
        self.assertEqual(expected.zero_fret, actual.zero_fret)
        self.assertEqual(expected.opens, actual.opens)

    def test_make(self):
        """`compute_hand` assigns fingers/open strings matching hand-picked expectations for three chord
        shapes (C4M, C4M_, F4M — the last one barred)."""
        expected = HandForChordForFrettedInstrument(instrument = Guitar,
                one = position_make(5, 1),
                two = position_make(3, 2),
                four = position_make(2, 3),
                opens = StringFrozenList([strings[3], strings[5]]),
            )
        actual = HandForChordForFrettedInstrument.compute_hand(Guitar, C4M)
        self.assertHandEqual(expected
            ,actual
        )
        self.assertHandEqual(
            HandForChordForFrettedInstrument(instrument = Guitar,
                one = position_make(5, 1),
                two = position_make(3, 2),
                four = position_make(2, 3),
                opens = StringFrozenList([strings[3]]),
            ),
            HandForChordForFrettedInstrument.compute_hand(Guitar, C4M_),
        )
        self.assertHandEqual(
            HandForChordForFrettedInstrument(instrument = Guitar,
                one = position_make(1, 1),
                two = position_make(4, 2),
                three = position_make(2, 3),
                four = position_make(3, 3),
                barred = Barred.FULLY,
            ),
            HandForChordForFrettedInstrument.compute_hand(Guitar, F4M),
        )


    def test_regression_502220(self):
        """Regression: the 5-0-2-2-2-0 shape's computed hand must match the expected finger assignment and
        stay rated unplayable."""
        chord = ChordOnFrettedInstrument.make(Guitar, [5, 0, 2, 2, 2, 0], absolute=True)
        hand = HandForChordForFrettedInstrument.compute_hand(Guitar, chord)
        expected= HandForChordForFrettedInstrument(
            instrument=Guitar,
              zero_fret=None,
                one=position_make(3, 2), 
                barred=Barred.NO, 
                two=position_make(4, 2),
                three=position_make(5, 2),
                four=position_make(1, 5),
                opens=StringFrozenList([Guitar.string(2), Guitar.string(6)]))
        self.assertEqual(hand, expected)
        playable = expected.playable()
        self.assertEqual(playable, Playable.NO)