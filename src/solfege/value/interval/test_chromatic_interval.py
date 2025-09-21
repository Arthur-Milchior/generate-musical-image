import unittest
from solfege.value.interval.alteration.alteration import Alteration
from solfege.value.interval.interval import Interval
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.chromatic_interval import *

class TestChromaticInterval(unittest.TestCase):
    unison = ChromaticInterval.make(0)
    second_minor = ChromaticInterval.make(1)
    second_minor_descending = ChromaticInterval.make(-1)
    second_major = ChromaticInterval.make(2)
    third_minor = ChromaticInterval.make(3)
    sept = ChromaticInterval.make(7)
    six = ChromaticInterval.make(6)
    seventh = ChromaticInterval.make(11)
    octave = ChromaticInterval.make(12)
    fourth_augmented_descending = ChromaticInterval.make(-6)
    fourth_descending = ChromaticInterval.make(-7)
    fifth_augmented_descending = ChromaticInterval.make(-8)
    seventh_descending = ChromaticInterval.make(-11)
    octave_descending = ChromaticInterval.make(-12)
    eighth_descending = ChromaticInterval.make(-13)

    def setUp(self):
        super().setUp()
        from solfege.value.interval.diatonic_interval import DiatonicInterval
        from solfege.value.interval.interval import Interval
        ChromaticInterval.DiatonicClass = DiatonicInterval
        ChromaticInterval.PairClass = Interval
        ChromaticInterval.AlterationClass = Alteration

    def test_classes(self):
        self.assertEqual(ChromaticInterval.IntervalClass, ChromaticInterval)
        self.assertEqual(ChromaticInterval.ChromaticClass, ChromaticInterval)
        self.assertEqual(ChromaticInterval.make_instance_of_selfs_class(0), ChromaticInterval.make(0))
        self.assertEqual(ChromaticInterval.PairClass, Interval)
        self.assertEqual(ChromaticInterval.DiatonicClass, DiatonicInterval)

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())

    def test_get_number(self):
        self.assertEqual(self.unison.value, 0)

    def test_equal(self):
        self.assertEqual(self.unison, self.unison)
        self.assertNotEqual(self.second_minor, self.unison)
        self.assertEqual(self.second_minor, self.second_minor)

    def test_add(self):
        self.assertEqual(self.second_minor + self.second_major, self.third_minor)

    def test_neg(self):
        self.assertEqual(-self.second_minor, self.second_minor_descending)

    def test_sub(self):
        self.assertEqual(self.third_minor - self.second_major, self.second_minor)

    def test_lt(self):
        self.assertLess(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_minor, self.second_minor)

    # def test_repr(self):
    #     self.assertEqual(repr(self.second_minor), "ChromaticInterval.make(value=1)")

    def test_octave(self):
        self.assertEqual(self.unison.octave(), 0)
        self.assertEqual(self.six.octave(), 0)
        self.assertEqual(self.seventh_descending.octave(), -1)
        self.assertEqual(self.octave_descending.octave(), -1)
        self.assertEqual(self.eighth_descending.octave(), -2)
        self.assertEqual(self.octave.octave(), 1)

    def test_add_octave(self):
        self.assertEqual(self.octave.add_octave(-1), self.unison)
        self.assertEqual(self.unison.add_octave(1), self.octave)
        self.assertEqual(self.octave.add_octave(-2), self.octave_descending)
        self.assertEqual(self.octave_descending.add_octave(2), self.octave)

    def test_same_interval_in_base_octave(self):
        self.assertEqual(self.octave.in_base_octave(), self.unison)
        self.assertEqual(self.octave_descending.in_base_octave(), self.unison)
        self.assertEqual(self.unison.in_base_octave(), self.unison)
        self.assertEqual(self.second_minor.in_base_octave(), self.second_minor)
        self.assertEqual(self.second_minor_descending.in_base_octave(), self.seventh)

    def test_same_interval_in_different_octave(self):
        self.assertFalse(self.second_minor.equals_modulo_octave(self.unison))
        self.assertFalse(self.second_minor.equals_modulo_octave(self.octave))
        self.assertFalse(self.second_minor.equals_modulo_octave(self.octave_descending))
        self.assertFalse(self.second_minor.equals_modulo_octave(self.second_minor_descending))
        self.assertTrue(self.unison.equals_modulo_octave(self.unison))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave_descending))
        self.assertTrue(self.octave.equals_modulo_octave(self.octave_descending))

    # def test_get_diatonic(self):
    #     self.assertEqual(ChromaticInterval.make(0).get_diatonic(), DiatonicInterval.make(0))
    #     self.assertEqual(ChromaticInterval.make(1).get_diatonic(), DiatonicInterval.make(0))
    #     self.assertEqual(ChromaticInterval.make(2).get_diatonic(), DiatonicInterval.make(1))
    #     self.assertEqual(ChromaticInterval.make(3).get_diatonic(), DiatonicInterval.make(2))
    #     self.assertEqual(ChromaticInterval.make(4).get_diatonic(), DiatonicInterval.make(2))
    #     self.assertEqual(ChromaticInterval.make(5).get_diatonic(), DiatonicInterval.make(3))
    #     self.assertEqual(ChromaticInterval.make(6).get_diatonic(), DiatonicInterval.make(3))
    #     self.assertEqual(ChromaticInterval.make(7).get_diatonic(), DiatonicInterval.make(4))
    #     self.assertEqual(ChromaticInterval.make(8).get_diatonic(), DiatonicInterval.make(5))
    #     self.assertEqual(ChromaticInterval.make(9).get_diatonic(), DiatonicInterval.make(5))
    #     self.assertEqual(ChromaticInterval.make(10).get_diatonic(), DiatonicInterval.make(6))
    #     self.assertEqual(ChromaticInterval.make(11).get_diatonic(), DiatonicInterval.make(6))
    #     self.assertEqual(ChromaticInterval.make(12).get_diatonic(), DiatonicInterval.make(7))
    #     self.assertEqual(ChromaticInterval.make(13).get_diatonic(), DiatonicInterval.make(7))
    #     self.assertEqual(ChromaticInterval.make(14).get_diatonic(), DiatonicInterval.make(8))
    #     self.assertEqual(ChromaticInterval.make(-1).get_diatonic(), DiatonicInterval.make(-1))
    #     self.assertEqual(ChromaticInterval.make(-2).get_diatonic(), DiatonicInterval.make(-1))
    #     self.assertEqual(ChromaticInterval.make(-3).get_diatonic(), DiatonicInterval.make(-2))
    #     self.assertEqual(ChromaticInterval.make(-4).get_diatonic(), DiatonicInterval.make(-2))
    #     self.assertEqual(ChromaticInterval.make(-5).get_diatonic(), DiatonicInterval.make(-3))
    #     self.assertEqual(ChromaticInterval.make(-6).get_diatonic(), DiatonicInterval.make(-4))
    #     self.assertEqual(ChromaticInterval.make(-7).get_diatonic(), DiatonicInterval.make(-4))
    #     self.assertEqual(ChromaticInterval.make(-8).get_diatonic(), DiatonicInterval.make(-5))
    #     self.assertEqual(ChromaticInterval.make(-9).get_diatonic(), DiatonicInterval.make(-5))
    #     self.assertEqual(ChromaticInterval.make(-10).get_diatonic(), DiatonicInterval.make(-6))
    #     self.assertEqual(ChromaticInterval.make(-11).get_diatonic(), DiatonicInterval.make(-7))
    #     self.assertEqual(ChromaticInterval.make(-12).get_diatonic(), DiatonicInterval.make(-7))
    #     self.assertEqual(ChromaticInterval.make(-13).get_diatonic(), DiatonicInterval.make(-8))
    #     self.assertEqual(ChromaticInterval.make(-14).get_diatonic(), DiatonicInterval.make(-8))

    # def test_get_pair(self):
    #     self.assertEqual(ChromaticInterval.make(0).get_pair(), Interval.make(0, 0))
    #     self.assertEqual(ChromaticInterval.make(1).get_pair(), Interval.make(1, 0))
    #     self.assertEqual(ChromaticInterval.make(2).get_pair(), Interval.make(2, 1))
    #     self.assertEqual(ChromaticInterval.make(3).get_pair(), Interval.make(3, 2))
    #     self.assertEqual(ChromaticInterval.make(4).get_pair(), Interval.make(4, 2))
    #     self.assertEqual(ChromaticInterval.make(5).get_pair(), Interval.make(5, 3))
    #     self.assertEqual(ChromaticInterval.make(6).get_pair(), Interval.make(6, 3))
    #     self.assertEqual(ChromaticInterval.make(7).get_pair(), Interval.make(7, 4))
    #     self.assertEqual(ChromaticInterval.make(8).get_pair(), Interval.make(8, 5))
    #     self.assertEqual(ChromaticInterval.make(9).get_pair(), Interval.make(9, 5))
    #     self.assertEqual(ChromaticInterval.make(10).get_pair(), Interval.make(10, 6))
    #     self.assertEqual(ChromaticInterval.make(11).get_pair(), Interval.make(11, 6))
    #     self.assertEqual(ChromaticInterval.make(12).get_pair(), Interval.make(12, 7))
    #     self.assertEqual(ChromaticInterval.make(13).get_pair(), Interval.make(13, 7))
    #     self.assertEqual(ChromaticInterval.make(14).get_pair(), Interval.make(14, 8))
    #     self.assertEqual(ChromaticInterval.make(-1).get_pair(), Interval.make(-1, -1))
    #     self.assertEqual(ChromaticInterval.make(-2).get_pair(), Interval.make(-2, -1))
    #     self.assertEqual(ChromaticInterval.make(-3).get_pair(), Interval.make(-3, -2))
    #     self.assertEqual(ChromaticInterval.make(-4).get_pair(), Interval.make(-4, -2))
    #     self.assertEqual(ChromaticInterval.make(-5).get_pair(), Interval.make(-5, -3))
    #     self.assertEqual(ChromaticInterval.make(-6).get_pair(), Interval.make(-6, -4))
    #     self.assertEqual(ChromaticInterval.make(-7).get_pair(), Interval.make(-7, -4))
    #     self.assertEqual(ChromaticInterval.make(-8).get_pair(), Interval.make(-8, -5))
    #     self.assertEqual(ChromaticInterval.make(-9).get_pair(), Interval.make(-9, -5))
    #     self.assertEqual(ChromaticInterval.make(-10).get_pair(), Interval.make(-10, -6))
    #     self.assertEqual(ChromaticInterval.make(-11).get_pair(), Interval.make(-11, -7))
    #     self.assertEqual(ChromaticInterval.make(-12).get_pair(), Interval.make(-12, -7))
    #     self.assertEqual(ChromaticInterval.make(-13).get_pair(), Interval.make(-13, -8))
    #     self.assertEqual(ChromaticInterval.make(-14).get_pair(), Interval.make(-14, -8))

    # def test_get_alteration(self):
    #     self.assertEqual(ChromaticInterval.make(0).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(1).get_alteration(), IntervalMode(1))
    #     self.assertEqual(ChromaticInterval.make(2).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(3).get_alteration(), IntervalMode(-1))
    #     self.assertEqual(ChromaticInterval.make(4).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(5).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(6).get_alteration(), IntervalMode(1))
    #     self.assertEqual(ChromaticInterval.make(7).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(8).get_alteration(), IntervalMode(-1))
    #     self.assertEqual(ChromaticInterval.make(9).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(10).get_alteration(), IntervalMode(-1))
    #     self.assertEqual(ChromaticInterval.make(11).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(12).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(13).get_alteration(), IntervalMode(1))
    #     self.assertEqual(ChromaticInterval.make(14).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-1).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-2).get_alteration(), IntervalMode(-1))
    #     self.assertEqual(ChromaticInterval.make(-3).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-4).get_alteration(), IntervalMode(-1))
    #     self.assertEqual(ChromaticInterval.make(-5).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-6).get_alteration(), IntervalMode(1))
    #     self.assertEqual(ChromaticInterval.make(-7).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-8).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-9).get_alteration(), IntervalMode(-1))
    #     self.assertEqual(ChromaticInterval.make(-10).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-11).get_alteration(), IntervalMode(1))
    #     self.assertEqual(ChromaticInterval.make(-12).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-13).get_alteration(), IntervalMode(0))
    #     self.assertEqual(ChromaticInterval.make(-14).get_alteration(), IntervalMode(-1))

    def test_get_interval_name_octave_NEVER_side(self):
        self.assertEqual(ChromaticInterval.make(0).get_interval_name(), "unison")
        self.assertEqual(ChromaticInterval.make(1).get_interval_name(), "second minor")
        self.assertEqual(ChromaticInterval.make(2).get_interval_name(), "second major")
        self.assertEqual(ChromaticInterval.make(3).get_interval_name(), "third minor")
        self.assertEqual(ChromaticInterval.make(4).get_interval_name(), "third major")
        self.assertEqual(ChromaticInterval.make(5).get_interval_name(), "fourth")
        self.assertEqual(ChromaticInterval.make(6).get_interval_name(), "tritone")
        self.assertEqual(ChromaticInterval.make(7).get_interval_name(), "fifth")
        self.assertEqual(ChromaticInterval.make(8).get_interval_name(), "sixth minor")
        self.assertEqual(ChromaticInterval.make(9).get_interval_name(), "sixth major")
        self.assertEqual(ChromaticInterval.make(10).get_interval_name(), "seventh minor")
        self.assertEqual(ChromaticInterval.make(11).get_interval_name(), "seventh major")
        self.assertEqual(ChromaticInterval.make(12).get_interval_name(), "octave")
        self.assertEqual(ChromaticInterval.make(13).get_interval_name(), "octave and second minor")
        self.assertEqual(ChromaticInterval.make(24).get_interval_name(), "2 octaves")
        self.assertEqual(ChromaticInterval.make(25).get_interval_name(), "2 octaves and second minor")
        self.assertEqual(ChromaticInterval.make(-1).get_interval_name(), "second minor")
        self.assertEqual(ChromaticInterval.make(-12).get_interval_name(), "octave")
        self.assertEqual(ChromaticInterval.make(-13).get_interval_name(), "octave and second minor")
        self.assertEqual(ChromaticInterval.make(-24).get_interval_name(), "2 octaves")
        self.assertEqual(ChromaticInterval.make(-25).get_interval_name(), "2 octaves and second minor")

    def test_get_interval_name_octave_ALWAYS_side(self):
        self.assertEqual(ChromaticInterval.make(0).get_interval_name(side=IntervalNameCreasing.ALWAYS), "unison")
        self.assertEqual(ChromaticInterval.make(1).get_interval_name(side=IntervalNameCreasing.ALWAYS), "second minor increasing")
        self.assertEqual(ChromaticInterval.make(2).get_interval_name(side=IntervalNameCreasing.ALWAYS), "second major increasing")
        self.assertEqual(ChromaticInterval.make(3).get_interval_name(side=IntervalNameCreasing.ALWAYS), "third minor increasing")
        self.assertEqual(ChromaticInterval.make(4).get_interval_name(side=IntervalNameCreasing.ALWAYS), "third major increasing")
        self.assertEqual(ChromaticInterval.make(5).get_interval_name(side=IntervalNameCreasing.ALWAYS), "fourth increasing")
        self.assertEqual(ChromaticInterval.make(6).get_interval_name(side=IntervalNameCreasing.ALWAYS), "tritone increasing")
        self.assertEqual(ChromaticInterval.make(7).get_interval_name(side=IntervalNameCreasing.ALWAYS), "fifth increasing")
        self.assertEqual(ChromaticInterval.make(8).get_interval_name(side=IntervalNameCreasing.ALWAYS), "sixth minor increasing")
        self.assertEqual(ChromaticInterval.make(9).get_interval_name(side=IntervalNameCreasing.ALWAYS), "sixth major increasing")
        self.assertEqual(ChromaticInterval.make(10).get_interval_name(side=IntervalNameCreasing.ALWAYS), "seventh minor increasing")
        self.assertEqual(ChromaticInterval.make(11).get_interval_name(side=IntervalNameCreasing.ALWAYS), "seventh major increasing")
        self.assertEqual(ChromaticInterval.make(12).get_interval_name(side=IntervalNameCreasing.ALWAYS), "octave increasing")
        self.assertEqual(ChromaticInterval.make(13).get_interval_name(side=IntervalNameCreasing.ALWAYS), "octave and second minor increasing")
        self.assertEqual(ChromaticInterval.make(24).get_interval_name(side=IntervalNameCreasing.ALWAYS), "2 octaves increasing")
        self.assertEqual(ChromaticInterval.make(25).get_interval_name(side=IntervalNameCreasing.ALWAYS), "2 octaves and second minor increasing")
        self.assertEqual(ChromaticInterval.make(-1).get_interval_name(side=IntervalNameCreasing.ALWAYS), "second minor decreasing")
        self.assertEqual(ChromaticInterval.make(-12).get_interval_name(side=IntervalNameCreasing.ALWAYS), "octave decreasing")
        self.assertEqual(ChromaticInterval.make(-13).get_interval_name(side=IntervalNameCreasing.ALWAYS), "octave and second minor decreasing")
        self.assertEqual(ChromaticInterval.make(-24).get_interval_name(side=IntervalNameCreasing.ALWAYS), "2 octaves decreasing")
        self.assertEqual(ChromaticInterval.make(-25).get_interval_name(side=IntervalNameCreasing.ALWAYS), "2 octaves and second minor decreasing")

    def test_get_interval_name_octave_DECREASING_side(self):
        self.assertEqual(ChromaticInterval.make(0).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "unison")
        self.assertEqual(ChromaticInterval.make(1).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "second minor")
        self.assertEqual(ChromaticInterval.make(2).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "second major")
        self.assertEqual(ChromaticInterval.make(3).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "third minor")
        self.assertEqual(ChromaticInterval.make(4).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "third major")
        self.assertEqual(ChromaticInterval.make(5).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "fourth")
        self.assertEqual(ChromaticInterval.make(6).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "tritone")
        self.assertEqual(ChromaticInterval.make(7).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "fifth")
        self.assertEqual(ChromaticInterval.make(8).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "sixth minor")
        self.assertEqual(ChromaticInterval.make(9).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "sixth major")
        self.assertEqual(ChromaticInterval.make(10).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "seventh minor")
        self.assertEqual(ChromaticInterval.make(11).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "seventh major")
        self.assertEqual(ChromaticInterval.make(12).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "octave")
        self.assertEqual(ChromaticInterval.make(13).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "octave and second minor")
        self.assertEqual(ChromaticInterval.make(24).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "2 octaves")
        self.assertEqual(ChromaticInterval.make(25).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "2 octaves and second minor")
        self.assertEqual(ChromaticInterval.make(-1).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "second minor decreasing")
        self.assertEqual(ChromaticInterval.make(-12).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "octave decreasing")
        self.assertEqual(ChromaticInterval.make(-13).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "octave and second minor decreasing")
        self.assertEqual(ChromaticInterval.make(-24).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "2 octaves decreasing")
        self.assertEqual(ChromaticInterval.make(-25).get_interval_name(side=IntervalNameCreasing.DECREASING_ONLY), "2 octaves and second minor decreasing")

    def test_mul(self):
        self.assertEqual(self.unison * 4, self.unison)
        self.assertEqual(self.second_minor * 2, self.second_major)
        # self.assertEqual(2 * self.second_minor, self.second_major)
        # self.assertEqual(4 * self.unison, self.unison)

    def test_one_octave(self):
        self.assertEqual(ChromaticInterval.one_octave(), ChromaticInterval.make(value=12))
