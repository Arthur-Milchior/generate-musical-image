from __future__ import annotations

from typing import Optional, Self

from solfege.interval.chromatic import ChromaticInterval
from solfege.interval.diatonic import DiatonicInterval


class Interval(ChromaticInterval):
    """A solfège interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass = DiatonicInterval
    ChromaticClass = ChromaticInterval

    def __init__(self, chromatic: Optional[int] = None, diatonic: Optional[int] = None,
                 alteration: Optional[int] = None, **kwargs):
        """chromatic and diatonic are used.
        Otherwise, if chromatic is present, it supposed to be the exact value.
        otherwise, alteration should be present, and chromatic is the sum of diatonic and alteration
        """
        assert (alteration is not None) or (chromatic is not None)
        self._diatonic = self.__class__.DiatonicClass(value=diatonic)
        if chromatic is not None:
            assert (isinstance(chromatic, int))
            super().__init__(value=chromatic)
        else:
            assert (isinstance(alteration, int))
            super().__init__(value=self._diatonic.get_chromatic().get_number() + alteration)

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
        return self.ChromaticClass(self.get_number())

    def get_diatonic(self) -> DiatonicInterval:
        return self._diatonic

    def __repr__(self):
        return f"{self.__class__.__name__}(chromatic = {self.get_chromatic().get_number()}, diatonic = {self.get_diatonic().get_number()})"

    def __add__(self, other) -> Self:
        diatonic = self.get_diatonic() + other.get_diatonic()
        chromatic = self.get_chromatic() + other.get_chromatic()
        from solfege.note.abstract import AbstractNote
        if self.ClassToTransposeTo:
            cls = self.ClassToTransposeTo
        elif isinstance(other, AbstractNote):
            cls = other.__class__
        else:
            cls = self.__class__
        return cls(chromatic=chromatic.get_number(), diatonic=diatonic.get_number())

    def __mul__(self, other):
        from solfege.note.abstract import AbstractNote
        assert (not isinstance(self, AbstractNote))
        assert (isinstance(other, int))
        diatonic = self.get_diatonic() * other
        chromatic = self.get_chromatic() * other
        cls = self.ClassToTransposeTo or self.__class__
        return cls(chromatic=chromatic.get_number(), diatonic=diatonic.get_number())

    @classmethod
    def get_one_octave(cls):
        return Interval(chromatic=12, diatonic=7)

    def get_octave(self):
        return self.get_diatonic().get_octave()


ChromaticInterval.RelatedSolfegeClass = Interval
Interval.IntervalClass = Interval

minus_octave = Interval(-12, -7)
minus_second_minor = Interval(-1, -1)
unison = Interval(0, 0)
second_minor = Interval(1, 1)
second_major = Interval(2, 1)
third_major = Interval(4, 2)
third_minor = Interval(3, 2)
octave = Interval(12, 7)


