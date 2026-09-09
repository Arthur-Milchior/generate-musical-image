import unittest
from solfege.value.interval.interval import *

class TestInterval(unittest.TestCase):
    """Tests for `Interval` (the chromatic+diatonic pair)."""

    def test_is_note(self):
        """An interval is never a note."""
        self.assertFalse(unison.is_note())

    def test_equal(self):
        """Equality compares both chromatic and diatonic components."""
        self.assertEqual(unison, unison)
        self.assertNotEqual(second_major, unison)
        self.assertEqual(second_major, second_major)

    def test_add(self):
        """Addition sums both components."""
        self.assertEqual(second_major + second_minor, third_minor)
        # self.assertEqual(second_major + ChromaticInterval.make(1), ChromaticInterval.make(3))
        # self.assertEqual(ChromaticInterval.make(1) + second_major, ChromaticInterval.make(3))
        # self.assertEqual(second_major + DiatonicInterval.make(1), DiatonicInterval.make(2))
        # self.assertEqual(DiatonicInterval.make(1) + second_major, DiatonicInterval.make(2))

    def test_neg(self):
        """Negation negates both components."""
        self.assertEqual(-second_minor, minus_second_minor)

    def test_sub(self):
        """Subtraction is addition of the negation."""
        self.assertEqual(third_minor - second_major, second_minor)

    def test_lt(self):
        """Ordering compares (chromatic, diatonic) lexicographically."""
        self.assertLess(second_minor, second_major)
        self.assertLessEqual(second_minor, second_major)
        self.assertLessEqual(second_major, second_major)

    def test_repr(self):
        """`repr` is evaluable, reusing the raw chromatic/diatonic values."""
        self.assertEqual(repr(second_major), "Interval.make(2, 1)")

    def test_octave(self):
        """`octave()` derives from the diatonic component."""
        self.assertEqual(unison.octave(), 0)
        self.assertEqual(minus_octave.octave(), -1)
        self.assertEqual(octave.octave(), 1)

    def test_add_octave(self):
        """`add_octave` shifts both components by whole octaves."""
        self.assertEqual(octave.add_octave(-1), unison)
        self.assertEqual(unison.add_octave(1), octave)
        self.assertEqual(octave.add_octave(-2), minus_octave)
        self.assertEqual(minus_octave.add_octave(2), octave)

    def test_same_interval_in_base_octave(self):
        """`in_base_octave` folds intervals of various octaves down to the base octave."""
        self.assertEqual(octave.in_base_octave(), unison)
        self.assertEqual(minus_octave.in_base_octave(), unison)
        self.assertEqual(unison.in_base_octave(), unison)
        self.assertEqual(second_major.in_base_octave(), second_major)

    def test_same_interval_in_different_octave(self):
        """`equals_modulo_octave` ignores octave but not the base interval."""
        self.assertFalse(second_major.equals_modulo_octave(unison))
        self.assertFalse(second_major.equals_modulo_octave(octave))
        self.assertFalse(second_major.equals_modulo_octave(minus_octave))
        self.assertTrue(unison.equals_modulo_octave(unison))
        self.assertTrue(unison.equals_modulo_octave(octave))
        self.assertTrue(unison.equals_modulo_octave(minus_octave))
        self.assertTrue(octave.equals_modulo_octave(minus_octave))

    def test_mul(self):
        """Multiplying by an int scales both components."""
        self.assertEqual(unison * 4, unison)
        self.assertEqual(second_major * 2, third_major)

    def test_one_octave(self):
        """`one_octave()` equals (12 semitones, 7 scale degrees)."""
        self.assertEqual(Interval.one_octave(), Interval.make(_chromatic=12, _diatonic=7))
