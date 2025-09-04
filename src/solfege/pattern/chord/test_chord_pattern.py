import unittest

from solfege.pattern.chord.chord_pattern import *

from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.interval_to_pattern import IntervalToPattern
from solfege.value.key.key import *
from solfege.pattern.chord.test_constants import *


class TestChordPattern(unittest.TestCase):
    def test_il_found(self):
        il = IntervalList.make_absolute([(4, 2), (7, 4), (10, 6)])
        print("========\nkeys are\n:")
        for key in interval_to_chord._interval_to_patterns:
            print(f"* {key=}")
        self.assertEqual([dominant_seventh_chord], interval_to_chord.get_patterns_from_interval(il))

    def test_il_no_fifth_found(self):
        il = IntervalList.make_absolute([(4, 2), (10, 6)])
        self.assertEqual([dominant_seventh_chord], interval_to_chord.get_patterns_from_interval(il))

    def test_il_chromatic_found(self):
        il_chromatic = ChromaticIntervalList.make_absolute([4, 7, 10])
        self.assertEqual([dominant_seventh_chord], interval_to_chord.get_patterns_from_chromatic_interval(il_chromatic))

    def test_il_no_fifth_chromatic_found(self):
        il = IntervalList.make_absolute([(4, 2), (10, 6)])
        il_chromatic = ChromaticIntervalList.make_absolute([4, 10])
        self.assertEqual([dominant_seventh_chord], interval_to_chord.get_patterns_from_chromatic_interval(il_chromatic))

    def test_inversion(self):
        self.assertEqual(dominant_seventh_chord.inversion(0), dominant_seventh_chord_zeroth_inversion)
        self.assertEqual(dominant_seventh_chord.inversion(1), dominant_seventh_chord_first_inversion)
        self.assertEqual(dominant_seventh_chord.inversion(2), dominant_seventh_chord_second_inversion)
        self.assertEqual(dominant_seventh_chord.inversion(3), dominant_seventh_chord_third_inversion)

    def test_inversions(self):
        inversions = dominant_seventh_chord.compute_all_inversions()
        self.assertEqual(len(inversions), 7)
        self.assertEqual(inversions[0], dominant_seventh_chord_zeroth_inversion)
        self.assertEqual(inversions[1], 
                            dominant_seventh_chord_no_fifth_zeroth_inversion,)
        self.assertEqual(inversions[2], 
                            dominant_seventh_chord_first_inversion,)
        self.assertEqual(inversions[3], 
                            dominant_seventh_chord_no_fifth_first_inversion,)
        self.assertEqual(inversions[4], 
                            dominant_seventh_chord_second_inversion,)
        self.assertEqual(inversions[5], 
                            dominant_seventh_chord_third_inversion,)
        self.assertEqual(inversions[6], 
                            dominant_seventh_chord_no_fifth_third_inversion)