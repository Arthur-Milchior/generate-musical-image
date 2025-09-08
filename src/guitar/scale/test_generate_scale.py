import unittest

from lily.svg import display_svg_file
from utils.util import ensure_folder, save_file
from .generate_scale import *
from solfege.pattern.scale.scale_patterns import major_scale

from .generate_scale import _generate_scale

major_1_1 = FrozenList([
    GuitarPositionWithFingers.make(string=1, fret=12, fingers={1}),
    GuitarPositionWithFingers.make(string=1, fret=14, fingers={3, 4}),
    GuitarPositionWithFingers.make(string=2, fret=11, fingers={1}),
    GuitarPositionWithFingers.make(string=2, fret=12, fingers={2, 3, 4}),
    GuitarPositionWithFingers.make(string=2, fret=14, fingers={4}),
    GuitarPositionWithFingers.make(string=3, fret=11, fingers={1}),
    GuitarPositionWithFingers.make(string=3, fret=13, fingers={3, 4}),
    GuitarPositionWithFingers.make(string=3, fret=14, fingers={4})])
major_2_1 = FrozenList([
    GuitarPositionWithFingers.make(string=1, fret=12, fingers={1}), 
    GuitarPositionWithFingers.make(string=1, fret=14, fingers={3, 4}), 
    GuitarPositionWithFingers.make(string=2, fret=11, fingers={1}), 
    GuitarPositionWithFingers.make(string=2, fret=12, fingers={2, 3, 4}), 
    GuitarPositionWithFingers.make(string=3, fret=9, fingers={1}), 
    GuitarPositionWithFingers.make(string=3, fret=11, fingers={3, 4}), 
    GuitarPositionWithFingers.make(string=4, fret=8, fingers={1}), 
    GuitarPositionWithFingers.make(string=4, fret=9, fingers={2, 3, 4}) ])

major_1_2 = FrozenList([
    GuitarPositionWithFingers.make(string=1, fret=12, fingers={1, 2, 3, 4}),
    GuitarPositionWithFingers.make(string=1, fret=14, fingers={3, 4}),
    GuitarPositionWithFingers.make(string=2, fret=11, fingers={1}),
    GuitarPositionWithFingers.make(string=2, fret=12, fingers={2, 3, 4}),
    GuitarPositionWithFingers.make(string=2, fret=14, fingers={4}),
    GuitarPositionWithFingers.make(string=3, fret=11, fingers={1}),
    GuitarPositionWithFingers.make(string=3, fret=13, fingers={3, 4}),
    GuitarPositionWithFingers.make(string=3, fret=14, fingers={4})])

major_2_2 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}),
                        GuitarPositionWithFingers.make(1, 14, {3, 4}),
                        GuitarPositionWithFingers.make(2, 11, {1}),
                        GuitarPositionWithFingers.make(2, 12, {2, 3, 4}),
                        GuitarPositionWithFingers.make(3, 9, {1}),
                        GuitarPositionWithFingers.make(3, 11, {3, 4}),
                        GuitarPositionWithFingers.make(4, 8, {1}),
                        GuitarPositionWithFingers.make(4, 9, {2, 3, 4})])

major_3_2 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}),
                        GuitarPositionWithFingers.make(2, 9, {1}),
                        GuitarPositionWithFingers.make(2, 11, {3, 4}),
                        GuitarPositionWithFingers.make(2, 12, {4}),
                        GuitarPositionWithFingers.make(3, 9, {1}),
                        GuitarPositionWithFingers.make(3, 11, {3, 4}), 
                        GuitarPositionWithFingers.make(4, 8, {1}),
                        GuitarPositionWithFingers.make(4, 9, {2, 3, 4})])

