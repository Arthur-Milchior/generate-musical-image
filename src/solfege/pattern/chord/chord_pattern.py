from dataclasses import dataclass, field
from itertools import pairwise
from typing import ClassVar, Dict, Iterable, List, Optional

from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.list import ChromaticIntervalList, DataClassWithDefaultArgument, IntervalList
from solfege.pattern.pattern import SolfegePattern
from solfege.value.interval.chromatic_interval import ChromaticInterval
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

    "Associate to a set of interval the chord it represents."
    set_of_interval_to_pattern: ClassVar[Dict[IntervalList, "ChordPattern"]] = dict()
    "associate to a set of chromatic interval the chord it represents."
    set_of_chromatic_interval_to_pattern: ClassVar[Dict[ChromaticIntervalList, "ChordPattern"]] = dict()

    """Whether the 5th is optional"""
    optional_fifth: bool
    inversions: List["InversionPattern"] = field(hash=False, compare=False, default_factory=list)
    
    @classmethod
    def _default_arguments_for_constructor(cls):
        default_dict = super()._default_arguments_for_constructor()
        default_dict["optional_fifth"] = False
        return default_dict

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.maybe_arg_to_kwargs(args, kwargs, "optional_fifth")
        args, kwargs = cls.maybe_arg_to_kwargs(args, kwargs, "inversions")
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        return args, kwargs

    def _index_of_fifth(self):
        index = None
        for i in range(len(self._absolute_intervals)):
            if self._absolute_intervals[i].diatonic.value == 4:
                assert index is None
                index = i
        assert index is not None
        return index

    def __post_init__(self):
        """A sequence of interval between the tonic and the other note of this chord.
        
        Unison is not present in the param. Other intervals are presented as a pair of Chromatic, Diatonic
        """
        super().__post_init__()
        if not self.record:
            return
        assert self.increasing
        self.inversions.extend(self.compute_all_inversions(record=self.record))
        if not self.optional_fifth:
            return
    
    def intervals_without_fifth(self):
        assert self.optional_fifth
        index_of_fifth = self._index_of_fifth()
        absolute_without_fifth = self._absolute_intervals[:index_of_fifth] + self._absolute_intervals[index_of_fifth+1:]
        return IntervalList.make_absolute(absolute_without_fifth)

    def to_arpeggio_pattern(self):
        from solfege.pattern.scale.scale_pattern import ScalePattern
        absolute_intervals = self._absolute_intervals + [Interval.one_octave()]
        assert self.increasing
        return ScalePattern.make(_absolute_intervals=absolute_intervals,
                            names=[chord_to_arpeggio_name(name) for name in self.names],
                            notation = self.notation,
                            interval_for_signature=self.interval_for_signature, record=True, increasing=self.increasing)

    def inversion(self, inversion_number, omit_fifth:bool=False, record=False):
        from solfege.pattern.chord.inversion_pattern import InversionPattern
        assert 0<= inversion_number<len(self._absolute_intervals)
        assert self.increasing
        new_lower = self._absolute_intervals[inversion_number]
        absolute_intervals = [(interval - new_lower).add_octave(1 if index < inversion_number else 0) for index, interval in enumerate(self._absolute_intervals)]
        absolute_intervals = absolute_intervals[inversion_number:] + absolute_intervals[:inversion_number]
        if omit_fifth:
            assert self.optional_fifth
            new_index_of_fifth = (self._index_of_fifth() - inversion_number) % len(absolute_intervals)
            assert new_index_of_fifth > 0 # don't remove the lowest note of the inversion
            absolute_intervals.pop(new_index_of_fifth)
        inversion_interval_list = IntervalList.make_absolute(absolute_intervals, increasing=self.increasing)
        return InversionPattern.make(inversion=inversion_number, interval_list=inversion_interval_list, base=self, fifth_omitted = omit_fifth, record=record)
    
    def compute_all_inversions(self, record=False):
        l = []
        for inversion_number in range(len(self._absolute_intervals)):
            l.append(self.inversion(inversion_number, record=record, omit_fifth=False))
            if self.optional_fifth and self._index_of_fifth() != inversion_number:
                l.append(self.inversion(inversion_number, record=record, omit_fifth=True))
        return l 

    def __lt__(self, other: "ChordPattern"):
        return self.first_of_the_names() < other.first_of_the_names()
    
    def interval_lists(self) -> List[IntervalList]:
        l = [self.get_interval_list()]
        if self.optional_fifth:
            l.append(self.intervals_without_fifth())
        return l
