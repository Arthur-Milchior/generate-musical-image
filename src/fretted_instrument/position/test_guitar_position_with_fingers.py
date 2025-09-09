import unittest

from utils.frozenlist import FrozenList
from .guitar_position_with_fingers import *

class TestGuitarPositionWithFingerss(unittest.TestCase):
    def test_positions_minus_tone_finger_1(self):
        self.assertEqual(([
            (frozenset({1}), GuitarPositionWithFingers.make(string=2, fret=9, fingers=4)),
            ]),
            GuitarPositionWithFingers.make(string=3, fret=6, fingers=1)
            .positions_for_interval(ChromaticInterval(-2))
            )

    def test_positions_minus_half_tone_finger_1(self):
        self.assertEqual([],
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(-1))
        )

    def test_positions_minus_half_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), GuitarPositionWithFingers.make(string=3, fret=5, fingers={1, 2})),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(-1))
        )

    def test_positions_minus_half_tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), GuitarPositionWithFingers.make(string=3, fret=5, fingers={1, 2, 3})),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(-1))
        )

        
    def test_positions_half_tone_finger_1(self):
        self.assertEqual(([
        (frozenset({1}), GuitarPositionWithFingers.make(string=3, fret=7, fingers={2, 3, 4})),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(1))
        )

    def test_positions_half_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), GuitarPositionWithFingers.make(string=3, fret=7, fingers=4)),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(1))
        )

    def test_positions_half_tone_finger_4(self):
        self.assertEqual(([
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(1))
        )

    def test_positions_tone_finger_1(self):
        self.assertEqual(([
        (frozenset({1}), GuitarPositionWithFingers.make(string=3, fret=8, fingers={3, 4})),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), GuitarPositionWithFingers.make(string=3, fret=8, fingers=4)),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), GuitarPositionWithFingers.make(string=4, fret=3, fingers=1)),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_tone_finger_1_4(self):
        self.assertEqual(([
        (frozenset({1, 2, 3}), GuitarPositionWithFingers.make(string=3, fret=8, fingers={3, 4})),
           (frozenset({4}), GuitarPositionWithFingers.make(string=4, fret=3, fingers=1)),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers={1, 2, 3, 4})
        .positions_for_interval(ChromaticInterval(2))
        )

    def test_positions_2tone_finger_1(self):
        self.assertEqual(([
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=1)
        .positions_for_interval(ChromaticInterval(4))
        )

    def test_positions_2tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), GuitarPositionWithFingers.make(string=4, fret=5, fingers={1,2})),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=3)
        .positions_for_interval(ChromaticInterval(4))
        )

    def test_positions_2tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), GuitarPositionWithFingers.make(string=4, fret=5, fingers={1, 2, 3})),
        ]),
        GuitarPositionWithFingers.make(string=3, fret=6, fingers=4)
        .positions_for_interval(ChromaticInterval(4))
        )