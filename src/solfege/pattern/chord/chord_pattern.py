from dataclasses import dataclass, field
from itertools import pairwise
from typing import Callable, ClassVar, Dict, List, Type

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from solfege.pattern.solfege_pattern import SolfegePattern
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
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

    """Whether the 5th is optional"""
    optional_fifth: bool
    inversions: List["InversionPattern"] = field(hash=False, compare=False, default_factory=list, repr=False)


    @classmethod
    def _new_record_keeper(cls):
        from solfege.pattern.chord.interval_list_to_chord_pattern import IntervalListToChordPattern
        return IntervalListToChordPattern.make()
   

    def _index_of_fifth(self):
        index = None
        for i in range(len(self._absolute_intervals)):
            if self._absolute_intervals[i].diatonic.value == 4:
                assert index is None
                index = i
        assert index is not None
        return index
    
    def intervals_without_fifth(self):
        assert self.optional_fifth
        index_of_fifth = self._index_of_fifth()
        absolute_without_fifth = self._absolute_intervals[:index_of_fifth] + self._absolute_intervals[index_of_fifth+1:]
        return IntervalListPattern.make_absolute(absolute_without_fifth)

    def to_arpeggio_pattern(self):
        from solfege.pattern.scale.scale_pattern import ScalePattern
        absolute_intervals = self._absolute_intervals + [Interval.one_octave()]
        assert self.increasing
        return ScalePattern.make(_absolute_intervals=absolute_intervals,
                            names=[chord_to_arpeggio_name(name) for name in self.names],
                            notation = self.notation,
                            interval_for_signature=self.interval_for_signature, record=True, increasing=self.increasing)

    def inversion(self, inversion_number, omit_fifth:bool=False, record=False):
        from solfege.pattern.inversion.inversion_pattern import InversionPattern
        assert 0<= inversion_number<len(self._absolute_intervals)
        assert self.increasing
        new_lower: Interval = self._absolute_intervals[inversion_number]
        absolute_intervals = [(interval - new_lower).add_octave(1 if index < inversion_number else 0) for index, interval in enumerate(self._absolute_intervals)]
        absolute_intervals = absolute_intervals[inversion_number:] + absolute_intervals[:inversion_number]
        if omit_fifth:
            assert self.optional_fifth
            new_index_of_fifth = (self._index_of_fifth() - inversion_number) % len(absolute_intervals)
            assert new_index_of_fifth > 0 # don't remove the lowest note of the inversion
            absolute_intervals.pop(new_index_of_fifth)
        inversion_interval_list = IntervalListPattern.make_absolute(absolute_intervals, increasing=self.increasing)
        return InversionPattern.make(inversion=inversion_number, interval_list=inversion_interval_list, base=self, fifth_omitted = omit_fifth, record=record, interval_in_base_corresponding_to_interval_0_in_inversion=new_lower)
    
    def compute_all_inversions(self, record=False):
        l = []
        for inversion_number in range(len(self._absolute_intervals)):
            l.append(self.inversion(inversion_number, record=record, omit_fifth=False))
            if self.optional_fifth and self._index_of_fifth() != inversion_number:
                l.append(self.inversion(inversion_number, record=record, omit_fifth=True))
        return l 

    def __lt__(self, other: "ChordPattern"):
        return self.first_of_the_names() < other.first_of_the_names()
    
    def interval_lists(self) -> List[IntervalListPattern]:
        l = [self.get_interval_list()]
        if self.optional_fifth:
            l.append(self.intervals_without_fifth())
        return l
    
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
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "optional_fifth")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "inversions")
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        """A sequence of interval between the tonic and the other note of this chord.
        
        Unison is not present in the param. Other intervals are presented as a pair of Chromatic, Diatonic
        """
        super().__post_init__()
        if not self.record:
            return
        assert self.increasing
        self.inversions.extend(self.compute_all_inversions(record=self.record))