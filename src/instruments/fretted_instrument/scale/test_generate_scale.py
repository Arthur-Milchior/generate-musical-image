"""Unit tests for guitar scale generation.

This module verifies the low-level scale generation logic for the Guitar fretted
instrument. It exercises both the recursive `_generate_scale` generator and the
higher-level `generate_scale` function that groups generated scales by finger
patterns for Anki-style presentation.

Tests cover:
- single-octave major scale generation from a specific start position
- full-finger major scale enumeration
- two-octave major scale generation
- grouping of scales into `AnkiScaleWithString`
- SVG rendering for a sample scale
"""

import itertools
import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrumentFrozenList
from instruments.fretted_instrument.position.fretted_instrument_position_with_fingers import FrettedInstrumentPositionWithFingersFrozenList
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_for_interval import FrettedPositionMakerForInterval
from lily.lily_svg_utils import display_svg_file
from utils.util import ensure_folder, save_file
from .anki_scale import *
from solfege.pattern.scale.scale_patterns import major_scale, blues

from .anki_scale import _generate_scale

def position_make(string: int, fret:int, fingers:Set[int]):
    """Create a fingered guitar position for the test fixtures."""
    string = Guitar.string(string)
    fret = Fret.make(fret, True)
    return PositionOnFrettedInstrumentWithFingers.make(string = string, fret=fret, fingers=fingers)

# Expected major-scale fingering shapes used by the tests.

# Standard way to play the major scale on first string from index. Uses 4 frets.
major_1rst_string_standard_from_index = ([
    position_make(string=1, fret=12, fingers={1}),
    position_make(string=1, fret=14, fingers={4}),
    position_make(string=2, fret=11, fingers={1}),
    position_make(string=2, fret=12, fingers={2, 3}),
    position_make(string=2, fret=14, fingers={4}),
    position_make(string=3, fret=11, fingers={1}),
    position_make(string=3, fret=13, fingers={3}),
    position_make(string=3, fret=14, fingers={4})])

#Another way to play it, ending on string four, using 7 frets!
major_1rst_string_from_index_too_big = ([
    position_make(string=1, fret=12, fingers={1}), 
    position_make(string=1, fret=14, fingers={4}), 
    position_make(string=2, fret=11, fingers={1}), 
    position_make(string=2, fret=12, fingers={4}), 
    position_make(string=3, fret=9, fingers={1}), 
    position_make(string=3, fret=11, fingers={4}), 
    position_make(string=4, fret=8, fingers={1}), 
    position_make(string=4, fret=9, fingers={2, 3, 4}) ])

# Same as major_1rst_scale_standard_from_index but starting on any finger except four
major_1rst_string_standard_from_123 = ([
    position_make(string=1, fret=12, fingers={1, 2, 3}),
    position_make(string=1, fret=14, fingers={4}),
    position_make(string=2, fret=11, fingers={1}),
    position_make(string=2, fret=12, fingers={2, 3}),
    position_make(string=2, fret=14, fingers={4}),
    position_make(string=3, fret=11, fingers={1}),
    position_make(string=3, fret=13, fingers={3}),
    position_make(string=3, fret=14, fingers={4})])

major_1rst_string_from_123_too_big = ([
    position_make(1, 12, {1, 2, 3}),
    position_make(1, 14, {4}),
    position_make(2, 11, {1}),
    position_make(2, 12, {4}),
    position_make(3, 9, {1}),
    position_make(3, 11, {4}),
    position_make(4, 8, {1}),
    position_make(4, 9, {2, 3, 4})])

major_1rst_string_from_ring = ([
    position_make(1, 12, {4}),
    position_make(2, 9, {1}),
    position_make(2, 11, {3}),
    position_make(2, 12, {4}),
    position_make(3, 9, {1}),
    position_make(3, 11, {4}), 
    position_make(4, 8, {1}),
    position_make(4, 9, {2, 3, 4})])

