import unittest

from solfege.value.interval.singleton_interval import AbstractSingletonInterval

class FakeSingletonInterval(AbstractSingletonInterval):
    def get_chromatic(self):
        return self
    def get_diatonic(self):
        return self

class TestBaseIntervalSingleton(unittest.TestCase):
    zero = FakeSingletonInterval.make(0)
    un = FakeSingletonInterval.make(1)
    moins_un = FakeSingletonInterval.make(-1)
    deux = FakeSingletonInterval.make(2)
    trois = FakeSingletonInterval.make(3)

    def test_is_note(self):
        self.assertFalse(self.zero.is_note())

    def test_get_number(self):
        self.assertEqual(self.zero.value, 0)

    def test_equal(self):
        self.assertEqual(self.zero, self.zero)
        self.assertNotEqual(self.un, self.zero)
        self.assertEqual(self.un, self.un)

    def test_add(self):
        self.assertEqual(self.un + self.deux, self.trois)

    def test_neg(self):
        self.assertEqual(-self.un, self.moins_un)

    def test_sub(self):
        self.assertEqual(self.trois - self.deux, self.un)

    def test_lt(self):
        self.assertLess(self.un, self.deux)
        self.assertLessEqual(self.un, self.deux)
    #     self.assertLessEqual(self.un, self.un)

    # def test_repr(self):
    #     actual = repr(self.un)
    #     expected = "FakeSingletonInterval.make(value=1)"
    #     self.assertEqual(actual, expected)

    def test_mul(self):
        self.assertEqual(self.zero * 4, self.zero)
        # self.assertEqual(self.un * 2, self.deux)
        # self.assertEqual(2 * self.un, self.deux)
        # self.assertEqual(4 * self.zero, self.zero)