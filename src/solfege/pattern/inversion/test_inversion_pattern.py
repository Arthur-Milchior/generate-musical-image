import unittest

from solfege.pattern.chord.chord_pattern import *

from solfege.pattern.inversion.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
from solfege.value.key.key import *
from solfege.pattern.chord.test_constants import *

class TestInversionPattern(unittest.TestCase):
    def check_inversion_equal(self, inv1:InversionPattern, inv2:InversionPattern):
        assert_typing(inv1, InversionPattern)
        assert_typing(inv2, InversionPattern)
        self.assertEqual(inv1.base, inv2.base)
        self.assertEqual(inv1.fifth_omitted, inv2.fifth_omitted)
        self.assertEqual(inv1.interval_list, inv2.interval_list)
        self.assertEqual(inv1.inversion, inv2.inversion)

    def test_eq(self):
        """Checks that "record" is ignored for equality."""
        self.assertFalse(dominant_seventh_chord_zeroth_inversion.record)
        self.assertTrue(dominant_seventh_chord.inversions[0].record)
        self.assertEqual(dominant_seventh_chord_zeroth_inversion, dominant_seventh_chord.inversions[0])

    def test_il_found(self):
        il = IntervalListPattern.make_absolute([(4, 2), (7, 4), (10, 6)])
        iv = make_inversion(0, il, dominant_seventh_chord, (0,0))
        actual = interval_to_inversion.get_recorded_container(il)
        self.assertEqual([iv], actual)

    def test_il_no_fifth_found(self):
        il = IntervalListPattern.make_absolute([(4, 2), (10, 6)])
        actual = interval_to_inversion.get_recorded_container(il)
        self.assertEqual(len(actual), 1)
        self.check_inversion_equal(make_inversion(0, il, dominant_seventh_chord, (0, 0), fifth_omitted=True), actual[0])

    def test_il_chromatic_found(self):
        il = IntervalListPattern.make_absolute([(4, 2), (7, 4), (10, 6)])
        il_chromatic = ChromaticIntervalListPattern.make_absolute([4, 7, 10])
        expected = ChromaticIntervalListAndItsInversions(il_chromatic)
        expected.append(make_inversion(0, il, dominant_seventh_chord, (0, 0)))
        self.assertEqual(expected, interval_to_inversion.get_from_chromatic_interval_list(il_chromatic))

    def test_il_no_fifth_chromatic_found(self):
        il = IntervalListPattern.make_absolute([(4, 2), (10, 6)])
        il_chromatic = ChromaticIntervalListPattern.make_absolute([4, 10])
        expected = ChromaticIntervalListAndItsInversions(il_chromatic)
        expected.append(make_inversion(0, il, dominant_seventh_chord, (0, 0), fifth_omitted=True))
        self.assertEqual(expected, interval_to_inversion.get_from_chromatic_interval_list(il_chromatic))

    def test_inversion_found(self):
        for inversion in inversions:
            chromatic_interval_list = inversion.interval_list.get_chromatic_interval_list()
            expected = ChromaticIntervalListAndItsInversions(chromatic_interval_list)
            expected.append(inversion)
            self.assertEqual([inversion], interval_to_inversion.get_recorded_container(inversion.interval_list))
            self.assertEqual(expected, interval_to_inversion.get_from_chromatic_interval_list(chromatic_interval_list))
