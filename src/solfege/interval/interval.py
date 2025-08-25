from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional, Self, Type, Union

from solfege.interval.chromatic_interval import ChromaticInterval
from solfege.interval.diatonic_interval import DiatonicInterval
from solfege.interval.abstract_interval import AbstractInterval
from solfege.value.pair import Pair
from utils.util import assert_typing


@dataclass(frozen=True)
class Interval(AbstractInterval, Pair):
    """A solfège interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass: ClassVar[Type[DiatonicInterval]] = DiatonicInterval
    ChromaticClass: ClassVar[Type[ChromaticInterval]] = ChromaticInterval

    chromatic: ChromaticInterval
    diatonic: DiatonicInterval

    def __post_init__(self):
        super().__post_init__()
        assert_typing(self.chromatic, ChromaticInterval)
        assert_typing(self.diatonic, DiatonicInterval)

    def __neg__(self):
        return self.make_instance_of_selfs_class(chromatic=-self.chromatic, diatonic=-self.diatonic)

    def __mul__(self, other: int):
        assert isinstance(other, int)
        diatonic = self.diatonic * other
        chromatic = self.chromatic * other
        assert_typing(diatonic, diatonic.__class__)
        assert_typing(chromatic, chromatic.__class__)
        return self.make_instance_of_selfs_class(chromatic=chromatic, diatonic=diatonic)


Interval.PairClass = Interval
ChromaticInterval.PairClass = Interval
DiatonicInterval.PairClass = Interval
Pair.IntervalClass = Interval

ChromaticInterval.DiatonicClass = DiatonicInterval
DiatonicInterval.ChromaticClass = ChromaticInterval

minus_octave = Interval.make(-12, -7)
minus_second_minor = Interval.make(-1, -1)
unison = Interval.make(0, 0)
second_minor = Interval.make(1, 1)
second_major = Interval.make(2, 1)
third_major = Interval.make(4, 2)
third_minor = Interval.make(3, 2)
octave = Interval.make(12, 7)
