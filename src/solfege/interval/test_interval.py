import unittest
from .interval import *

class TestInterval(unittest.TestCase):

    def test_is_note(self):
        self.assertFalse(unison.is_note())

    def test_has_number(self):
        self.assertTrue(unison.has_number())

    def test_get_number(self):
        self.assertEqual(unison.get_number(), 0)

    def test_equal(self):
        self.assertEqual(unison, unison)
        self.assertNotEqual(second_major, unison)
        self.assertEqual(second_major, second_major)

    def test_add(self):
        self.assertEqual(second_major + second_minor, third_minor)

    def test_neg(self):
        self.assertEqual(-second_minor, minus_second_minor)

    def test_sub(self):
        self.assertEqual(third_minor - second_major, second_minor)

    def test_lt(self):
        self.assertLess(second_minor, second_major)
        self.assertLessEqual(second_minor, second_major)
        self.assertLessEqual(second_major, second_major)

    def test_repr(self):
        self.assertEqual(repr(second_major), "Interval(chromatic = 2, diatonic = 1)")

    def test_get_octave(self):
        self.assertEqual(unison.get_octave(), 0)
        self.assertEqual(minus_octave.get_octave(), -1)
        self.assertEqual(octave.get_octave(), 1)

    def test_add_octave(self):
        self.assertEqual(octave.add_octave(-1), unison)
        self.assertEqual(unison.add_octave(1), octave)
        self.assertEqual(octave.add_octave(-2), minus_octave)
        self.assertEqual(minus_octave.add_octave(2), octave)

    def test_same_interval_in_base_octave(self):
        self.assertEqual(octave.get_in_base_octave(), unison)
        self.assertEqual(minus_octave.get_in_base_octave(), unison)
        self.assertEqual(unison.get_in_base_octave(), unison)
        self.assertEqual(second_major.get_in_base_octave(), second_major)

    def test_same_interval_in_different_octave(self):
        self.assertFalse(second_major.equals_modulo_octave(unison))
        self.assertFalse(second_major.equals_modulo_octave(octave))
        self.assertFalse(second_major.equals_modulo_octave(minus_octave))
        self.assertTrue(unison.equals_modulo_octave(unison))
        self.assertTrue(unison.equals_modulo_octave(octave))
        self.assertTrue(unison.equals_modulo_octave(minus_octave))
        self.assertTrue(octave.equals_modulo_octave(minus_octave))

    def test_clean_interval_interval(self):
        i = Interval(chromatic=3, diatonic=2)
        self.assertEqual(Interval.factory(i), i)

    def test_clean_interval_int(self):
        self.assertEqual(Interval.factory(3), Interval(chromatic=3, diatonic=1))

    def test_clean_interval_tuple(self):
        self.assertEqual(Interval.factory((3, 2)), Interval(chromatic=3, diatonic=2))

    def test_mul(self):
        self.assertEqual(unison * 4, unison)
        self.assertEqual(second_major * 2, third_major)
        self.assertEqual(2 * second_major, third_major)
        self.assertEqual(4 * unison, unison)

    def test_one_octave(self):
        self.assertEqual(Interval.get_one_octave(), Interval(chromatic=12, diatonic=7))
