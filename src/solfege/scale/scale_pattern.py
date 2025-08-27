from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Generic, Self, Union, Tuple, Optional

from solfege.key.key import *
from solfege.scale.scale import Scale
from solfege.interval.abstract_interval import IntervalType
from solfege.note.note import Note
from solfege.note.abstract_note import NoteType
from solfege.interval.interval_pattern import intervals_up_to_octave

"""Contains a class to represent a scale.

Also contains all scales from wikipedia, which can be done using the 12 note from chromatic scales."""

import sys

from solfege.interval.interval import Interval, octave
from solfege.solfege_pattern import SolfegePattern


@dataclass(frozen=True)
class ScalePattern(SolfegePattern):
    """The descending pattern if different from the ascending one. Mostly used for minor melodic. It's stored in an ascending way.
    If it's none, the descending is self"""
    descending: Optional[Self] = None
    """If True, add a warning if the result is not a perfect octave"""
    suppress_warning: bool = field(compare = False, default=False)

    def __post_init__(self):
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
