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
    """The diatonic-only class used for this pair's diatonic component."""
    ChromaticClass: ClassVar[Type[ChromaticInterval]] = ChromaticInterval
    """The chromatic-only class used for this pair's chromatic component."""
    AlterationClass: ClassVar[Alteration] = IntervalAlteration
    """The alteration base class used to express this interval's diatonic degree as minor/major or
    diminished/just/augmented (the concrete constructor is picked by `get_alteration_constructor`)."""

    def __post_init__(self):
        """Validate component types, and that the chromatic component's role (if set) agrees with this
        interval's own role."""
        super().__post_init__()
        chromatic_role = self.get_chromatic()._role
        if chromatic_role is not None:
            assert self.get_role() == chromatic_role
        assert_typing(self.get_chromatic(), ChromaticInterval)
        assert_typing(self._diatonic, DiatonicInterval)

    def __mul__(self, other: int) -> Self:
        """Scale both components by the int `other` (e.g. a third major times 2 spans two thirds major)."""
        assert isinstance(other, int)
        diatonic = self._diatonic * other
        chromatic = self.get_chromatic() * other
        assert_typing(diatonic, diatonic.__class__)
        assert_typing(chromatic, chromatic.__class__)
        return self.make_instance_of_selfs_class(_chromatic=chromatic, _diatonic=diatonic)

    def __add__(self, other: Self) -> Self:
        """Add two intervals component-wise. Returns `NotImplemented` if `other` isn't also an `Interval`."""
        if not other.__class__ == self.__class__:
            return NotImplemented
        return self.make_instance_of_selfs_class(_chromatic=self.get_chromatic() + other.get_chromatic(), _diatonic=self._diatonic+other._diatonic)

    #pragma mark - ChromaticGetter

    def get_chromatic(self)-> ChromaticInterval:
        """Return the chromatic component, stamped with this interval's role (asserting consistency
        if the stored chromatic component already had a role of its own)."""
        role = self.get_role()
        current_chromatic = self._chromatic
        chromatic_role = current_chromatic._role
        if chromatic_role is not None:
            assert chromatic_role == role
        return dataclasses.replace(current_chromatic, _role = role)

    #pragma mark - AbstractInterval

    def __neg__(self) -> Self:
        """The opposite interval, negating both components."""
        return self.make_instance_of_selfs_class(_chromatic=-self.get_chromatic(), _diatonic=-self._diatonic)

    def get_role(self) -> IntervalRole:
        """Return `self._role` if set, otherwise infer one from the interval's own chromatic/diatonic
        values via `IntervalRoleFromInterval`."""
        if self._role is None:
            from solfege.value.interval.role.interval_role_from_interval import IntervalRoleFromInterval
            return IntervalRoleFromInterval(self)
        return self._role

    @classmethod
    def unison(cls):
        """The unison interval (chromatic 0, diatonic 0)."""
        return cls.make(0, 0)

    def notation(self) -> str:
        """Compact notation such as "3M" (major third) or "-3M" for the decreasing version, using the
        1-based diatonic degree and the alteration's `letter()`."""
        if self._diatonic.value < 0:
            return "-" + (-self).notation()
        return f"{self._diatonic.value+1}{self.get_alteration().letter()}"

    #pragma mark - Pair

    def get_alteration_constructor(self) ->IntervalAlteration:
        """Pick the alteration constructor matching this interval's diatonic degree: unison/fourth/fifth
        (indices 0, 3, 4) use `JustAlteration` (diminished/just/augmented), every other degree uses
        `MinorMajorAlteration` (diminished/minor/major/augmented)."""
        if self._diatonic.in_base_octave().value in [0, 3, 4]:
            return JustAlteration.make
        else:
            return MinorMajorAlteration.make

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `_role` to `None` when not supplied."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        kwargs["_role"] = None
        return kwargs


class IntervalFrozenList(FrozenList[Interval]):
    """A `FrozenList` specialized to hold `Interval` elements."""
    type = Interval
    """Element type enforced by `FrozenList`."""

    def get_chromatic_intervals(self) ->ChromaticIntervalFrozenList:
        """Return the chromatic component of every interval in this list, as a `ChromaticIntervalFrozenList`."""
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
