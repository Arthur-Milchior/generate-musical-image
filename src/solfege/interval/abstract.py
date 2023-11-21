from __future__ import annotations

import math
from typing import TypeVar
import unittest


class AbstractInterval:
    """This class is the basis for each kind of interval. It should never be used directly.
    It allows to represent a number, access it.
    It also allows to add it to another such element, negate it, while generating an object of its subclass.
    Such elements can be compared, and basically hashed (the hash being the number itself)

    The number can't be set, because the object is supposed to be immutable.

    Inheriting class which are instantiated should contain the following variable:
    * modulo: number of note by octave (7 for diatonic, 12 for chromatic)
    * ClassToTransposeTo: the class of object to generate. If it's None, the class of self is used.
    * RelatedDiatonicClass: class to which a chromatic object must be converted when a diatonic object is required.
    * RelatedSolfegeClass: the class to which a diatonic and chromatic object must be converted.
"""
    ClassToTransposeTo = None
    number_of_interval_in_an_octave: int
    IntervalClass: type(AbstractInterval)
    value: int

    def __init__(self, value: int, **kwargs):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used."""
        super().__init__(**kwargs)
        self.value = value

    def is_note(self):
        """True if it's a note. False if it's an interval"""
        return False

    def has_number(self):
        return isinstance(self.value, int)

    def get_number(self):
        if not isinstance(self.value, int):
            raise Exception("A number which is not int but %s" % self.value)
        return self.value

    @classmethod
    def get_one_octave(cls):
        return cls.IntervalClass(value=cls.number_of_interval_in_an_octave)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise Exception(f"Comparison of two distinct classes: {self.__class__} and {other.__class__}")
        return self.get_number() == other.get_number()

    def __add__(self, other):
        """Sum of both intervals. Class of `self`"""
        from solfege.note.abstract import AbstractNote
        if isinstance(other, AbstractNote):
            clazz = other.__class__
        else:
            clazz = self.__class__
        if not isinstance(other, int):
            other_number = other.get_number()
        else:
            other_number = other
        sum_ = self.get_number() + other_number
        ret = clazz(value=sum_)
        return ret

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        assert (isinstance(other, int))
        from solfege.note.abstract import AbstractNote
        assert (not isinstance(self, AbstractNote))
        clazz = self.ClassToTransposeTo or self.__class__
        return clazz(value=self.get_number() * other)

    def __neg__(self):
        """Inverse interval"""
        clazz = self.ClassToTransposeTo or self.__class__
        return clazz(value=-self.get_number())

    def __sub__(self, other):
        """This interval minus the other one. Class of `self`"""
        neg = -other
        if neg.is_note():
            raise Exception("Neg is %s, which is a note" % neg)
        return self + neg

    def __hash__(self):
        return self.get_number()

    def __le__(self, other):
        if isinstance(other, AbstractInterval):
            other = other.get_number()
        return self.get_number() <= other

    def __lt__(self, other):
        if isinstance(other, AbstractInterval):
            other = other.get_number()
        return self.get_number() < other

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.get_number()})"

    def get_octave(self):
        """The octave number. 0 for unison/central C up to seventh/C one octave above."""
        return math.floor(self.get_number() / self.__class__.number_of_interval_in_an_octave)

    def add_octave(self, nb):
        """Same note with nb more octave"""
        return self + self.get_one_octave() * nb

    def get_in_base_octave(self):
        """Same note in the base octave"""
        octave = self.get_octave()
        if octave == 0:
            return self
        return self.add_octave(-self.get_octave())

    def equals_modulo_octave(self, other):
        """Whether self and other are same note, potentially at distinct octaves"""
        return self.get_in_base_octave() == other.get_in_base_octave()

    def difference_in_base_octave(self, other):
        """self-other, in octave"""
        clazz = self.ClassToTransposeTo or self.__class__
        return clazz((self.get_number() - other.get_number()) % self.__class__.number_of_interval_in_an_octave)


IntervalType = TypeVar('IntervalType', bound=AbstractInterval)


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
        self.assertEquals(self.zero.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.zero, self.zero)
        self.assertNotEquals(self.un, self.zero)
        self.assertEquals(self.un, self.un)

    def test_add(self):
        self.assertEquals(self.un + self.deux, self.trois)

    def test_neg(self):
        self.assertEquals(-self.un, self.moins_un)

    def test_sub(self):
        self.assertEquals(self.trois - self.deux, self.un)

    def test_lt(self):
        self.assertLess(self.un, self.deux)
        self.assertLessEqual(self.un, self.deux)
        self.assertLessEqual(self.un, self.un)

    def test_repr(self):
        self.assertEquals(repr(self.un), "AbstractInterval(value=1)")

    def test_mul(self):
        self.assertEquals(self.zero * 4, self.zero)
        self.assertEquals(self.un * 2, self.deux)
        self.assertEquals(2 * self.un, self.deux)
        self.assertEquals(4 * self.zero, self.zero)