major_2_octave_1 = ([position_make(1, 12, {1, 2, 3}), position_make(1, 14, {4}), position_make(2, 11, {1}), position_make(2, 12, {2, 3}), position_make(2, 14, {4}), position_make(3, 11, {1}), position_make(3, 13, {3}), position_make(3, 14, {4}), position_make(4, 11, {1}), position_make(4, 13, {3}), position_make(4, 14, {4}), position_make(5, 12, {1, 2, 3}), position_make(5, 14, {4}), position_make(6, 11, {1}), position_make(6, 12, {2, 3, 4})])
major_2_octave_2 = ([position_make(1, 12, {1, 2, 3}), position_make(1, 14, {4}), position_make(2, 11, {1}), position_make(2, 12, {2, 3}), position_make(2, 14, {4}), position_make(3, 11, {1}), position_make(3, 13, {3}), position_make(3, 14, {4}), position_make(4, 11, {1}), position_make(4, 13, {4}), position_make(5, 10, {1}), position_make(5, 12, {3}), position_make(5, 14, {4}), position_make(6, 11, {1}), position_make(6, 12, {2, 3, 4})])
major_2_octave_3 = ([position_make(1, 12, {1, 2, 3}), position_make(1, 14, {4}), position_make(2, 11, {1}), position_make(2, 12, {2, 3}), position_make(2, 14, {4}), position_make(3, 11, {1}), position_make(3, 13, {3}), position_make(3, 14, {4}), position_make(4, 11, {1}), position_make(4, 13, {4}), position_make(5, 10, {1}), position_make(5, 12, {4}), position_make(6, 9, {1}), position_make(6, 11, {3}), position_make(6, 12, {4})])
major_2_octave_4 = ([position_make(1, 12, {1, 2, 3}), position_make(1, 14, {4}), position_make(2, 11, {1}), position_make(2, 12, {4}), position_make(3, 9, {1}), position_make(3, 11, {4}), position_make(4, 8, {1}), position_make(4, 9, {2, 3}), position_make(4, 11, {4}), position_make(5, 9, {1, 2}), position_make(5, 10, {2, 3}), position_make(5, 12, {4}), position_make(6, 9, {1}), position_make(6, 11, {3}), position_make(6, 12, {4})])
major_2_octave_5 = ([position_make(1, 12, {4}), position_make(2, 9, {1}), position_make(2, 11, {3}), position_make(2, 12, {4}), position_make(3, 9, {1}), position_make(3, 11, {4}), position_make(4, 8, {1}), position_make(4, 9, {2, 3}), position_make(4, 11, {4}), position_make(5, 9, {1, 2}), position_make(5, 10, {2, 3}), position_make(5, 12, {4}), position_make(6, 9, {1}), position_make(6, 11, {3}), position_make(6, 12, {4})])


folder_path = "test/guitar/scale"

major_2_path = f"{folder_path}/major_2.svg"
major_3_path = f"{folder_path}/major_3.svg"
major_4_path = f"{folder_path}/major_4.svg"
major_5_path = f"{folder_path}/major_5.svg"
ensure_folder(folder_path)


strings = list(Guitar.strings())

for i, notes in enumerate([major_2_octave_1, major_2_octave_2, major_2_octave_3, major_2_octave_4, major_2_octave_5]):
    path = f"{folder_path}/major_{i}.svg"
    # save_file(path, SetOfFrettedInstrumentPositions.make(positions=notes).svg(absolute=False))
    # display_svg_file(path)

def anki_scale_make(*args, **kwargs):
    return AnkiScaleWithFingersAndString.make(Guitar, *args, **kwargs)

def set_of_pos_make(*args, **kwargs):
    return SetOfPositionOnFrettedInstrument.make(*args, **kwargs, absolute=True)

