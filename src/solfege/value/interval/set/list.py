from dataclasses import dataclass
from itertools import pairwise
from typing import Callable, ClassVar, Generic, Iterable, List, Optional, Self, Tuple, Type, Union

from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval import Interval
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from solfege.value.chromatic import ChromaticGetter
from solfege.value.key.key import *
from utils.frozenlist import FrozenList
from utils.util import assert_typing

@dataclass(frozen=True)
class DataClassWithDefaultArgument:
    """Must always be added as last ancestor."""

    @classmethod
    def make(cls, *args, **kwargs) -> Self:
        args, kwargs = cls._clean_arguments_for_constructor(args, kwargs)
        default_args = cls._default_arguments_for_constructor()
        default_args.update(kwargs)
        return cls(*args, **default_args)

    def __post_init__(self):
        hash(self) #check that hash can be computed
    
    @staticmethod
    def arg_to_kwargs(args, kwargs, name, clean: Callable = lambda x: x):
        """If there is args, the first value is assumed to be name, not in kwargs, and is added in kwargs.
        Otherwise check that name in `kwargs`.

        Also clean the value with `clean`.

        Value is moved from args to kwargs.
        """
        if args:
            assert name not in kwargs
            arg = args[0]
            args = args[1:]
        else:
            assert name in kwargs
            arg = kwargs[name]
        kwargs[name] = clean(arg)
        return (args, kwargs)
    
    @staticmethod
    def maybe_arg_to_kwargs(args, kwargs, name, clean: Callable = lambda x:x):
        """Clean the value associated to name, by default the first of args, if it exists. Otherwise do nothing."""
        if not args and name not in kwargs:
            return (args, kwargs)
        return DataClassWithDefaultArgument.arg_to_kwargs(args, kwargs, name, clean)

    @classmethod
    def _default_arguments_for_constructor(cls):
        """Returns the association from argument name to default argument value.
        Class inheriting must call super."""
        return dict()
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Ensure that any value is changed so that it gets the correct type. E.g. transform list in frozenlist
        and pair of int in interval.
        Class inheriting must call super."""
        return (args, kwargs)

@dataclass(frozen=True, unsafe_hash=True)
class AbstractIntervalList(Generic[IntervalType], DataClassWithDefaultArgument):
    interval_type: ClassVar[Type[AbstractInterval]]
    """The list of intervals, all relative to a common starting note."""
    _absolute_intervals: FrozenList[IntervalType]
    increasing: bool

    @classmethod
    def _default_arguments_for_constructor(cls):
        default_dict = super()._default_arguments_for_constructor()
        default_dict["increasing"] = True
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_absolute_intervals(intervals):
            if not isinstance(intervals, FrozenList):
                return FrozenList(intervals)
            return intervals
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_absolute_intervals", clean_absolute_intervals)
        args, kwargs = cls.maybe_arg_to_kwargs(args, kwargs, "increasing")
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert self._absolute_intervals[0] == self.interval_type.unison()
        assert_typing(self._absolute_intervals, FrozenList)
        for interval in self._absolute_intervals:
            assert_typing(interval, self.interval_type)
        for first, second in pairwise(self._absolute_intervals):
            if self.increasing:
                assert first < second
            else:
                assert first > second
        super().__post_init__()

    @classmethod
    def make_absolute(cls, absolute_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]], *args, add_implicit_zero: bool = True, **kwargs):
        absolute_intervals = [cls.interval_type.make_single_argument(absolute_interval) for absolute_interval in absolute_intervals]
        first_interval = absolute_intervals[0]
        unison = cls.interval_type.unison()
        if first_interval != unison and add_implicit_zero:
            absolute_intervals = [unison] + absolute_intervals
        return cls.make(_absolute_intervals=absolute_intervals, *args, **kwargs)

    @classmethod
    def make_relative(cls, relative_intervals: Iterable[Union[int, IntervalType, Tuple[int, int]]],  *args,  **kwargs):
        unison = cls.interval_type.unison()
        absolute_intervals = [unison]
        for relative_interval in relative_intervals:
            relative_interval = cls.interval_type.make_single_argument(relative_interval)
            absolute_intervals.append(absolute_intervals[-1] + relative_interval)
        return cls.make(*args, _absolute_intervals=absolute_intervals, **kwargs)

    def absolute_intervals(self) -> FrozenList[Interval]:
        return self._absolute_intervals

    def relative_intervals(self, assume_implicit_zero=True) -> FrozenList[Interval]:
        """Generator of the difference of intervals"""
        unison = self.interval_type.unison()
        assert self._absolute_intervals[0] == unison
        return FrozenList([higher - lower for lower, higher in pairwise(self._absolute_intervals)])

    def from_note(self, note: NoteType) -> FrozenList[NoteType]:
        return FrozenList([note + absolute_interval for absolute_interval in self._absolute_intervals])

    def relative_chromatic(self) -> FrozenList[ChromaticInterval]:
        return FrozenList([interval.get_chromatic() for interval in self.relative_intervals()])

    def relative_diatonic(self) -> FrozenList[DiatonicInterval]:
        return FrozenList([interval.get_diatonic() for interval in self.relative_intervals()])

    def absolute_chromatic(self) -> FrozenList[ChromaticInterval]:
        return FrozenList([interval.get_chromatic() for interval in self.absolute_intervals()])

    def absolute_diatonic(self) -> FrozenList[DiatonicInterval]:
        return FrozenList([interval.get_diatonic() for interval in self.absolute_intervals()])

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIntervalList(AbstractIntervalList[ChromaticInterval]):
    interval_type: ClassVar[Type[ChromaticInterval]] = ChromaticInterval

@dataclass(frozen=True, unsafe_hash=True)
class IntervalList(AbstractIntervalList[Interval]):
    interval_type: ClassVar[Type[Interval]] = Interval

    def get_chromatic(self) -> ChromaticIntervalList:
        absolute_chromatic = self.absolute_chromatic()
        return ChromaticIntervalList.make_absolute([interval.get_chromatic() for interval in absolute_chromatic], increasing=self.increasing)

    def get_interval_list(self) -> "IntervalList":
        return IntervalList(self._absolute_intervals, self.increasing)