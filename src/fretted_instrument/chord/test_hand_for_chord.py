import unittest

from fretted_instrument.chord.hand_for_chord import HandForChordForFrettedInstrument
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from utils.frozenlist import FrozenList
from fretted_instrument.position.string.string import StringFrozenList
from fretted_instrument.chord.test_constants import *

strings = list(Guitar.strings())

def position_make(*args, **kwargs):
    return PositionOnFrettedInstrument.make(Guitar, *args, **kwargs)

class TestHandForFrettedInstrumentChord(unittest.TestCase):
    def assertHandEqual(self, expected: HandForChordForFrettedInstrument, actual: HandForChordForFrettedInstrument):
        self.assertEqual(expected.one, actual.one)
        self.assertEqual(expected.two, actual.two)
        self.assertEqual(expected.barred, actual.barred)
        self.assertEqual(expected.three, actual.three)
        self.assertEqual(expected.four, actual.four)
        self.assertEqual(expected.zero_fret, actual.zero_fret)
        self.assertEqual(expected.opens, actual.opens)

    def test_make(self):
        expected = HandForChordForFrettedInstrument(instrument = Guitar,
                one = position_make(5, 1),
                two = position_make(3, 2),
                four = position_make(2, 3),
                opens = StringFrozenList([strings[3], strings[5]]),
            )
        actual = HandForChordForFrettedInstrument.make(C4M)
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
            HandForChordForFrettedInstrument.make(C4M_),
        )
        self.assertHandEqual(
            HandForChordForFrettedInstrument(instrument = Guitar,
                one = position_make(1, 1),
                two = position_make(4, 2),
                three = position_make(2, 3),
                four = position_make(3, 3),
                barred = Barred.FULLY,
            ),
            HandForChordForFrettedInstrument.make(F4M),
        )