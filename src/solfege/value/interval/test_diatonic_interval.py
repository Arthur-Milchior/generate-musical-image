import unittest
from solfege.value.interval.diatonic_interval import *

class TestDiatonicInterval(unittest.TestCase):
    unison = DiatonicInterval(0)
    second = DiatonicInterval(1)
    second_descending = DiatonicInterval(-1)
    third = DiatonicInterval(2)
    fourth = DiatonicInterval(3)
    octave = DiatonicInterval(7)
    seventh = DiatonicInterval(6)
    seventh_descending = DiatonicInterval(-6)
    octave_descending = DiatonicInterval(-7)
    second_twice_descending = DiatonicInterval(-8)

    def setUp(self):
        super().setUp()
        from solfege.value.interval.chromatic_interval import ChromaticInterval
        DiatonicInterval.ChromaticClass = ChromaticInterval

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())
        
    def test_get_number(self):
        self.assertEqual(self.unison.value, 0)

    def test_equal(self):
        self.assertEqual(self.unison, self.unison)
        self.assertNotEqual(self.second, self.unison)
        self.assertEqual(self.second, self.second)

    def test_add(self):
        self.assertEqual(self.second + self.third, self.fourth)

    def test_neg(self):
        self.assertEqual(-self.second, self.second_descending)

    def test_sub(self):
        self.assertEqual(self.fourth - self.third, self.second)

    def test_lt(self):
        self.assertLess(self.second, self.third)
        self.assertLessEqual(self.second, self.third)
        self.assertLessEqual(self.second, self.second)

    def test_repr(self):
        self.assertEqual(repr(self.second), "DiatonicInterval(value=1)")

    def test_octave(self):
        self.assertEqual(self.unison.octave(), 0)
        self.assertEqual(self.seventh.octave(), 0)
        self.assertEqual(self.seventh_descending.octave(), -1)
        self.assertEqual(self.octave_descending.octave(), -1)
        self.assertEqual(self.second_twice_descending.octave(), -2)
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
        self.assertEqual(self.second.in_base_octave(), self.second)
        self.assertEqual(self.second_descending.in_base_octave(), self.seventh)

    def test_same_interval_in_different_octaves(self):
        self.assertFalse(self.second.equals_modulo_octave(self.unison))
        self.assertFalse(self.second.equals_modulo_octave(self.octave))
        self.assertFalse(self.second.equals_modulo_octave(self.octave_descending))
        self.assertFalse(self.second.equals_modulo_octave(self.second_descending))
        self.assertTrue(self.unison.equals_modulo_octave(self.unison))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave_descending))
        self.assertTrue(self.octave.equals_modulo_octave(self.octave_descending))

    # def test_get_chromatic(self):
    #     from solfege.value.interval.chromatic_interval import ChromaticInterval
    #     self.assertEqual(DiatonicInterval(0).get_chromatic(), ChromaticInterval(0))
    #     self.assertEqual(DiatonicInterval(1).get_chromatic(), ChromaticInterval(2))
    #     self.assertEqual(DiatonicInterval(2).get_chromatic(), ChromaticInterval(4))
    #     self.assertEqual(DiatonicInterval(3).get_chromatic(), ChromaticInterval(5))
    #     self.assertEqual(DiatonicInterval(4).get_chromatic(), ChromaticInterval(7))
    #     self.assertEqual(DiatonicInterval(5).get_chromatic(), ChromaticInterval(9))
    #     self.assertEqual(DiatonicInterval(6).get_chromatic(), ChromaticInterval(11))
    #     self.assertEqual(DiatonicInterval(7).get_chromatic(), ChromaticInterval(12))
    #     self.assertEqual(DiatonicInterval(8).get_chromatic(), ChromaticInterval(14))
    #     self.assertEqual(DiatonicInterval(9).get_chromatic(), ChromaticInterval(16))
    #     self.assertEqual(DiatonicInterval(-1).get_chromatic(), ChromaticInterval(-1))
    #     self.assertEqual(DiatonicInterval(-2).get_chromatic(), ChromaticInterval(-3))
    #     self.assertEqual(DiatonicInterval(-3).get_chromatic(), ChromaticInterval(-5))
    #     self.assertEqual(DiatonicInterval(-4).get_chromatic(), ChromaticInterval(-7))
    #     self.assertEqual(DiatonicInterval(-5).get_chromatic(), ChromaticInterval(-8))
    #     self.assertEqual(DiatonicInterval(-6).get_chromatic(), ChromaticInterval(-10))
    #     self.assertEqual(DiatonicInterval(-7).get_chromatic(), ChromaticInterval(-12))
    #     self.assertEqual(DiatonicInterval(-8).get_chromatic(), ChromaticInterval(-13))
    #     self.assertEqual(DiatonicInterval(-9).get_chromatic(), ChromaticInterval(-15))

    def test_get_name_no_octave(self):
        self.assertEqual(DiatonicInterval(0).get_interval_name(showOctave=False), "unison")
        self.assertEqual(DiatonicInterval(1).get_interval_name(showOctave=False), "second")
        self.assertEqual(DiatonicInterval(2).get_interval_name(showOctave=False), "third")
        self.assertEqual(DiatonicInterval(3).get_interval_name(showOctave=False), "fourth")
        self.assertEqual(DiatonicInterval(4).get_interval_name(showOctave=False), "fifth")
        self.assertEqual(DiatonicInterval(5).get_interval_name(showOctave=False), "sixth")
        self.assertEqual(DiatonicInterval(6).get_interval_name(showOctave=False), "seventh")
        self.assertEqual(DiatonicInterval(7).get_interval_name(showOctave=False), "unison")
        self.assertEqual(DiatonicInterval(8).get_interval_name(showOctave=False), "second")
        self.assertEqual(DiatonicInterval(9).get_interval_name(showOctave=False), "third")
        self.assertEqual(DiatonicInterval(-1).get_interval_name(showOctave=False), "second decreasing")
        self.assertEqual(DiatonicInterval(-2).get_interval_name(showOctave=False), "third decreasing")
        self.assertEqual(DiatonicInterval(-3).get_interval_name(showOctave=False), "fourth decreasing")
        self.assertEqual(DiatonicInterval(-4).get_interval_name(showOctave=False), "fifth decreasing")
        self.assertEqual(DiatonicInterval(-5).get_interval_name(showOctave=False), "sixth decreasing")
        self.assertEqual(DiatonicInterval(-6).get_interval_name(showOctave=False), "seventh decreasing")
        self.assertEqual(DiatonicInterval(-7).get_interval_name(showOctave=False), "unison decreasing")
        self.assertEqual(DiatonicInterval(-8).get_interval_name(showOctave=False), "second decreasing")
        self.assertEqual(DiatonicInterval(-9).get_interval_name(showOctave=False), "third decreasing")

    def test_get_name_with_octave(self):
        self.assertEqual(DiatonicInterval(0).get_interval_name(showOctave=True), "unison")
        self.assertEqual(DiatonicInterval(1).get_interval_name(showOctave=True), "second")
        self.assertEqual(DiatonicInterval(2).get_interval_name(showOctave=True), "third")
        self.assertEqual(DiatonicInterval(3).get_interval_name(showOctave=True), "fourth")
        self.assertEqual(DiatonicInterval(4).get_interval_name(showOctave=True), "fifth")
        self.assertEqual(DiatonicInterval(5).get_interval_name(showOctave=True), "sixth")
        self.assertEqual(DiatonicInterval(6).get_interval_name(showOctave=True), "seventh")
        self.assertEqual(DiatonicInterval(7).get_interval_name(showOctave=True), "octave")
        self.assertEqual(DiatonicInterval(8).get_interval_name(showOctave=True), "octave and second")
        self.assertEqual(DiatonicInterval(9).get_interval_name(showOctave=True), "octave and third")
        self.assertEqual(DiatonicInterval(10).get_interval_name(showOctave=True), "octave and fourth")
        self.assertEqual(DiatonicInterval(11).get_interval_name(showOctave=True), "octave and fifth")
        self.assertEqual(DiatonicInterval(12).get_interval_name(showOctave=True), "octave and sixth")
        self.assertEqual(DiatonicInterval(13).get_interval_name(showOctave=True), "octave and seventh")
        self.assertEqual(DiatonicInterval(14).get_interval_name(showOctave=True), "2 octaves")
        self.assertEqual(DiatonicInterval(15).get_interval_name(showOctave=True), "2 octaves and second")
        self.assertEqual(DiatonicInterval(16).get_interval_name(showOctave=True), "2 octaves and third")
        self.assertEqual(DiatonicInterval(-1).get_interval_name(showOctave=True), "second decreasing")
        self.assertEqual(DiatonicInterval(-2).get_interval_name(showOctave=True), "third decreasing")
        self.assertEqual(DiatonicInterval(-3).get_interval_name(showOctave=True), "fourth decreasing")
        self.assertEqual(DiatonicInterval(-4).get_interval_name(showOctave=True), "fifth decreasing")
        self.assertEqual(DiatonicInterval(-5).get_interval_name(showOctave=True), "sixth decreasing")
        self.assertEqual(DiatonicInterval(-6).get_interval_name(showOctave=True), "seventh decreasing")
        self.assertEqual(DiatonicInterval(-7).get_interval_name(showOctave=True), "octave decreasing")
        self.assertEqual(DiatonicInterval(-8).get_interval_name(showOctave=True), "octave and second decreasing")
        self.assertEqual(DiatonicInterval(-9).get_interval_name(showOctave=True), "octave and third decreasing")
        self.assertEqual(DiatonicInterval(-10).get_interval_name(showOctave=True), "octave and fourth decreasing")
        self.assertEqual(DiatonicInterval(-11).get_interval_name(showOctave=True), "octave and fifth decreasing")
        self.assertEqual(DiatonicInterval(-12).get_interval_name(showOctave=True), "octave and sixth decreasing")
        self.assertEqual(DiatonicInterval(-13).get_interval_name(showOctave=True), "octave and seventh decreasing")
        self.assertEqual(DiatonicInterval(-14).get_interval_name(showOctave=True), "2 octaves decreasing")
        self.assertEqual(DiatonicInterval(-15).get_interval_name(showOctave=True), "2 octaves and second decreasing")
        self.assertEqual(DiatonicInterval(-16).get_interval_name(showOctave=True), "2 octaves and third decreasing")

    def test_mul(self):
        self.assertEqual(self.unison * 4, self.unison)
        self.assertEqual(self.second * 2, self.third)
        # self.assertEqual(2 * self.second, self.third)
        # self.assertEqual(4 * self.unison, self.unison)

    def test_one_octave(self):
        self.assertEqual(DiatonicInterval.one_octave(), DiatonicInterval(value=7))
