from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional

from solfege.value.interval.set.interval_list import IntervalList
from solfege.pattern.scale.scale import Scale
from solfege.value.note.abstract_note import NoteType
from utils.util import assert_optional_typing

"""Contains a class to represent a scale.

Also contains all scales from wikipedia, which can be done using the 12 note from chromatic scales."""

import sys

from solfege.value.interval.interval import Interval, octave
from solfege.pattern.pattern import SolfegePattern


@dataclass(frozen=True)
class ScalePattern(SolfegePattern):
    """A pattern for one of the scale."""


    """See SolfegePattern"""
    name_to_pattern: ClassVar[Dict[str, "ScalePattern"]] = dict()
    all_patterns: ClassVar[List['ScalePattern']] = list()

    """The descending pattern if different from the ascending one. Mostly used for minor melodic. It's stored in an ascending way.
    If it's none, the descending is self"""
    descending: Optional["ScalePattern"] = None
    """If True, add a warning if the result is not a perfect octave"""
    suppress_warning: bool = field(compare = False, default=False)


    @classmethod
    def _new_record_keeper(cls):
        from solfege.pattern.scale.interval_list_to_scale_pattern import IntervalListToScalePattern
        return IntervalListToScalePattern.make()

    def __post_init__(self):
        assert_optional_typing(self.descending, ScalePattern)
        assert_optional_typing(self.suppress_warning, bool)
        super().__post_init__()
        if not self.suppress_warning:
            last_interval = self._absolute_intervals[-1]
            if last_interval != octave:
                assert f"Warning: scale {self.names[0]} has a last interval of {last_interval}"

    def __neg__(self):
        """The same pattern, reversed. Ignore the descending option"""
        return ScalePattern.make_relative(names=self.names, notation=self.notation, relative_intervals=[-interval for interval in reversed(list(self.relative_intervals()))],
                            interval_for_signature=self.interval_for_signature, suppress_warning=True, increasing = not self.increasing, descending=self.descending,
                            record=False)

    def from_note(self, tonic: NoteType, number_of_octaves=1,
                 add_an_extra_note: bool = False) -> Scale[NoteType]:
        """The note, starting at tonic, following this pattern for nb_octave.
        If nb_octave is negative, the generated scale is decreasing."""
        assert number_of_octaves != 0
        if number_of_octaves < 0:
            return (-self).from_note(tonic, -number_of_octaves, add_an_extra_note=add_an_extra_note)
        current_note = tonic
        notes = [tonic]
        relative_intervals = list(self.relative_intervals())
        for octave_number in range(number_of_octaves):
            for interval in relative_intervals:
                current_note += interval
                notes.append(current_note)
        if add_an_extra_note:
            notes.append(notes[-1] + relative_intervals[0])
        return Scale[NoteType](notes=notes, pattern=self, key = notes[0] + self.interval_for_signature)

    def __len__(self):
        return len(self.relative_intervals)

    def multiple_octaves(self, nb_octave: int):
        assert nb_octave >= 0
        return IntervalList.make_relative(self.relative_intervals()*nb_octave)