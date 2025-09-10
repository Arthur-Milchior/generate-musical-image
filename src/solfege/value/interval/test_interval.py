import unittest
from solfege.value.interval.interval import *

class TestInterval(unittest.TestCase):

    def test_is_note(self):
        self.assertFalse(unison.is_note())

    def test_equal(self):
        self.assertEqual(unison, unison)
        self.assertNotEqual(second_major, unison)
        self.assertEqual(second_major, second_major)

    def test_add(self):
        self.assertEqual(second_major + second_minor, third_minor)
        # self.assertEqual(second_major + ChromaticInterval(1), ChromaticInterval(3))
        # self.assertEqual(ChromaticInterval(1) + second_major, ChromaticInterval(3))
        # self.assertEqual(second_major + DiatonicInterval(1), DiatonicInterval(2))
        # self.assertEqual(DiatonicInterval(1) + second_major, DiatonicInterval(2))

    def test_neg(self):
        self.assertEqual(-second_minor, minus_second_minor)

    def test_sub(self):
        self.assertEqual(third_minor - second_major, second_minor)

    def test_lt(self):
        self.assertLess(second_minor, second_major)
        self.assertLessEqual(second_minor, second_major)
        self.assertLessEqual(second_major, second_major)

    def test_repr(self):
        self.assertEqual(repr(second_major), "Interval(chromatic=ChromaticInterval(value=2), diatonic=DiatonicInterval(value=1))")

    def test_octave(self):
        self.assertEqual(unison.octave(), 0)
        self.assertEqual(minus_octave.octave(), -1)
        self.assertEqual(octave.octave(), 1)

    def test_add_octave(self):
        self.assertEqual(octave.add_octave(-1), unison)
        self.assertEqual(unison.add_octave(1), octave)
        self.assertEqual(octave.add_octave(-2), minus_octave)
        self.assertEqual(minus_octave.add_octave(2), octave)

    def test_same_interval_in_base_octave(self):
        self.assertEqual(octave.in_base_octave(), unison)
        self.assertEqual(minus_octave.in_base_octave(), unison)
        self.assertEqual(unison.in_base_octave(), unison)
        self.assertEqual(second_major.in_base_octave(), second_major)

    def test_same_interval_in_different_octave(self):
        self.assertFalse(second_major.equals_modulo_octave(unison))
        self.assertFalse(second_major.equals_modulo_octave(octave))
        self.assertFalse(second_major.equals_modulo_octave(minus_octave))
        self.assertTrue(unison.equals_modulo_octave(unison))
        self.assertTrue(unison.equals_modulo_octave(octave))
        self.assertTrue(unison.equals_modulo_octave(minus_octave))
        self.assertTrue(octave.equals_modulo_octave(minus_octave))

    def test_mul(self):
        self.assertEqual(unison * 4, unison)
        self.assertEqual(second_major * 2, third_major)

    def test_one_octave(self):
        self.assertEqual(Interval.one_octave(), Interval.make(chromatic=12, diatonic=7))
