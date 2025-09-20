from typing import Union
import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from utils.frozenlist import FrozenList
from .fretted_instrument_position_with_fingers import *

def position_make(string: int, fret: int, fingers: Union[int, Set[int]]):
    if isinstance(string, int):
        string = Guitar.string(string)
    if isinstance(fret, int):
        fret = Fret(fret, True)
    if isinstance(fingers, int):
        fingers = {fingers}
    return PositionOnFrettedInstrumentWithFingers.make(string=string, fret=fret, fingers=fingers)

any_string = StringDelta.ANY_STRING(Guitar)
class TestFrettedInstrumentPositionWithFingerss(unittest.TestCase):
    def test_positions_minus_tone_finger_1(self):
        expected_position = position_make(string=2, fret=9, fingers=4)
        start_position = position_make(string=3, fret=6, fingers=1)
        interval =ChromaticInterval(-2)
        fingers_position_list = start_position.positions_for_interval(instrument=Guitar, interval=interval, string_delta=any_string)
        self.assertEqual(len(fingers_position_list), 1)
        fingers, position = fingers_position_list[0]
        self.assertEqual(fingers, frozenset({1}))
        self.assertEqual(position, expected_position)

    def test_positions_minus_half_tone_finger_1(self):
        self.assertEqual([],
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval(-1))
        )

    def test_positions_minus_half_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=5, fingers={1, 2})),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval(-1))
        )

    def test_positions_minus_half_tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), position_make(string=3, fret=5, fingers={1, 2, 3})),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval(-1))
        )

        
    def test_positions_half_tone_finger_1(self):
        self.assertEqual(([
        (frozenset({1}), position_make(string=3, fret=7, fingers={2, 3, 4})),
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval(1))
        )

    def test_positions_half_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=7, fingers=4)),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval(1))
        )

    def test_positions_half_tone_finger_4(self):
        self.assertEqual(([
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval(1))
        )

    def test_positions_tone_finger_1(self):
        self.assertEqual(([
        (frozenset({1}), position_make(string=3, fret=8, fingers={3, 4})),
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval(2))
        )

    def test_positions_tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=8, fingers=4)),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval(2))
        )

    def test_positions_tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), position_make(string=4, fret=3, fingers=1)),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval(2))
        )

    def test_positions_tone_finger_1_4(self):
        self.assertEqual(([
        (frozenset({1, 2, 3}), position_make(string=3, fret=8, fingers={3, 4})),
           (frozenset({4}), position_make(string=4, fret=3, fingers=1)),
        ]),
        position_make(string=3, fret=6, fingers={1, 2, 3, 4})
        .positions_for_interval(Guitar, ChromaticInterval(2))
        )

    def test_positions_2tone_finger_1(self):
        self.assertEqual(([
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval(4))
        )

    def test_positions_2tone_finger_3(self):
        self.assertEqual(([
        (frozenset({3}), position_make(string=4, fret=5, fingers={1,2})),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval(4))
        )

    def test_positions_2tone_finger_4(self):
        self.assertEqual(([
        (frozenset({4}), position_make(string=4, fret=5, fingers={1, 2, 3})),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval(4))
        )

    def test_restrict_to_compatible(self):
        current_note = position_make(1, 12, {1, 2, 3})
        next_note = position_make(1, 14, {3})
        expected_note = position_make(1, 12, {1})
        self.assertEqual(expected_note, current_note.restrict_to_compatible_fingering(Guitar, next_note))