major_2_octave_1 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}), GuitarPositionWithFingers.make(1, 14, {3, 4}), GuitarPositionWithFingers.make(2, 11, {1}), GuitarPositionWithFingers.make(2, 12, {2, 3, 4}), GuitarPositionWithFingers.make(2, 14, {4}), GuitarPositionWithFingers.make(3, 11, {1}), GuitarPositionWithFingers.make(3, 13, {3, 4}), GuitarPositionWithFingers.make(3, 14, {4}), GuitarPositionWithFingers.make(4, 11, {1}), GuitarPositionWithFingers.make(4, 13, {3, 4}), GuitarPositionWithFingers.make(4, 14, {4}), GuitarPositionWithFingers.make(5, 12, {1, 2, 3}), GuitarPositionWithFingers.make(5, 14, {3, 4}), GuitarPositionWithFingers.make(6, 11, {1}), GuitarPositionWithFingers.make(6, 12, {2, 3, 4})])
major_2_octave_2 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}), GuitarPositionWithFingers.make(1, 14, {3, 4}), GuitarPositionWithFingers.make(2, 11, {1}), GuitarPositionWithFingers.make(2, 12, {2, 3, 4}), GuitarPositionWithFingers.make(2, 14, {4}), GuitarPositionWithFingers.make(3, 11, {1}), GuitarPositionWithFingers.make(3, 13, {3, 4}), GuitarPositionWithFingers.make(3, 14, {4}), GuitarPositionWithFingers.make(4, 11, {1}), GuitarPositionWithFingers.make(4, 13, {3, 4}), GuitarPositionWithFingers.make(5, 10, {1}), GuitarPositionWithFingers.make(5, 12, {3, 4}), GuitarPositionWithFingers.make(5, 14, {4}), GuitarPositionWithFingers.make(6, 11, {1}), GuitarPositionWithFingers.make(6, 12, {2, 3, 4})])
major_2_octave_3 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}), GuitarPositionWithFingers.make(1, 14, {3, 4}), GuitarPositionWithFingers.make(2, 11, {1}), GuitarPositionWithFingers.make(2, 12, {2, 3, 4}), GuitarPositionWithFingers.make(2, 14, {4}), GuitarPositionWithFingers.make(3, 11, {1}), GuitarPositionWithFingers.make(3, 13, {3, 4}), GuitarPositionWithFingers.make(3, 14, {4}), GuitarPositionWithFingers.make(4, 11, {1}), GuitarPositionWithFingers.make(4, 13, {3, 4}), GuitarPositionWithFingers.make(5, 10, {1}), GuitarPositionWithFingers.make(5, 12, {3, 4}), GuitarPositionWithFingers.make(6, 9, {1}), GuitarPositionWithFingers.make(6, 11, {3, 4}), GuitarPositionWithFingers.make(6, 12, {4})])
major_2_octave_4 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}), GuitarPositionWithFingers.make(1, 14, {3, 4}), GuitarPositionWithFingers.make(2, 11, {1}), GuitarPositionWithFingers.make(2, 12, {2, 3, 4}), GuitarPositionWithFingers.make(3, 9, {1}), GuitarPositionWithFingers.make(3, 11, {3, 4}), GuitarPositionWithFingers.make(4, 8, {1}), GuitarPositionWithFingers.make(4, 9, {2, 3, 4}), GuitarPositionWithFingers.make(4, 11, {4}), GuitarPositionWithFingers.make(5, 9, {1, 2, 3}), GuitarPositionWithFingers.make(5, 10, {2, 3, 4}), GuitarPositionWithFingers.make(5, 12, {4}), GuitarPositionWithFingers.make(6, 9, {1}), GuitarPositionWithFingers.make(6, 11, {3, 4}), GuitarPositionWithFingers.make(6, 12, {4})])
major_2_octave_5 = FrozenList([GuitarPositionWithFingers.make(1, 12, {1, 2, 3, 4}), GuitarPositionWithFingers.make(2, 9, {1}), GuitarPositionWithFingers.make(2, 11, {3, 4}), GuitarPositionWithFingers.make(2, 12, {4}), GuitarPositionWithFingers.make(3, 9, {1}), GuitarPositionWithFingers.make(3, 11, {3, 4}), GuitarPositionWithFingers.make(4, 8, {1}), GuitarPositionWithFingers.make(4, 9, {2, 3, 4}), GuitarPositionWithFingers.make(4, 11, {4}), GuitarPositionWithFingers.make(5, 9, {1, 2, 3}), GuitarPositionWithFingers.make(5, 10, {2, 3, 4}), GuitarPositionWithFingers.make(5, 12, {4}), GuitarPositionWithFingers.make(6, 9, {1}), GuitarPositionWithFingers.make(6, 11, {3, 4}), GuitarPositionWithFingers.make(6, 12, {4})])


folder_path = "test/guitar/scale"

major_2_path = f"{folder_path}/major_2.svg"
major_3_path = f"{folder_path}/major_3.svg"
major_4_path = f"{folder_path}/major_4.svg"
major_5_path = f"{folder_path}/major_5.svg"
ensure_folder(folder_path)

for i, notes in enumerate([major_2_octave_1, major_2_octave_2, major_2_octave_3, major_2_octave_4, major_2_octave_5]):
    path = f"{folder_path}/major_{i}.svg"
    save_file(path, SetOfGuitarPositions.make(positions=notes).svg(absolute=False))
    display_svg_file(path)

class TestGenerateScale(unittest.TestCase):
    def assert_equal_list_of_scales(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(expected[i], actual[i])

    def test_major_1(self):
        self.assertEqual(list(
            _generate_scale(
            GuitarPositionWithFingers.make(string=1, fret=12, fingers=1),
            major_scale.relative_chromatic())),
                       [major_1_1, major_2_1]
                       )
        
    def test_major_all_fingers(self):
        self.assertEqual(
            [major_1_2, major_2_2, major_3_2],
            list(_generate_scale(
                GuitarPositionWithFingers.make(string=1, fret=12, fingers=[1, 2, 3, 4]),
                major_scale.relative_chromatic())),
        )
        
    def test_2_major_all_fingers(self):
        self.assertEqual(
            [major_2_octave_1, major_2_octave_2,
              major_2_octave_3, major_2_octave_4, major_2_octave_5, 
             ],
            list(_generate_scale(
                GuitarPositionWithFingers.make(string=1, fret=12, fingers=[1, 2, 3, 4]),
                major_scale.multiple_octaves(2).get_chromatic_interval_list().relative_chromatic())),
        )
        
