import unittest

from fretted_instrument.fretted_instrument.fretted_instruments import Gui_tar
from utils.frozenlist import FrozenList
from .fretted_instrument_position_with_fingers import *

def position_make(*args, **kwargs):
    return PositionOnFrettedInstrumentWithFingers.make(Gui_tar, *args, **kwargs)

class TestFrettedInstrumentPositionWithFingerss(unittest.TestCase):
    def test_positions_minus_tone_finger_1(self):
        self.assertEqual(([
            (frozenset({1}), position_make(string=2, fret=9, fingers=4)),
            ]),
            position_make(string=3, fret=6, fingers=1)
            .positions_for_interval(ChromaticInterval(-2))
            )

    def test_positions_minus_half_tone_finger_1(self):
        self.assertEqual([],
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(-1))
        )

    def test_positions_minus_half_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=5, fingers={1, 2})),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(-1))
        )

    def test_positions_minus_half_tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), position_make(string=3, fret=5, fingers={1, 2, 3})),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(-1))
        )

        
    def test_positions_half_tone_finger_1(self):
        self.assertEqual(([
        (frozenset({1}), position_make(string=3, fret=7, fingers={2, 3, 4})),
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(1))
        )

    def test_positions_half_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=7, fingers=4)),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(1))
        )

    def test_positions_half_tone_finger_4(self):
        self.assertEqual(([
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(1))
        )

    def test_positions_tone_finger_1(self):
        self.assertEqual(([
        (frozenset({1}), position_make(string=3, fret=8, fingers={3, 4})),
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=8, fingers=4)),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), position_make(string=4, fret=3, fingers=1)),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_tone_finger_1_4(self):
        self.assertEqual(([
        (frozenset({1, 2, 3}), position_make(string=3, fret=8, fingers={3, 4})),
           (frozenset({4}), position_make(string=4, fret=3, fingers=1)),
        ]),
        position_make(string=3, fret=6, fingers={1, 2, 3, 4})
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_2tone_finger_1(self):
        self.assertEqual(([
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(4))
        )

    def test_positions_2tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=4, fret=5, fingers={1,2})),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(4))
        )

    def test_positions_2tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), position_make(string=4, fret=5, fingers={1, 2, 3})),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(4))
        )