from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional, Self, Type, Union, overload

from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.abstract_interval import AbstractInterval
from solfege.value.pair import Pair
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True, eq=False, repr=False)
class Interval(AbstractInterval, Pair[ChromaticInterval, DiatonicInterval]):
    """A solfège interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass: ClassVar[Type[DiatonicInterval]] = DiatonicInterval
    ChromaticClass: ClassVar[Type[ChromaticInterval]] = ChromaticInterval

    chromatic: ChromaticInterval
    diatonic: DiatonicInterval

    def __post_init__(self):
        super().__post_init__()
        assert_typing(self.chromatic, ChromaticInterval)
        assert_typing(self.diatonic, DiatonicInterval)

    def __mul__(self, other: int) -> Self:
        assert isinstance(other, int)
        diatonic = self.diatonic * other
        chromatic = self.chromatic * other
        assert_typing(diatonic, diatonic.__class__)
        assert_typing(chromatic, chromatic.__class__)
        return self.make_instance_of_selfs_class(chromatic=chromatic, diatonic=diatonic)
    
    def __add__(self, other: Self) -> Self:
        if not other.__class__ == self.__class__:
            return NotImplemented
        return self.make_instance_of_selfs_class(chromatic=self.chromatic + other.chromatic, diatonic=self.diatonic+other.diatonic)    

    #pragma mark - AbstractInterval
    def __neg__(self) -> Self:
        return self.make_instance_of_selfs_class(chromatic=-self.chromatic, diatonic=-self.diatonic)

    @classmethod
    def unison(cls):
        return cls.make(0, 0)


class IntervalFrozenList(FrozenList[Interval]):
    type = Interval

    def get_chromatic_intervals(self) ->ChromaticIntervalFrozenList:
        return ChromaticIntervalFrozenList.make(interval.chromatic for interval in self)

Interval.IntervalClass = Interval
Interval.PairClass = Interval
ChromaticInterval.PairClass = Interval
DiatonicInterval.PairClass = Interval

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
