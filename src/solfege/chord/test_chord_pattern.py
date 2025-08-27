import unittest

from .chord_pattern import *

from solfege.key.key import *


dominant_seventh_chord = ChordPattern.make_absolute(names=["Dominant seventh chord", "major minor seventh chord"], notation="<sup>7</sup>",
                                      absolute_intervals=[(4, 2), (7, 4), (10, 6)], optional_fifth=True,
                                      interval_for_signature=one_flat)

class TestChordPattern(unittest.TestCase):
    def test_il_found(self):
        il = IntervalList.make_absolute([(4, 2), (7, 4), (10, 6)])
        self.assertEqual(dominant_seventh_chord, ChordPattern.get_pattern_from_interval(il))

    def test_il_no_fifth_found(self):
        il = IntervalList.make_absolute([(4, 2), (10, 6)])
        self.assertEqual(dominant_seventh_chord, ChordPattern.get_pattern_from_interval(il))

    def test_il_chromatic_found(self):
        il = ChromaticIntervalList.make_absolute([4, 7, 10])
        self.assertEqual(dominant_seventh_chord, ChordPattern.get_pattern_from_chromatic_interval(il))

    def test_il_no_fifth_chromatic_found(self):
        il = ChromaticIntervalList.make_absolute([4, 10])
        self.assertEqual(dominant_seventh_chord, ChordPattern.get_pattern_from_chromatic_interval(il))