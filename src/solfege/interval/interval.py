from __future__ import annotations

import unittest
from typing import Optional

from solfege.interval.chromatic import ChromaticInterval
from solfege.interval.diatonic import DiatonicInterval


class Interval(ChromaticInterval):
    """A solfège interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass = DiatonicInterval
    ChromaticClass = ChromaticInterval

    def __init__(self, chromatic: Optional[int] = None, diatonic: Optional[int] = None,
                 alteration: Optional[int] = None,
                 none=None, **kwargs):
        """chromatic and diatonic are used.
        Otherwise, if chromatic is present, it supposed to be the exact value.
        otherwise, alteration should be present, and chromatic is the sum of diatonic and alteration
        """
        assert (alteration is not None or chromatic is not None or none is not None)
        if none:
            super().__init__(none=none)
            assert (chromatic is None)
            assert (diatonic is None)
            assert (alteration is None)
        else:
            self._diatonic = self.__class__.DiatonicClass(diatonic=diatonic)
            if chromatic is not None:
                assert (isinstance(chromatic, int))
                super().__init__(chromatic=chromatic)
            else:
                assert alteration
                assert (isinstance(alteration, int))
                self.initChromaticAbsent(alteration)
                super().__init__(chromatic=self._diatonic.get_chromatic().get_number() + alteration)

    @classmethod
    def factory(cls, interval):
        """Allow a simple representation of intervals.
        An interval return itself
        A pair is considered as (chromatic, diatonic)
        An int is considered as a chromatic value, for diatonic one."""

        if isinstance(interval, Interval):
            return interval
        if isinstance(interval, int):
            return cls(chromatic=interval, diatonic=1)
        if isinstance(interval, tuple):
            assert (len(interval) == 2)
            chromatic, diatonic = interval
            return cls(chromatic=chromatic, diatonic=diatonic)

    def __eq__(self, other: Interval):
        diatonicEq = self.get_diatonic() == other.get_diatonic()
        chromaticEq = super().__eq__(other)
        return diatonicEq and chromaticEq

    def __hash__(self):
        return hash(self.get_chromatic())

    def __neg__(self):
        Class = self.ClassToTransposeTo or self.__class__
        return Class(chromatic=-self.get_number(), diatonic=-self.get_diatonic().get_number())

    def get_chromatic(self):
        return self.ChromaticClass(chromatic=self.get_number())

    def get_diatonic(self):
        return self._diatonic

    def __repr__(self):
        return f"{self.__class__.__name__}(chromatic = {self.get_chromatic().get_number()}, diatonic = {self.get_diatonic().get_number()})"

    def __add__(self, other):
        diatonic = self.get_diatonic() + other.get_diatonic()
        chromatic = self.get_chromatic() + other.get_chromatic()
        from solfege.note.abstract import AbstractNote
        if self.ClassToTransposeTo:
            clazz = self.ClassToTransposeTo
        elif isinstance(other, AbstractNote):
            clazz = other.__class__
        else:
            clazz = self.__class__
        return clazz(chromatic=chromatic.get_number(), diatonic=diatonic.get_number())

    def __mul__(self, other):
        from solfege.note.abstract import AbstractNote
        assert (not isinstance(self, AbstractNote))
        assert (isinstance(other, int))
        diatonic = self.get_diatonic() * other
        chromatic = self.get_chromatic() * other
        clazz = self.ClassToTransposeTo or self.__class__
        return clazz(chromatic=chromatic.get_number(), diatonic=diatonic.get_number())

    @classmethod
    def get_one_octave(cls):
        return Interval(chromatic=12, diatonic=7)

    def get_octave(self):
        return self.get_diatonic().get_octave()


ChromaticInterval.RelatedSolfegeClass = Interval
Interval.IntervalClass = Interval


class TestInterval(unittest.TestCase):
    minus_octave = Interval(-12, -7)
    minus_second_minor = Interval(-1, -1)
    unison = Interval(0, 0)
    second_minor = Interval(1, 1)
    second_major = Interval(2, 1)
    third_major = Interval(4, 2)
    third_minor = Interval(3, 2)
    octave = Interval(12, 7)

    def test_is_note(self):
        self.assertFalse(self.unison.is_note())

    def test_has_number(self):
        self.assertTrue(self.unison.has_number())

    def test_get_number(self):
        self.assertEquals(self.unison.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.unison, self.unison)
        self.assertNotEquals(self.second_major, self.unison)
        self.assertEquals(self.second_major, self.second_major)

    def test_add(self):
        self.assertEquals(self.second_major + self.second_minor, self.third_minor)

    def test_neg(self):
        self.assertEquals(-self.second_minor, self.minus_second_minor)

    def test_sub(self):
        self.assertEquals(self.third_minor - self.second_major, self.second_minor)

    def test_lt(self):
        self.assertLess(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_minor, self.second_major)
        self.assertLessEqual(self.second_major, self.second_major)

    def test_repr(self):
        self.assertEquals(repr(self.second_major), "Interval(chromatic = 2, diatonic = 1)")

    def test_get_octave(self):
        self.assertEquals(self.unison.get_octave(), 0)
        self.assertEquals(self.minus_octave.get_octave(), -1)
        self.assertEquals(self.octave.get_octave(), 1)

    def test_add_octave(self):
        self.assertEquals(self.octave.add_octave(-1), self.unison)
        self.assertEquals(self.unison.add_octave(1), self.octave)
        self.assertEquals(self.octave.add_octave(-2), self.minus_octave)
        self.assertEquals(self.minus_octave.add_octave(2), self.octave)

    def test_same_interval_in_base_octave(self):
        self.assertEquals(self.octave.get_in_base_octave(), self.unison)
        self.assertEquals(self.minus_octave.get_in_base_octave(), self.unison)
        self.assertEquals(self.unison.get_in_base_octave(), self.unison)
        self.assertEquals(self.second_major.get_in_base_octave(), self.second_major)

    def test_same_interval_in_different_octave(self):
        self.assertFalse(self.second_major.equals_modulo_octave(self.unison))
        self.assertFalse(self.second_major.equals_modulo_octave(self.octave))
        self.assertFalse(self.second_major.equals_modulo_octave(self.minus_octave))
        self.assertTrue(self.unison.equals_modulo_octave(self.unison))
        self.assertTrue(self.unison.equals_modulo_octave(self.octave))
        self.assertTrue(self.unison.equals_modulo_octave(self.minus_octave))
        self.assertTrue(self.octave.equals_modulo_octave(self.minus_octave))

    def test_clean_interval_interval(self):
        i = Interval(chromatic=3, diatonic=2)
        self.assertEquals(Interval.factory(i), i)

    def test_clean_interval_int(self):
        self.assertEquals(Interval.factory(3), Interval(chromatic=3, diatonic=1))

    def test_clean_interval_tuple(self):
        self.assertEquals(Interval.factory((3, 2)), Interval(chromatic=3, diatonic=2))

    def test_mul(self):
        self.assertEquals(self.unison * 4, self.unison)
        self.assertEquals(self.second_major * 2, self.third_major)
        self.assertEquals(2 * self.second_major, self.third_major)
        self.assertEquals(4 * self.unison, self.unison)

    def test_one_octave(self):
        self.assertEquals(Interval.get_one_octave(), Interval(chromatic=12, diatonic=7))