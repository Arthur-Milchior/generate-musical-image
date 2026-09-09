from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from itertools import pairwise
from typing import Callable, ClassVar, Dict, Generic, Iterable, List, Optional, Self, Tuple, Type, TypeVar, Union

from solfege.list_order import ListOrder
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.role.interval_role import IntervalRole
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.util import assert_iterable_typing, assert_typing, sorted_unique

"""Generate the role from the index"""
RoleMaker = Callable[[int], IntervalRole]

@dataclass(frozen=True, unsafe_hash=True)
class AbstractIntervalListPattern(DataClassWithDefaultArgument, ABC, Generic[IntervalType]):
    """An ordered list of intervals, all relative to a common starting note (unison always first),
    used to represent a chord/scale's shape independently of any concrete tonic. `IntervalList`
    (chromatic+diatonic) and `ChromaticIntervalListPattern` (chromatic-only) are the concrete
    subclasses. Build with `make_absolute` (intervals already relative to the tonic) or
    `make_relative` (intervals relative to the previous note)."""
    interval_type: ClassVar[Type[AbstractInterval]]
    """The interval class held by `_absolute_intervals` (e.g. `Interval` or `ChromaticInterval`)."""
    _absolute_intervals: FrozenList[IntervalType]
    """The list of intervals, all relative to a common starting note."""
    _frozen_list_type: ClassVar[Type[FrozenList[IntervalType]]]
    """The `FrozenList` subclass used to store `_absolute_intervals`."""
    increasing: bool
    """Whether consecutive intervals in `_absolute_intervals` must be strictly increasing (True) or
    strictly decreasing (False); enforced in `__post_init__`."""

    def __len__(self):
        """Number of intervals in the list (including the leading unison)."""
        return len(self._absolute_intervals)

    @classmethod
    def make_absolute(cls, absolute_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]], *args, add_implicit_unison: bool = True, **kwargs):
        """Returns an instance of `cls` for the absolute intervals `relative_intervals`. 
        if `add_implicit_unison` then add a unison at start if it's not already here.
        """
        absolute_intervals = [cls.interval_type.make_single_argument(absolute_interval) for absolute_interval in absolute_intervals]
        assert_iterable_typing(absolute_intervals, cls.interval_type)
        first_interval = absolute_intervals[0] if absolute_intervals else None
        unison = cls.interval_type.unison()
        if first_interval != unison and add_implicit_unison:
            absolute_intervals = [unison] + absolute_intervals
        return cls.make(*args, _absolute_intervals=cls._frozen_list_type(absolute_intervals), **kwargs)

    @classmethod
    def make_relative(cls, relative_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]],  role_maker: Optional[RoleMaker]=None, *args,  **kwargs):
        """Returns an instance of `cls` for the relative intervals `relative_intervals`. Each interval has a role determined by `role_maker`."""
        unison = cls.interval_type.unison()
        if role_maker:
            unison = dataclasses.replace(unison, _role=role_maker(0))
        absolute_intervals = [unison]
        for index_relative, relative_interval in enumerate(relative_intervals):
            relative_interval = cls.interval_type.make_single_argument(relative_interval)
            next_interval = absolute_intervals[-1] + relative_interval
            if role_maker:
                next_interval = dataclasses.replace(next_interval, _role=role_maker(index_relative + 1 ))
            if relative_interval._role:
                next_interval = dataclasses.replace(next_interval, _role=relative_interval._role)
            absolute_intervals.append(next_interval)
        return cls.make(*args, _absolute_intervals=cls._frozen_list_type(absolute_intervals), **kwargs)

    def absolute_intervals(self) -> FrozenList[IntervalType]:
        """Return `_absolute_intervals` (the intervals relative to the shared starting note)."""
        return self._absolute_intervals

    def relative_intervals(self, assume_implicit_zero=True) -> FrozenList[IntervalType]:
        """Generator of the difference of intervals"""
        unison = self.interval_type.unison()
        assert self._absolute_intervals[0] == unison
        return self._frozen_list_type([higher - lower for lower, higher in pairwise(self._absolute_intervals)])

    @classmethod
    @abstractmethod
    def _note_list_constructor(cls) -> Callable[["NoteType"], "AbstractNoteList"]:
        """Return the `AbstractNoteList` subclass constructor matching this interval-list type
        (e.g. `NoteList` for `IntervalList`, `ChromaticNoteList` for `ChromaticIntervalListPattern`)."""
        ...
    def _from_note(self, note: "NoteType") -> FrozenList["NoteType"]:
        """Add each absolute interval to `note`, returning the resulting notes as a frozen list."""
        return self._frozen_list_type.note_frozen_list_type([note + absolute_interval for absolute_interval in self._absolute_intervals])

    def from_note(self, note: "NoteType") -> "NoteList":
        """Instantiate this pattern starting at `note`, returning a `NoteList` (increasing order)."""
        from solfege.value.note.set.note_list import NoteList
        return self._note_list_constructor()(self._from_note(note), ListOrder.INCREASING)

    # def relative_chromatic(self) -> ChromaticIntervalFrozenList:
    #     return self._frozen_list_type([interval.get_chromatic() for interval in self.relative_intervals()])

    # def relative_diatonic(self) -> DiatonicIntervalFrozenList:
    #     return self._frozen_list_type([interval.get_diatonic() for interval in self.relative_intervals()])

    # def absolute_chromatic(self) -> ChromaticIntervalFrozenList:
    #     return self._frozen_list_type([interval.get_chromatic() for interval in self.absolute_intervals()])

    # def absolute_diatonic(self) -> DiatonicIntervalFrozenList:
    #     return self._frozen_list_type([interval.get_diatonic() for interval in self.absolute_intervals()])
    
    def __repr__(self):
        """Evaluable repr, e.g. `IntervalList.make_absolute([(0, 0), (4, 2), (7, 4)])`."""
        l = [f"{self.__class__.__name__}.make_absolute(["""]
        l.append(", ".join(self.interval_repr(chromatic_interval) for chromatic_interval in self.absolute_intervals()))
        if self.increasing is not True:
            l.append(f", {str(self.increasing)}")
        l.append("])")
        return "".join(l)
    
    @staticmethod
    @abstractmethod
    def interval_repr(interval: IntervalType) -> str:
        """How to display the interval in make."""
        ...


    def in_base_octave(self) -> Self:
        """Return the same pattern with every interval folded into the base octave, deduplicated
        and sorted."""
        intervals_in_base_octave = sorted_unique(interval.in_base_octave() for interval in self._absolute_intervals)
        return self.__class__.make(intervals_in_base_octave)

    def is_in_base_octave(self, accepting_octave: bool = False):
        """Whether every interval in the list is already in the base octave (see
        `Abstract.is_in_base_octave`)."""
        for interval in self._absolute_intervals:
            if not interval.is_in_base_octave(accepting_octave):
                return False
        return True
    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `increasing` to `True`."""
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["increasing"] = True
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Coerce `_absolute_intervals` into `cls._frozen_list_type` if it isn't already one."""
        def clean_absolute_intervals(intervals):
            """Wrap a plain iterable of intervals into `cls._frozen_list_type`, leaving an
            already-correct instance untouched."""
            if not isinstance(intervals, cls._frozen_list_type):
                return cls._frozen_list_type(intervals)
            return intervals
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_absolute_intervals", clean_absolute_intervals)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "increasing")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        """Validate that the list starts with the unison, holds only `interval_type` instances, and
        is strictly monotonic in the direction given by `increasing`."""
        assert self._absolute_intervals[0] == self.interval_type.unison()
        assert_typing(self._absolute_intervals, self._frozen_list_type)
        assert_iterable_typing(self._absolute_intervals, self.interval_type)
        for first, second in pairwise(self._absolute_intervals):
            if self.increasing:
                assert first < second, self._absolute_intervals
            else:
                assert first > second, self._absolute_intervals
        super().__post_init__()

IntervalListPatternType = TypeVar("IntervalListPatternType", bound=AbstractIntervalListPattern)
"""Type variable bound to `AbstractIntervalListPattern`, used to parametrize generic classes over the
concrete interval-list-pattern type."""

