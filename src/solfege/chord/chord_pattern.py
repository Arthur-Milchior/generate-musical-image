from dataclasses import dataclass
from itertools import pairwise
from typing import ClassVar, Dict, Iterable, Optional

from solfege.interval.interval import Interval
from solfege.interval.set.list import ChromaticIntervalList, IntervalList
from solfege.solfege_pattern import SolfegePattern
from solfege.interval.chromatic_interval import ChromaticInterval
from utils.frozenlist import FrozenList
from utils.util import assert_all_same_class

def chord_to_arpeggio_name(name: str):
    if "chord" in name:
        return name.replace("chord", "arpeggio")
    if "triad" in name:
        return name.replace("triad", "arpeggio")
    else:
        return f"{name} arpeggio"

@dataclass(frozen=True)
class ChordPattern(SolfegePattern):
    """A pattern describing a chord."""

    "Associate to a set of interval the chord it represents."
    set_of_interval_to_pattern: ClassVar[Dict[IntervalList, "ChordPattern"]] = dict()
    "associate to a set of chromatic interval the chord it represents."
    set_of_chromatic_interval_to_pattern: ClassVar[Dict[ChromaticIntervalList, "ChordPattern"]] = dict()

    """Whether the 5th is optional"""
    optional_fifth: bool = False
    record: bool = False

    def __post_init__(self):
        """A sequence of interval between the tonic and the other note of this chord.
        
        Unison is not present in the param. Other intervals are presented as a pair of Chromatic, Diatonic
        """
        super().__post_init__()
        intervals_lists = [IntervalList(self._absolute_intervals, increasing=self.increasing)]
        if self.optional_fifth:
            intervals_without_fifth_list = IntervalList(
                FrozenList([interval for interval in self._absolute_intervals if interval.get_diatonic().value != 4]), increasing=self.increasing)
            intervals_lists.append(intervals_without_fifth_list)
        for interval_list in intervals_lists:
            self.set_of_interval_to_pattern[interval_list] = self
            self.set_of_chromatic_interval_to_pattern[interval_list.get_chromatic()] = self
        
    @classmethod
    def get_pattern_from_interval(cls, intervals: IntervalList):
        """Given a set of interval, return the object having this set of intervals."""
        return cls.set_of_interval_to_pattern.get(intervals)

    @classmethod
    def get_pattern_from_chromatic_interval(cls, intervals: ChromaticIntervalList) -> Optional["ChordPattern"]:
        """Given a set of interval, return the object having this set of intervals."""
        return cls.set_of_chromatic_interval_to_pattern.get(intervals)

    def to_arpeggio_pattern(self):
        from solfege.scale.scale_pattern import ScalePattern
        absolute_intervals = self._absolute_intervals + [Interval.one_octave()]
        assert self.increasing
        return ScalePattern(_absolute_intervals=absolute_intervals,
                            names=[chord_to_arpeggio_name(name) for name in self.names],
                            notation = self.notation,
                            interval_for_signature=self.interval_for_signature, record=True, increasing=self.increasing)
