from dataclasses import dataclass
from itertools import pairwise
from typing import Callable, ClassVar, Dict, Generic, Iterable, List, Self, Tuple, Type, TypeVar, Union

from solfege.list_order import ListOrder
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.diatonic_interval import DiatonicInterval, DiatonicIntervalFrozenList
from solfege.value.interval.interval import Interval, IntervalFrozenList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.util import assert_iterable_typing, assert_typing, sorted_unique

@dataclass(frozen=True, unsafe_hash=True)
class AbstractIntervalListPattern(DataClassWithDefaultArgument, Generic[IntervalType]):
    interval_type: ClassVar[Type[AbstractInterval]]
    """The list of intervals, all relative to a common starting note."""
    _absolute_intervals: FrozenList[IntervalType]
    _frozen_list_type: ClassVar[Type[FrozenList[IntervalType]]]
    increasing: bool

    @classmethod
    def make_absolute(cls, absolute_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]], *args, add_implicit_zero: bool = True, **kwargs):
        absolute_intervals = [cls.interval_type.make_single_argument(absolute_interval) for absolute_interval in absolute_intervals]
        assert_iterable_typing(absolute_intervals, cls.interval_type)
        first_interval = absolute_intervals[0] if absolute_intervals else None
        unison = cls.interval_type.unison()
        if first_interval != unison and add_implicit_zero:
            absolute_intervals = [unison] + absolute_intervals
        return cls.make(*args, _absolute_intervals=cls._frozen_list_type(absolute_intervals), **kwargs)

    @classmethod
    def make_relative(cls, relative_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]],  *args,  **kwargs):
        unison = cls.interval_type.unison()
        absolute_intervals = [unison]
        for relative_interval in relative_intervals:
            relative_interval = cls.interval_type.make_single_argument(relative_interval)
            absolute_intervals.append(absolute_intervals[-1] + relative_interval)
        return cls.make(*args, _absolute_intervals=cls._frozen_list_type(absolute_intervals), **kwargs)

    def absolute_intervals(self) -> FrozenList[IntervalType]:
        return self._absolute_intervals

    def relative_intervals(self, assume_implicit_zero=True) -> FrozenList[IntervalType]:
        """Generator of the difference of intervals"""
        unison = self.interval_type.unison()
        assert self._absolute_intervals[0] == unison
        return self._frozen_list_type([higher - lower for lower, higher in pairwise(self._absolute_intervals)])

    @classmethod
    def _note_list_constructor(cls) -> Callable[["NoteType"], "AbstractNoteList"]:
        return NotImplemented

    def _from_note(self, note: "NoteType") -> FrozenList["NoteType"]:
        return self._frozen_list_type.note_frozen_list_type([note + absolute_interval for absolute_interval in self._absolute_intervals])
    
    def from_note(self, note: "NoteType") -> "NoteList":
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
        l = [f"{self.__class__.__name__}.make_absolute(["""]
        l.append(", ".join(self.interval_repr(chromatic_interval) for chromatic_interval in self.absolute_intervals()))
        if self.increasing is not True:
            l.append(f", {str(self.increasing)}")
        l.append("])")
        return "".join(l)
    
    @staticmethod
    def interval_repr(interval: IntervalType) -> str:
        "How to display the interval in make."
        return NotImplemented
    
    def in_base_octave(self) -> Self:
        intervals_in_base_octave = sorted_unique(interval.in_base_octave() for interval in self._absolute_intervals)
        return self.__class__.make(intervals_in_base_octave)
    
    def is_in_base_octave(self, accepting_octave: bool = False):
        for interval in self._absolute_intervals:
            if not interval.is_in_base_octave(accepting_octave):
                return False
        return True
    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["increasing"] = True
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_absolute_intervals(intervals):
            if not isinstance(intervals, cls._frozen_list_type):
                return cls._frozen_list_type(intervals)
            return intervals
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_absolute_intervals", clean_absolute_intervals)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "increasing")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert self._absolute_intervals[0] == self.interval_type.unison()
        assert_typing(self._absolute_intervals, self._frozen_list_type)
        assert_iterable_typing(self._absolute_intervals, self.interval_type)
        for first, second in pairwise(self._absolute_intervals):
            if self.increasing:
                assert first < second, self._absolute_intervals
            else:
                assert first > second, self._absolute_intervals
        super().__post_init__()

    
IntervalListType = TypeVar("IntervalListType", bound=AbstractIntervalListPattern)

@dataclass(frozen=True, unsafe_hash=True, repr=False)
class ChromaticIntervalListPattern(AbstractIntervalListPattern[ChromaticInterval]):
    interval_type: ClassVar[Type[ChromaticInterval]] = ChromaticInterval
    note_list_type: ClassVar[Type]
    _frozen_list_type: ClassVar[Type] = ChromaticIntervalFrozenList

    @classmethod
    def _note_list_constructor(cls):
        from solfege.value.note.set.note_list import ChromaticNoteList
        return ChromaticNoteList
    
    @staticmethod
    def interval_repr(interval: ChromaticInterval) -> str:
        "How to display the interval in make."
        return str(interval.value)

@dataclass(frozen=True, unsafe_hash=True, repr=False)
class IntervalListPattern(AbstractIntervalListPattern[Interval]):
    interval_type: ClassVar[Type[Interval]] = Interval
    _frozen_list_type: ClassVar[Type] = IntervalFrozenList

    @classmethod
    def _note_list_constructor(cls):
        from solfege.value.note.set.note_list import NoteList
        return NoteList
    
    @staticmethod
    def interval_repr(interval: Interval) -> str:
        "How to display the interval in make."
        return f"""({interval.chromatic.value}, {interval.diatonic.value})"""

    def get_chromatic_interval_list(self) -> ChromaticIntervalListPattern:
        chromatic_interval_list = ChromaticIntervalListPattern.make_absolute([interval.get_chromatic() for interval in self._absolute_intervals], increasing=self.increasing)
        assert_typing(chromatic_interval_list, ChromaticIntervalListPattern)
        return chromatic_interval_list

    def get_interval_list(self) -> "IntervalListPattern":
        return IntervalListPattern(self._absolute_intervals, self.increasing)
    

class IntervalListFrozenList(FrozenList[IntervalListPattern]):
    type = IntervalListPattern