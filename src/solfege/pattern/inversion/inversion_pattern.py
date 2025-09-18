

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Dict, Generic, List, Tuple, Type, TypeVar
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from solfege.value.note.note import Note
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing



@dataclass(frozen=True)
class InversionPattern(PatternWithIntervalList["IntervalListToIdenticalInversionPattern", Tuple[int, int]],
                       DataClassWithDefaultArgument):
    #pragma mark - Recordable
    _key_type: ClassVar[Type] = IntervalListPattern

    # public

    """Order is considering not inversion first. Then with fifth. Then base."""
    inversion: int
    interval_list: IntervalListPattern
    base: ChordPattern
    fifth_omitted: bool

    """For a scale whose lowest note is n, you get the position of the tonic with n+tonic_minus_lowest_note."""
    tonic_minus_lowest_note: Interval

    def get_tonic(self, lowest_note: Note):
        assert_typing(lowest_note, Note)
        return lowest_note - self.tonic_minus_lowest_note

    @classmethod
    def _new_record_keeper(cls):
        from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
        return IntervalListToInversionPattern.make()
    
    def get_interval_list(self) -> IntervalListPattern:
        iv = self.interval_list
        assert_typing(iv, IntervalListPattern, exact=True)
        return iv
    
    def names(self):
        names = []
        for chord_name in self.base.names:
            if self.inversion == 0:
                suffix = ""
            elif self.inversion == 1:
                suffix = " first inversion"
            elif self.inversion == 2:
                suffix = " second inversion"
            elif self.inversion == 3:
                suffix = " third inversion"
            else:
                assert self.inversion < 10
                suffix = f" {self.inversion}th inversion"
            names.append(f"""{chord_name}{suffix}""")
        return names

    def notation(self):
        suffix = "" if self.inversion == 0 else f"/{self.inversion}"
        return f"""{self.base.notation}{suffix}"""
    
    def __lt__(self, other: "InversionPattern"):
        return (self.inversion, not self.fifth_omitted, self.base) < (other.inversion, not other.fifth_omitted, other.base)

    @classmethod
    def _get_instantiation_type(cls) -> Type["Inversion"]:
        from solfege.pattern_instantiation.inversion.inversion import Inversion
        return Inversion
    
    #pragma mark - ClassWithEasyness
    def easy_key(self) -> Tuple[int, int]:
        return (self.inversion, self.base.easy_key())


    # pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        number_of_notes = len(self.interval_list) + (1 if self.fifth_omitted else 0)
        assert self.inversion < number_of_notes
        absolute_intervals = self.interval_list.absolute_intervals()
        assert absolute_intervals[0] == Interval.make(0, 0)
        for interval in absolute_intervals:
            assert interval.is_in_base_octave(accepting_octave=False)
        super().__post_init__()

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["fifth_omitted"] = False
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        cls.arg_to_kwargs(args, kwargs, "inversion")
        def clean_absolute_intervals(intervals):
            if not isinstance(intervals, IntervalListPattern):
                return IntervalListPattern.make_absolute(intervals)
            return intervals
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "interval_list", clean_absolute_intervals)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "base")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "fifth_omitted")
        return super()._clean_arguments_for_constructor(args, kwargs)