from __future__ import annotations

from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Dict, List, Optional, Self, Type, Union, overload

from solfege.value.interval.alteration.alteration import Alteration
from solfege.value.interval.alteration.just_alteration import JustAlteration
from solfege.value.interval.alteration.minor_major_alteration import MinorMajorAlteration
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.abstract_interval import AbstractInterval
from solfege.value.interval.interval_alteration import IntervalAlteration
from solfege.value.interval.role.interval_role import IntervalRole
from solfege.value.pair import Pair
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True, eq=False, repr=False)
class Interval(AbstractInterval, Pair[ChromaticInterval, DiatonicInterval, IntervalAlteration]):
    """A solfège interval. Composed of both a diatonic interval and a chromatic interval."""
    DiatonicClass: ClassVar[Type[DiatonicInterval]] = DiatonicInterval
    ChromaticClass: ClassVar[Type[ChromaticInterval]] = ChromaticInterval
    AlterationClass: ClassVar[Alteration] = IntervalAlteration

    def __post_init__(self):
        super().__post_init__()
        chromatic_role = self.get_chromatic()._role
        if chromatic_role is not None:
            assert self.get_role() == chromatic_role
        assert_typing(self.get_chromatic(), ChromaticInterval)
        assert_typing(self._diatonic, DiatonicInterval)

    def __mul__(self, other: int) -> Self:
        assert isinstance(other, int)
        diatonic = self._diatonic * other
        chromatic = self.get_chromatic() * other
        assert_typing(diatonic, diatonic.__class__)
        assert_typing(chromatic, chromatic.__class__)
        return self.make_instance_of_selfs_class(_chromatic=chromatic, _diatonic=diatonic)
    
    def __add__(self, other: Self) -> Self:
        if not other.__class__ == self.__class__:
            return NotImplemented
        return self.make_instance_of_selfs_class(_chromatic=self.get_chromatic() + other.get_chromatic(), _diatonic=self._diatonic+other._diatonic)
    
    #pragma mark - ChromaticGetter
    
    def get_chromatic(self)-> ChromaticInterval:
        role = self.get_role()
        current_chromatic = self._chromatic
        chromatic_role = current_chromatic._role
        if chromatic_role is not None:
            assert chromatic_role == role
        return dataclasses.replace(current_chromatic, _role = role)

    #pragma mark - AbstractInterval

    def __neg__(self) -> Self:
        return self.make_instance_of_selfs_class(_chromatic=-self.get_chromatic(), _diatonic=-self._diatonic)
    
    def get_role(self) -> IntervalRole:
        if self._role is None:
            from solfege.value.interval.role.interval_role_from_interval import IntervalRoleFromInterval
            return IntervalRoleFromInterval(self)
        return self._role

    @classmethod
    def unison(cls):
        return cls.make(0, 0)
    
    #pragma mark - Pair

    def get_alteration_constructor(self) ->IntervalAlteration:
        if self._diatonic.in_base_octave().value in [0, 4, 5]:
            return JustAlteration.make
        else:
            return MinorMajorAlteration.make
        
    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        kwargs["_role"] = None
        return kwargs


class IntervalFrozenList(FrozenList[Interval]):
    type = Interval

    def get_chromatic_intervals(self) ->ChromaticIntervalFrozenList:
        return ChromaticIntervalFrozenList.make(interval.get_chromatic() for interval in self)

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
