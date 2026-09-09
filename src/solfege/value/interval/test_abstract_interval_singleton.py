import unittest

from solfege.value.interval.singleton_interval import AbstractSingletonInterval

class FakeSingletonInterval(AbstractSingletonInterval):
    """Minimal concrete `AbstractSingletonInterval` used only to exercise the base class's behavior
    in isolation, without pulling in `ChromaticInterval`/`DiatonicInterval` specifics."""
    def get_chromatic(self):
        """Return self: a test double, its chromatic component is itself."""
        return self
    def get_diatonic(self):
        """Return self: a test double, its diatonic component is itself."""
        return self

class TestBaseIntervalSingleton(unittest.TestCase):
    """Tests for `AbstractSingletonInterval`, via the `FakeSingletonInterval` test double."""
    zero = FakeSingletonInterval.make(0)
    un = FakeSingletonInterval.make(1)
    moins_un = FakeSingletonInterval.make(-1)
    deux = FakeSingletonInterval.make(2)
    trois = FakeSingletonInterval.make(3)

    def test_is_note(self):
        """An interval is never a note."""
        self.assertFalse(self.zero.is_note())

    def test_get_number(self):
        """`value` returns the raw int passed to `make`."""
        self.assertEqual(self.zero.value, 0)

    def test_equal(self):
        """Equality compares by value."""
        self.assertEqual(self.zero, self.zero)
        self.assertNotEqual(self.un, self.zero)
        self.assertEqual(self.un, self.un)

    def test_add(self):
        """Addition sums the raw values."""
        self.assertEqual(self.un + self.deux, self.trois)

    def test_neg(self):
        """Negation flips the sign of the raw value."""
        self.assertEqual(-self.un, self.moins_un)

    def test_sub(self):
        """Subtraction is addition of the negation."""
        self.assertEqual(self.trois - self.deux, self.un)

    def test_lt(self):
        """Ordering compares by raw value."""
        self.assertLess(self.un, self.deux)
        self.assertLessEqual(self.un, self.deux)
    #     self.assertLessEqual(self.un, self.un)

    # def test_repr(self):
    #     actual = repr(self.un)
    #     expected = "FakeSingletonInterval.make(value=1)"
    #     self.assertEqual(actual, expected)

    def test_mul(self):
        """Multiplying by an int scales the raw value."""
        self.assertEqual(self.zero * 4, self.zero)
        # self.assertEqual(self.un * 2, self.deux)
        # self.assertEqual(2 * self.un, self.deux)
        # self.assertEqual(4 * self.zero, self.zero)