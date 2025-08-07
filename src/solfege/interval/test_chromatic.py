from .chromatic import *

class TestChromaticInterval(unittest.TestCase):
    unison = ChromaticInterval(0)
    second_minor = ChromaticInterval(1)
    second_minor_descending = ChromaticInterval(-1)
    second_major = ChromaticInterval(2)
    third_minor = ChromaticInterval(3)
    sept = ChromaticInterval(7)
    six = ChromaticInterval(6)
    seventh = ChromaticInterval(11)
    octave = ChromaticInterval(12)
    fourth_augmented_descending = ChromaticInterval(-6)
    fourth_descending = ChromaticInterval(-7)
    fifth_augmented_descending = ChromaticInterval(-8)
    seventh_descending = ChromaticInterval(-11)
    octave_descending = ChromaticInterval(-12)
    eighth_descending = ChromaticInterval(-13)

    def setUp(self):
        super().setUp()
        from solfege.interval.diatonic import DiatonicInterval
        from solfege.interval.interval import Interval
        from solfege.interval.intervalmode import IntervalMode
        ChromaticInterval.RelatedDiatonicClass = DiatonicInterval
        ChromaticInterval.RelatedSolfegeClass = Interval
        ChromaticInterval.AlterationClass = IntervalMode

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())

    def test_has_number(self):
        self.assertTrue(self.unison.has_number())

    def test_get_number(self):
        self.assertEquals(self.unison.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.unison, self.unison)
        self.assertNotEquals(self.second_minor, self.unison)
        self.assertEquals(self.second_minor, self.second_minor)

    def test_add(self):
        self.assertEquals(self.second_minor + self.second_major, self.third_minor)

    def test_neg(self):
        self.assertEquals(-self.second_minor, self.second_minor_descending)

    def test_sub(self):
        self.assertEquals(self.third_minor - self.second_major, self.second_minor)

    def test_lt(self):
        self.assertLess(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_minor, self.second_minor)

    def test_repr(self):
        self.assertEquals(repr(self.second_minor), "ChromaticInterval(value=1)")

    def test_get_octave(self):
        self.assertEquals(self.unison.get_octave(), 0)
        self.assertEquals(self.six.get_octave(), 0)
        self.assertEquals(self.seventh_descending.get_octave(), -1)
        self.assertEquals(self.octave_descending.get_octave(), -1)
        self.assertEquals(self.eighth_descending.get_octave(), -2)
        self.assertEquals(self.octave.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(self.octave.add_octave(-1), self.unison)
        self.assertEquals(self.unison.add_octave(1), self.octave)
        self.assertEquals(self.octave.add_octave(-2), self.octave_descending)
        self.assertEquals(self.octave_descending.add_octave(2), self.octave)

    def test_same_interval_in_base_octave(self):
        self.assertEquals(self.octave.get_in_base_octave(), self.unison)
        self.assertEquals(self.octave_descending.get_in_base_octave(), self.unison)
        self.assertEquals(self.unison.get_in_base_octave(), self.unison)
        self.assertEquals(self.second_minor.get_in_base_octave(), self.second_minor)
        self.assertEquals(self.second_minor_descending.get_in_base_octave(), self.seventh)

    def test_same_interval_in_different_octave(self):
        self.assertFalse(self.second_minor.equals_modulo_octave(self.unison))
        self.assertFalse(self.second_minor.equals_modulo_octave(self.octave))
        self.assertFalse(self.second_minor.equals_modulo_octave(self.octave_descending))
        self.assertFalse(self.second_minor.equals_modulo_octave(self.second_minor_descending))
        self.assertTrue(self.unison.equals_modulo_octave(self.unison))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave_descending))
        self.assertTrue(self.octave.equals_modulo_octave(self.octave_descending))

    def test_get_diatonic(self):
        from solfege.interval.diatonic import DiatonicInterval
        self.assertEquals(ChromaticInterval(0).get_diatonic(), DiatonicInterval(0))
        self.assertEquals(ChromaticInterval(1).get_diatonic(), DiatonicInterval(0))
        self.assertEquals(ChromaticInterval(2).get_diatonic(), DiatonicInterval(1))
        self.assertEquals(ChromaticInterval(3).get_diatonic(), DiatonicInterval(2))
        self.assertEquals(ChromaticInterval(4).get_diatonic(), DiatonicInterval(2))
        self.assertEquals(ChromaticInterval(5).get_diatonic(), DiatonicInterval(3))
        self.assertEquals(ChromaticInterval(6).get_diatonic(), DiatonicInterval(3))
        self.assertEquals(ChromaticInterval(7).get_diatonic(), DiatonicInterval(4))
        self.assertEquals(ChromaticInterval(8).get_diatonic(), DiatonicInterval(5))
        self.assertEquals(ChromaticInterval(9).get_diatonic(), DiatonicInterval(5))
        self.assertEquals(ChromaticInterval(10).get_diatonic(), DiatonicInterval(6))
        self.assertEquals(ChromaticInterval(11).get_diatonic(), DiatonicInterval(6))
        self.assertEquals(ChromaticInterval(12).get_diatonic(), DiatonicInterval(7))
        self.assertEquals(ChromaticInterval(13).get_diatonic(), DiatonicInterval(7))
        self.assertEquals(ChromaticInterval(14).get_diatonic(), DiatonicInterval(8))
        self.assertEquals(ChromaticInterval(-1).get_diatonic(), DiatonicInterval(-1))
        self.assertEquals(ChromaticInterval(-2).get_diatonic(), DiatonicInterval(-1))
        self.assertEquals(ChromaticInterval(-3).get_diatonic(), DiatonicInterval(-2))
        self.assertEquals(ChromaticInterval(-4).get_diatonic(), DiatonicInterval(-2))
        self.assertEquals(ChromaticInterval(-5).get_diatonic(), DiatonicInterval(-3))
        self.assertEquals(ChromaticInterval(-6).get_diatonic(), DiatonicInterval(-4))
        self.assertEquals(ChromaticInterval(-7).get_diatonic(), DiatonicInterval(-4))
        self.assertEquals(ChromaticInterval(-8).get_diatonic(), DiatonicInterval(-5))
        self.assertEquals(ChromaticInterval(-9).get_diatonic(), DiatonicInterval(-5))
        self.assertEquals(ChromaticInterval(-10).get_diatonic(), DiatonicInterval(-6))
        self.assertEquals(ChromaticInterval(-11).get_diatonic(), DiatonicInterval(-7))
        self.assertEquals(ChromaticInterval(-12).get_diatonic(), DiatonicInterval(-7))
        self.assertEquals(ChromaticInterval(-13).get_diatonic(), DiatonicInterval(-8))
        self.assertEquals(ChromaticInterval(-14).get_diatonic(), DiatonicInterval(-8))

    def test_get_solfege(self):
        from solfege.interval.interval import Interval
        self.assertEquals(ChromaticInterval(0).get_solfege(), Interval(0, 0))
        self.assertEquals(ChromaticInterval(1).get_solfege(), Interval(1, 0))
        self.assertEquals(ChromaticInterval(2).get_solfege(), Interval(2, 1))
        self.assertEquals(ChromaticInterval(3).get_solfege(), Interval(3, 2))
        self.assertEquals(ChromaticInterval(4).get_solfege(), Interval(4, 2))
        self.assertEquals(ChromaticInterval(5).get_solfege(), Interval(5, 3))
        self.assertEquals(ChromaticInterval(6).get_solfege(), Interval(6, 3))
        self.assertEquals(ChromaticInterval(7).get_solfege(), Interval(7, 4))
        self.assertEquals(ChromaticInterval(8).get_solfege(), Interval(8, 5))
        self.assertEquals(ChromaticInterval(9).get_solfege(), Interval(9, 5))
        self.assertEquals(ChromaticInterval(10).get_solfege(), Interval(10, 6))
        self.assertEquals(ChromaticInterval(11).get_solfege(), Interval(11, 6))
        self.assertEquals(ChromaticInterval(12).get_solfege(), Interval(12, 7))
        self.assertEquals(ChromaticInterval(13).get_solfege(), Interval(13, 7))
        self.assertEquals(ChromaticInterval(14).get_solfege(), Interval(14, 8))
        self.assertEquals(ChromaticInterval(-1).get_solfege(), Interval(-1, -1))
        self.assertEquals(ChromaticInterval(-2).get_solfege(), Interval(-2, -1))
        self.assertEquals(ChromaticInterval(-3).get_solfege(), Interval(-3, -2))
        self.assertEquals(ChromaticInterval(-4).get_solfege(), Interval(-4, -2))
        self.assertEquals(ChromaticInterval(-5).get_solfege(), Interval(-5, -3))
        self.assertEquals(ChromaticInterval(-6).get_solfege(), Interval(-6, -4))
        self.assertEquals(ChromaticInterval(-7).get_solfege(), Interval(-7, -4))
        self.assertEquals(ChromaticInterval(-8).get_solfege(), Interval(-8, -5))
        self.assertEquals(ChromaticInterval(-9).get_solfege(), Interval(-9, -5))
        self.assertEquals(ChromaticInterval(-10).get_solfege(), Interval(-10, -6))
        self.assertEquals(ChromaticInterval(-11).get_solfege(), Interval(-11, -7))
        self.assertEquals(ChromaticInterval(-12).get_solfege(), Interval(-12, -7))
        self.assertEquals(ChromaticInterval(-13).get_solfege(), Interval(-13, -8))
        self.assertEquals(ChromaticInterval(-14).get_solfege(), Interval(-14, -8))

    def test_get_alteration(self):
        from solfege.interval.intervalmode import IntervalMode
        self.assertEquals(ChromaticInterval(0).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(1).get_alteration(), IntervalMode(1))
        self.assertEquals(ChromaticInterval(2).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(3).get_alteration(), IntervalMode(-1))
        self.assertEquals(ChromaticInterval(4).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(5).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(6).get_alteration(), IntervalMode(1))
        self.assertEquals(ChromaticInterval(7).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(8).get_alteration(), IntervalMode(-1))
        self.assertEquals(ChromaticInterval(9).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(10).get_alteration(), IntervalMode(-1))
        self.assertEquals(ChromaticInterval(11).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(12).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(13).get_alteration(), IntervalMode(1))
        self.assertEquals(ChromaticInterval(14).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-1).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-2).get_alteration(), IntervalMode(-1))
        self.assertEquals(ChromaticInterval(-3).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-4).get_alteration(), IntervalMode(-1))
        self.assertEquals(ChromaticInterval(-5).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-6).get_alteration(), IntervalMode(1))
        self.assertEquals(ChromaticInterval(-7).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-8).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-9).get_alteration(), IntervalMode(-1))
        self.assertEquals(ChromaticInterval(-10).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-11).get_alteration(), IntervalMode(1))
        self.assertEquals(ChromaticInterval(-12).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-13).get_alteration(), IntervalMode(0))
        self.assertEquals(ChromaticInterval(-14).get_alteration(), IntervalMode(-1))

    def test_mul(self):
        self.assertEquals(self.unison * 4, self.unison)
        self.assertEquals(self.second_minor * 2, self.second_major)
        self.assertEquals(2 * self.second_minor, self.second_major)
        self.assertEquals(4 * self.unison, self.unison)

    def test_one_octave(self):
        self.assertEquals(ChromaticInterval.get_one_octave(), ChromaticInterval(value=12))