chromatic_relative_intervals = major_scale.get_interval_list().get_chromatic_interval_list().relative_intervals()
chromatic_relative_intervals_2_octaves = major_scale.multiple_octaves(2).get_chromatic_interval_list().relative_intervals()
class TestGenerateScale(unittest.TestCase):
    def assertEqualAnkiScaleWithFingersAndString(self, expected:AnkiScaleWithFingersAndString, actual: AnkiScaleWithFingersAndString):
        self.assertEqual(expected.start_string, actual.start_string)
        self.assertEqual(expected.number_of_octaves, actual.number_of_octaves)
        self.assertEqual(expected.first_fingers, actual.first_fingers)
        self.assertEqual(expected.pattern, actual.pattern)
        self.assert_equal_list_of_scales(expected.scales, actual.scales)

    def assertEqualAnkiScaleWithString(self, expected:AnkiScalesWithSameFirstString, actual: AnkiScalesWithSameFirstString):
        self.assertEqual(expected.start_string, actual.start_string)
        self.assertEqual(expected.number_of_octaves, actual.number_of_octaves)
        self.assertEqual(expected.pattern, actual.pattern)
        for expected_fingers in expected.fingers_to_scales:
            self.assertIn(expected_fingers, actual.fingers_to_scales)
            self.assertEqualAnkiScaleWithFingersAndString(expected.fingers_to_scales[expected_fingers], actual.fingers_to_scales[expected_fingers])
        for actual_fingers in actual.fingers_to_scales:
            self.assertIn(actual_fingers, expected.fingers_to_scales)
            self.assertEqualAnkiScaleWithFingersAndString(expected.fingers_to_scales[actual_fingers], actual.fingers_to_scales[actual_fingers])

    def assert_equal_list_of_scales(self, expecteds, actuals):
        self.assertEqual(len(expecteds), len(actuals))
        for i, (expected, actual) in enumerate(itertools.zip_longest(expecteds, actuals)):
            self.assertEqual(expected, actual, f"\n\n{i}-th scale differs:\n{expecteds[i]}\n{actuals[i]}")

    def assert_equal_list_of_anki_notes(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i], actual[i], f"\n\n{i}-th anki note differs:\n{expected[i]}\n{actual[i]}")

    def test_major_1(self):
        """Verify `_generate_scale` returns the two expected major-scale paths for a one-octave scale starting on string 1."""
        # The scale (1, 12), (1, 14), (1, 16), (2, 12), (2, 14), (3,11), (3, 13), (3, 14) is not generated because it requires to have 2 frets difference between two fingers that are closed together on first string.
        expected = [major_1rst_string_standard_from_index, major_1rst_string_from_index_too_big]
        actual = _generate_scale(Guitar,
                position_make(string=1, fret=12, fingers=1),
                chromatic_relative_intervals)
        self.assertEqual(expected, list(actual))
        
    def test_major_all_fingers(self):
        """Verify that when all fingers are allowed, `_generate_scale` finds all valid one-octave major-scale shapes starting from the same note."""
        expected = [major_1rst_string_standard_from_123, major_1rst_string_from_123_too_big, major_1rst_string_from_ring]
        actual = _generate_scale(
            Guitar,
            position_make(string=1, fret=12, fingers=[1, 2, 3, 4]),
            chromatic_relative_intervals)
        self.assertEqual(expected, list(actual))
        
    def test_2_major_all_fingers(self):
        """Verify that two-octave major-scale generation enumerates the expected fingering variants from a single start position."""
        self.assert_equal_list_of_scales(
            [major_2_octave_1, major_2_octave_2,
              major_2_octave_3, major_2_octave_4, major_2_octave_5, 
             ],
            list(_generate_scale(Guitar,
                position_make(string=1, fret=12, fingers=[1, 2, 3, 4]),
                chromatic_relative_intervals_2_octaves)),
        )
        
        
    def test_anki_notes(self):
        """Verify `generate_scale` correctly groups generated major-scale variants by starting finger set into an Anki-style scale object."""
        one_two_three = anki_scale_make(
            start_string=strings[0], 
            number_of_octaves=2,
            fingers = frozenset({1, 2, 3}),
            scales=[
                set_of_pos_make(major_2_octave_1), set_of_pos_make(major_2_octave_2), set_of_pos_make(major_2_octave_3), set_of_pos_make(major_2_octave_4)
            ],
            pattern=major_scale)
        four =  anki_scale_make(
            start_string=strings[0], 
            number_of_octaves=2, 
            fingers = frozenset({4}),
            pattern=major_scale,
            scales=[set_of_pos_make(major_2_octave_5)])
        expected_scale_with_string = AnkiScalesWithSameFirstString.make(instrument=Guitar, start_string=strings[0], number_of_octaves=2, pattern=major_scale, fingers_to_scales={ 
                frozenset({1, 2, 3}): one_two_three,
                frozenset({4}):four,
            })
        actual = generate_scale(Guitar, 
                position_make(string=1, fret=12, fingers=[1, 2, 3, 4]),
                major_scale, 2)
        self.assertEqualAnkiScaleWithString(
            expected_scale_with_string,
            actual
        )

    
    def test_show_scale(self):
        """Verify that a generated blues scale can be saved as an SVG diagram without raising errors."""
        first_position = PositionOnFrettedInstrument.make(Guitar.string(2), Fret(3, absolute=False))
        tonic = first_position.get_chromatic()
        maker = FrettedPositionMakerForInterval.make(tonic=tonic, pattern=blues)
        position_list = PositionOnFrettedInstrumentFrozenList(
            [
              first_position, 
              (Guitar.string(2), Fret(6, absolute=False)),
              (Guitar.string(3), Fret(3, absolute=False)),
              (Guitar.string(3), Fret(4, absolute=False)),
              (Guitar.string(3), Fret(5, absolute=False)),
              (Guitar.string(4), Fret(3, absolute=False)),
              (Guitar.string(5), Fret(1, absolute=False)),
             ]
        )
        scale = SetOfPositionOnFrettedInstrument.make(position_list, absolute=False)
        file_name = scale.save_svg(folder_path, instrument=Guitar, fretted_position_maker=maker)
        # display_svg_file(f"{folder_path}/{file_name}" )
        # uncomment to see what the image looks like
        
    # def test_pentatonic_major_finger_2(self):
    #     actual = generate_scale(instrument= Guitar,
    #                             start_pos=position_make(string=1, fret=12, fingers=[2]),
    #                             scale_pattern=pentatonic_major, number_of_octaves=2)
    #     self.assertEqual(actual, None)