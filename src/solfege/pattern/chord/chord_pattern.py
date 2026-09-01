from dataclasses import dataclass, field
from itertools import pairwise
from typing import Callable, ClassVar, Dict, List, Optional, Type

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import IntervalList
from solfege.pattern.solfege_pattern import SolfegePattern
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_all_same_class, assert_typing

def chord_to_arpeggio_name(name: str):
    if "chord" in name:
        return name.replace("chord", "arpeggio")
    if "triad" in name:
        return name.replace("triad", "arpeggio")
    else:
        return f"{name} arpeggio"

@dataclass(frozen=True, unsafe_hash=True)
class ChordPattern(SolfegePattern, DataClassWithDefaultArgument):
    """A pattern describing a chord.
    
    Ordered according to the name."""

    """See SolfegePattern"""
    name_to_pattern: ClassVar[Dict[str, "ChordPattern"]] = dict()
    all_patterns: ClassVar[List['ChordPattern']] = list()

    _record_keeper: ClassVar[List]

    _full_interval_list: IntervalList
    """Whether the 5th is optional"""
    optional_fifth: bool

    _is_chord_pattern: bool = True


    @classmethod
    def _new_record_keeper(cls):
        from solfege.pattern.chord.interval_list_to_chord_pattern import IntervalListToChordPattern
        return IntervalListToChordPattern.make()

    def _index_of_fifth(self):
        index = None
        for i in range(len(self._full_interval_list)):
            if self._full_interval_list.absolute_intervals()[i]._diatonic.value == 4:
                assert index is None
                index = i
        assert index is not None
        return index
    
    def intervals_with_all_notes(self):
        return self._full_interval_list

    def intervals_without_fifth(self):
        assert self.optional_fifth
        index_of_fifth = self._index_of_fifth()
        full_intervals = self.intervals_with_all_notes().absolute_intervals()
        absolute_without_fifth = full_intervals[:index_of_fifth] + full_intervals[index_of_fifth+1:]
        return IntervalList.make_absolute(absolute_intervals=absolute_without_fifth)

    def to_arpeggio_pattern(self):
        from solfege.pattern.scale.scale_pattern import ScalePattern
        absolute_intervals = self._full_interval_list.absolute_intervals() + [Interval.one_octave()]
        return ScalePattern.make(_absolute_intervals=absolute_intervals,
                            names=[chord_to_arpeggio_name(name) for name in self.names],
                            notation = self.notation,
                            interval_for_signature=self.interval_for_signature, record=True, increasing=True, _is_chord_pattern=True)

    def interval_list_of_inversion(self, inversion_number, omit_fifth:bool=False) -> Optional[IntervalList]:
        assert 0<= inversion_number<len(self._full_interval_list)
        new_lower: Interval = self._full_interval_list.absolute_intervals()[inversion_number]
        absolute_intervals = [(interval - new_lower).add_octave(1 if index < inversion_number else 0) for index, interval in enumerate(self._full_interval_list.absolute_intervals())]
        absolute_intervals = absolute_intervals[inversion_number:] + absolute_intervals[:inversion_number]
        if omit_fifth:
            assert self.optional_fifth
            new_index_of_fifth = (self._index_of_fifth() - inversion_number) % len(absolute_intervals)
            if new_index_of_fifth == 0: # don't remove the lowest note of the inversion
                return None
            absolute_intervals.pop(new_index_of_fifth)
        inversion_interval_list = IntervalList.make_absolute(absolute_intervals, increasing=True)
        return inversion_interval_list

    def inversion(self, inversion_number, record=False):
        from solfege.pattern.inversion.inversion_pattern import InversionPattern
        new_lower: Interval = self._full_interval_list.absolute_intervals()[inversion_number]
        return InversionPattern.make(inversion=inversion_number, base=self, record=record, tonic_minus_lowest_note=new_lower)
    
    def inversions(self, record=False):
        l = []
        for inversion_number in range(len(self._full_interval_list.absolute_intervals())):
            l.append(self.inversion(inversion_number, record=record))
        return l 

    def __lt__(self, other: "ChordPattern"):
        return self.first_of_the_names() < other.first_of_the_names()

    def get_interval_lists(self) -> List[IntervalList]:
        il = self.intervals_with_all_notes()
        assert_typing(il, IntervalList)
        l = [il]
        if self.optional_fifth:
            il = self.intervals_without_fifth()
            assert_typing(il, IntervalList)
            l.append(il)
        return l
    
    # pragma mark - PatternWithIntervalLists
    
    @classmethod
    def _get_instantiation_type(cls) -> Type["Chord"]:
        from solfege.pattern_instantiation.chord.chord import Chord
        return Chord


    # pragma mark - DataClassWithDefaultArgument
 
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default_dict = super()._default_arguments_for_constructor(args, kwargs)
        default_dict["optional_fifth"] = False
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_full_interval_list(l):
            if isinstance(l, IntervalList):
                return l
            else:
                return IntervalList.make_absolute(l)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_full_interval_list", clean_full_interval_list)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "optional_fifth")
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        """A sequence of interval between the tonic and the other note of this chord.
        
        Unison is not present in the param. Other intervals are presented as a pair of Chromatic, Diatonic
        """
        assert_typing(self._full_interval_list, IntervalList)
        super().__post_init__()
        if not self.record:
            return
        
        self.inversions(record=self.record)