from typing import Union
import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from utils.frozenlist import FrozenList
from .fretted_instrument_position_with_fingers import *

def position_make(string: int, fret: int, fingers: Union[int, Set[int]]):
    """Shorthand to build a `PositionOnFrettedInstrumentWithFingers` from raw string/fret numbers and fingers."""
    if isinstance(string, int):
        string = Guitar.string(string)
    if isinstance(fret, int):
        fret = Fret.make(fret, True)
    if isinstance(fingers, int):
        fingers = {fingers}
    return PositionOnFrettedInstrumentWithFingers.make(string=string, fret=fret, fingers=fingers)

any_string = StringDelta.ANY_STRING(Guitar)
class TestFrettedInstrumentPositionWithFingerss(unittest.TestCase):
    def test_positions_minus_tone_finger_1(self):
        """Moving a whole tone down from finger 1 resolves to a single reachable position/finger pair."""
        expected_position = position_make(string=2, fret=9, fingers=4)
        start_position = position_make(string=3, fret=6, fingers=1)
        interval =ChromaticInterval.make(-2)
        fingers_position_list = start_position.positions_for_interval(instrument=Guitar, interval=interval, chord = True, string_delta=any_string)
        self.assertEqual(len(fingers_position_list), 1)
        fingers, position = fingers_position_list[0]
        self.assertEqual(fingers, frozenset({1}))
        self.assertEqual(position, expected_position)

    def test_positions_minus_half_tone_finger_1(self):
        """Finger 1 cannot reach a half-tone below itself: no compatible position exists."""
        self.assertEqual([],
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval.make(-1), chord = True)
        )

    def test_positions_minus_half_tone_finger_3(self):
        """Finger 3 reaches a half-tone below via fingers 1 or 2 on the target position."""
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=5, fingers={1, 2})),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval.make(-1), chord = True)
        )

    def test_positions_minus_half_tone_finger_4(self):
        """Finger 4 reaches a half-tone below via fingers 1, 2 or 3 on the target position."""
        self.assertEqual(([
        (frozenset({4}), position_make(string=3, fret=5, fingers={1, 2, 3})),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval.make(-1), chord = True)
        )

        
    def test_positions_half_tone_finger_1(self):
        """Finger 1 reaches a half-tone above via fingers 2, 3 or 4 on the target position."""
        self.assertEqual(([
        (frozenset({1}), position_make(string=3, fret=7, fingers={2, 3, 4})),
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval.make(1), chord = True)
        )

    def test_positions_half_tone_finger_3(self):
        """Finger 3 reaches a half-tone above via finger 4 on the target position."""
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=7, fingers=4)),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval.make(1), chord = True)
        )

    def test_positions_half_tone_finger_4(self):
        """Finger 4 cannot reach a half-tone above itself: no compatible position exists."""
        self.assertEqual(([
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval.make(1), chord = True)
        )

    def test_positions_tone_finger_1(self):
        """Finger 1 reaches a whole tone above via fingers 3 or 4 on the target position."""
        self.assertEqual(([
        (frozenset({1}), position_make(string=3, fret=8, fingers={3, 4})),
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval.make(2), chord = True)
        )

    def test_positions_tone_finger_3(self):
        """Finger 3 reaches a whole tone above, on the same string, via finger 4."""
        self.assertEqual(([
        (frozenset({3}), position_make(string=3, fret=8, fingers=4)),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval.make(2), chord = True)
        )

    def test_positions_tone_finger_4(self):
        """Finger 4 reaches a whole tone above by shifting to the next string, via finger 1."""
        self.assertEqual(([
        (frozenset({4}), position_make(string=4, fret=3, fingers=1)),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval.make(2), chord = True)
        )

    def test_positions_tone_finger_1_4(self):
        """With all fingers as candidates, a whole-tone move can land on either of the two positions reachable from individual fingers, each keyed by its own set of compatible current-note fingers."""
        self.assertEqual(([
        (frozenset({1, 2, 3}), position_make(string=3, fret=8, fingers={3, 4})),
           (frozenset({4}), position_make(string=4, fret=3, fingers=1)),
        ]),
        position_make(string=3, fret=6, fingers={1, 2, 3, 4})
        .positions_for_interval(Guitar, ChromaticInterval.make(2), chord = True)
        )

    def test_positions_2tone_finger_1(self):
        """Finger 1 cannot reach two whole tones above: no compatible position exists."""
        self.assertEqual(([
        ]),
        position_make(string=3, fret=6, fingers=1)
        .positions_for_interval(Guitar, ChromaticInterval.make(4), chord = True)
        )

    def test_positions_2tone_finger_3(self):
        """Finger 3 reaches two whole tones above, on the next string, via fingers 1 or 2."""
        self.assertEqual(([
        (frozenset({3}), position_make(string=4, fret=5, fingers={1,2})),
        ]),
        position_make(string=3, fret=6, fingers=3)
        .positions_for_interval(Guitar, ChromaticInterval.make(4), chord = True)
        )

    def test_positions_2tone_finger_4(self):
        """Finger 4 reaches two whole tones above, on the next string, via fingers 1, 2 or 3."""
        self.assertEqual(([
        (frozenset({4}), position_make(string=4, fret=5, fingers={1, 2, 3})),
        ]),
        position_make(string=3, fret=6, fingers=4)
        .positions_for_interval(Guitar, ChromaticInterval.make(4), chord = True)
        )

    def test_restrict_to_compatible(self):
        """`restrict_to_compatible_fingering` narrows candidate fingers to those compatible with a fixed next-note finger."""
        current_note = position_make(1, 12, {1, 2, 3})
        next_note = position_make(1, 14, {3})
        expected_note = position_make(1, 12, {1})
        self.assertEqual(expected_note, current_note.restrict_to_compatible_fingering(Guitar, next_note, chord=True))
