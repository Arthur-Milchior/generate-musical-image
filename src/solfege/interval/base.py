from __future__ import annotations

import math
from typing import Optional
import unittest


class _Interval:
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
    modulo: int

    def __init__(self, value=None, toCopy: Optional[_Interval] = None, callerClass=None, none=None, **kwargs):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used. none, if true,
        means that there is no value and it is acceptable"""
        super().__init__(**kwargs)
        self.dic = dict()
        if none:
            assert (value is None)
            assert (toCopy is None)
            assert (callerClass is None)
            self.value = None
            return
        if toCopy is not None:
            if not isinstance(toCopy, callerClass):
                raise Exception("An interval: %s is not of the class %s" % (toCopy, callerClass))
            number = toCopy.get_number() if toCopy.has_number() else None
        else:
            number = value
        if not isinstance(number, int):
            raise (Exception("A result which is not a number but %s.\n value:%s, toCopy:%s, callerClass:%s,none:%s" % (
                number, value, toCopy, callerClass, none)))
        self.value = number

    def is_note(self):
        """True if it's a note. False if it's an interval"""
        return False

    def has_number(self):
        return isinstance(self.value, int)

    def get_number(self):
        if not isinstance(self.value, int):
            raise Exception("A number which is not int but %s" % self.value)
        return self.value

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise Exception(f"Comparison of two distinct classes: {self.__class__} and {other.__class__}")
        return self.get_number() == other.get_number()

    def __add__(self, other):
        """Sum of both intervals. Class of `self`"""
        from solfege.note.base import _Note
        if isinstance(other, _Note):
            clazz = other.__class__
        else:
            clazz = self.__class__
        if not isinstance(other, int):
            otherNumber = other.get_number()
        else:
            otherNumber = other
        sum_ = self.get_number() + otherNumber
        ret = clazz(value=sum_)
        # debug("Adding %s and %s we obtain %s",(self,other,ret))
        return ret

    def __neg__(self):
        """Inverse interval"""
        Class = self.ClassToTransposeTo or self.__class__
        return self.__class__(value=-self.get_number())

    def __sub__(self, other):
        """This interval minus the other one. Class of `self`"""
        neg = -other
        if neg.is_note():
            raise Exception("Neg is %s, which is a note" % neg)
        return (self + neg)

    def __hash__(self):
        return self.get_number()

    def __le__(self, other):
        if isinstance(other, _Interval):
            other = other.get_number()
        return self.get_number() <= other

    def __lt__(self, other):
        if isinstance(other, _Interval):
            other = other.get_number()
        return self.get_number() < other

    def __repr__(self):
        return f"{self.__class__.__name__}({self.get_number()})"

    def get_octave(self):
        """The octave number. 0 for unison/central C up to seventh/C one octave above."""
        return math.floor(self.get_number() / self.__class__.modulo)

    def add_octave(self, nb):
        """Same note with nb more octave"""
        Class = self.ClassToTransposeTo or self.__class__
        return Class(value=self.get_number() + nb * self.__class__.modulo)

    def get_same_note_in_base_octave(self):
        """Same note in the base octave"""
        return self.add_octave(-self.get_octave())

    def same_notes_in_different_octaves(self, other):
        """Whether self and other are same note, potentially at distinct octaves"""
        return self.get_same_note_in_base_octave() == other.get_same_note_in_base_octave()

    def difference_in_base_octave(self, other):
        """self-other, in octave"""
        Class = self.ClassToTransposeTo or self.__class__
        return Class((self.get_number() - other.get_number()) % self.__class__.modulo)


class TestInterval(unittest.TestCase):
    zero = _Interval(0)
    un = _Interval(1)
    moins_un = _Interval(-1)
    deux = _Interval(2)
    trois = _Interval(3)

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
        self.assertEquals(repr(self.un), "_Interval(1)")
