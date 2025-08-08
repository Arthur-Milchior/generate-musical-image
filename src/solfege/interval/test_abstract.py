import unittest
from .abstract import *

class TestBaseInterval(unittest.TestCase):
    zero = AbstractInterval(0)
    un = AbstractInterval(1)
    moins_un = AbstractInterval(-1)
    deux = AbstractInterval(2)
    trois = AbstractInterval(3)

    def test_is_note(self):
        self.assertFalse(self.zero.is_note())

    def test_has_number(self):
        self.assertTrue(self.zero.has_number())

    def test_get_number(self):
        self.assertEqual(self.zero.get_number(), 0)

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
        self.assertLessEqual(self.un, self.un)

    def test_repr(self):
        self.assertEqual(repr(self.un), "AbstractInterval(value=1)")

    def test_mul(self):
        self.assertEqual(self.zero * 4, self.zero)
        self.assertEqual(self.un * 2, self.deux)
        self.assertEqual(2 * self.un, self.deux)
        self.assertEqual(4 * self.zero, self.zero)
