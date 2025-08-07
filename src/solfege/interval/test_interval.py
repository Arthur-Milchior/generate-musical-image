from .interval import *

class TestInterval(unittest.TestCase):

    def test_is_note(self):
        self.assertFalse(unison.is_note())

    def test_has_number(self):
        self.assertTrue(unison.has_number())

    def test_get_number(self):
        self.assertEquals(unison.get_number(), 0)

    def test_equal(self):
        self.assertEquals(unison, unison)
        self.assertNotEquals(second_major, unison)
        self.assertEquals(second_major, second_major)

    def test_add(self):
        self.assertEquals(second_major + second_minor, third_minor)

    def test_neg(self):
        self.assertEquals(-second_minor, minus_second_minor)

    def test_sub(self):
        self.assertEquals(third_minor - second_major, second_minor)

    def test_lt(self):
        self.assertLess(second_minor, second_major)
        self.assertLessEqual(second_minor, second_major)
        self.assertLessEqual(second_major, second_major)

    def test_repr(self):
        self.assertEquals(repr(second_major), "Interval(chromatic = 2, diatonic = 1)")

    def test_get_octave(self):
        self.assertEquals(unison.get_octave(), 0)
        self.assertEquals(minus_octave.get_octave(), -1)
        self.assertEquals(octave.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(octave.add_octave(-1), unison)
        self.assertEquals(unison.add_octave(1), octave)
        self.assertEquals(octave.add_octave(-2), minus_octave)
        self.assertEquals(minus_octave.add_octave(2), octave)

    def test_same_interval_in_base_octave(self):
        self.assertEquals(octave.get_in_base_octave(), unison)
        self.assertEquals(minus_octave.get_in_base_octave(), unison)
        self.assertEquals(unison.get_in_base_octave(), unison)
        self.assertEquals(second_major.get_in_base_octave(), second_major)

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
        self.assertEquals(Interval.factory(i), i)

    def test_clean_interval_int(self):
        self.assertEquals(Interval.factory(3), Interval(chromatic=3, diatonic=1))

    def test_clean_interval_tuple(self):
        self.assertEquals(Interval.factory((3, 2)), Interval(chromatic=3, diatonic=2))

    def test_mul(self):
        self.assertEquals(unison * 4, unison)
        self.assertEquals(second_major * 2, third_major)
        self.assertEquals(2 * second_major, third_major)
        self.assertEquals(4 * unison, unison)

    def test_one_octave(self):
        self.assertEquals(Interval.get_one_octave(), Interval(chromatic=12, diatonic=7))
