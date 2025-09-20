import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position_with_fingers import FrettedInstrumentPositionWithFingersFrozenList
from lily.lily_svg import display_svg_file
from utils.util import ensure_folder, save_file
from .generate_scale import *
from solfege.pattern.scale.scale_patterns import major_scale, pentatonic_major

from .generate_scale import _generate_scale

def position_make(string: int, fret:int, fingers:Set[int]):
    string = Guitar.string(string)
    fret = Fret(fret, True)
    return PositionOnFrettedInstrumentWithFingers.make(string = string, fret=fret, fingers=fingers)

major_1_1 = ([
    position_make(string=1, fret=12, fingers={1}),
    position_make(string=1, fret=14, fingers={4}),
    position_make(string=2, fret=11, fingers={1}),
    position_make(string=2, fret=12, fingers={2, 3}),
    position_make(string=2, fret=14, fingers={4}),
    position_make(string=3, fret=11, fingers={1}),
    position_make(string=3, fret=13, fingers={3}),
    position_make(string=3, fret=14, fingers={4})])
major_2_1 = ([
    position_make(string=1, fret=12, fingers={1}), 
    position_make(string=1, fret=14, fingers={4}), 
    position_make(string=2, fret=11, fingers={1}), 
    position_make(string=2, fret=12, fingers={4}), 
    position_make(string=3, fret=9, fingers={1}), 
    position_make(string=3, fret=11, fingers={4}), 
    position_make(string=4, fret=8, fingers={1}), 
    position_make(string=4, fret=9, fingers={2, 3, 4}) ])

major_1_2 = ([
    position_make(string=1, fret=12, fingers={1, 2, 3}),
    position_make(string=1, fret=14, fingers={4}),
    position_make(string=2, fret=11, fingers={1}),
    position_make(string=2, fret=12, fingers={2, 3}),
    position_make(string=2, fret=14, fingers={4}),
    position_make(string=3, fret=11, fingers={1}),
    position_make(string=3, fret=13, fingers={3}),
    position_make(string=3, fret=14, fingers={4})])

major_2_2 = ([position_make(1, 12, {1, 2, 3}),
                        position_make(1, 14, {4}),
                        position_make(2, 11, {1}),
                        position_make(2, 12, {4}),
                        position_make(3, 9, {1}),
                        position_make(3, 11, {4}),
                        position_make(4, 8, {1}),
                        position_make(4, 9, {2, 3, 4})])

major_3_2 = ([position_make(1, 12, {4}),
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
major_2_octave_4 = ([position_make(1, 12, {1, 2, 3}), position_make(1, 14, {4}), position_make(2, 11, {1}), position_make(2, 12, {4}), position_make(3, 9, {1}), position_make(3, 11, {4}), position_make(4, 8, {1}), position_make(4, 9, {2, 3}), position_make(4, 11, {4}), position_make(5, 9, {1, 2, 3}), position_make(5, 10, {2, 3}), position_make(5, 12, {4}), position_make(6, 9, {1}), position_make(6, 11, {3}), position_make(6, 12, {4})])
major_2_octave_5 = ([position_make(1, 12, {4}), position_make(2, 9, {1}), position_make(2, 11, {3}), position_make(2, 12, {4}), position_make(3, 9, {1}), position_make(3, 11, {4}), position_make(4, 8, {1}), position_make(4, 9, {2, 3}), position_make(4, 11, {4}), position_make(5, 9, {1, 2, 3}), position_make(5, 10, {2, 3}), position_make(5, 12, {4}), position_make(6, 9, {1}), position_make(6, 11, {3}), position_make(6, 12, {4})])


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
        self.assertEqual(expected.fingers, actual.fingers)
        self.assertEqual(expected.pattern, actual.pattern)
        self.assert_equal_list_of_scales(expected.scales, actual.scales)

    def assertEqualAnkiScaleWithString(self, expected:AnkiScaleWithString, actual: AnkiScaleWithString):
        self.assertEqual(expected.start_string, actual.start_string)
        self.assertEqual(expected.number_of_octaves, actual.number_of_octaves)
        self.assertEqual(expected.pattern, actual.pattern)
        for expected_fingers in expected.fingers_to_scales:
            self.assertIn(expected_fingers, actual.fingers_to_scales)
            self.assertEqualAnkiScaleWithFingersAndString(expected.fingers_to_scales[expected_fingers], actual.fingers_to_scales[expected_fingers])
        for actual_fingers in actual.fingers_to_scales:
            self.assertIn(actual_fingers, expected.fingers_to_scales)
            self.assertEqualAnkiScaleWithFingersAndString(expected.fingers_to_scales[actual_fingers], actual.fingers_to_scales[actual_fingers])

    def assert_equal_list_of_scales(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i], actual[i], f"\n\n{i}-th scale differs:\n{expected[i]}\n{actual[i]}")

    def assert_equal_list_of_anki_notes(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i], actual[i], f"\n\n{i}-th anki note differs:\n{expected[i]}\n{actual[i]}")

    def test_major_1(self):
        
        expected = [major_1_1, major_2_1]
        actual = list(_generate_scale(Guitar,
            position_make(string=1, fret=12, fingers=1),
            chromatic_relative_intervals))
        self.assertEqual(expected, actual)
        
    def test_major_all_fingers(self):
        self.assertEqual(
            [major_1_2, major_2_2, major_3_2],
            list(_generate_scale(Guitar,
                position_make(string=1, fret=12, fingers=[1, 2, 3, 4]),
                chromatic_relative_intervals)),
        )
        
    def test_2_major_all_fingers(self):
        self.assert_equal_list_of_scales(
            [major_2_octave_1, major_2_octave_2,
              major_2_octave_3, major_2_octave_4, major_2_octave_5, 
             ],
            list(_generate_scale(Guitar,
                position_make(string=1, fret=12, fingers=[1, 2, 3, 4]),
                chromatic_relative_intervals_2_octaves)),
        )
        
        
    def test_anki_notes(self):
        one_two_three = anki_scale_make(start_string=strings[0], number_of_octaves=2, fingers = frozenset({1, 2, 3}), scales=[
                set_of_pos_make(major_2_octave_1), set_of_pos_make(major_2_octave_2), set_of_pos_make(major_2_octave_3), set_of_pos_make(major_2_octave_4)
            ], pattern=major_scale)
        four =  anki_scale_make(start_string=strings[0], number_of_octaves=2, fingers = frozenset({4}), pattern=major_scale, scales=[set_of_pos_make(major_2_octave_5)])
        expected_scale_with_string = AnkiScaleWithString.make(instrument=Guitar, start_string=strings[0], number_of_octaves=2, pattern=major_scale, fingers_to_scales={ 
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
        
    def test_pentatonic_major_finger_2(self):
        actual = generate_scale(instrument= Guitar,
                                start_pos=position_make(string=1, fret=12, fingers=[2]),
                                scale_pattern=pentatonic_major, number_of_octaves=2)
        self.assertEqual(actual, None)