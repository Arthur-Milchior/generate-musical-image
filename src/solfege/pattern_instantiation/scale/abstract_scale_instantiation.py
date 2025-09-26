
from dataclasses import dataclass
from typing import ClassVar, Generic

from solfege.list_order import ListOrder
from solfege.pattern.pattern_with_interval_list import PatternWithIntervalList
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.key.key import Key
from solfege.value.note.abstract_note import NoteType
from solfege.value.note.set.abstract_note_list import AbstractNoteList


@dataclass(frozen=True)
class AbstractScale(AbstractPatternInstantiation[ScalePattern, NoteType, IntervalType, int],  Generic[NoteType, IntervalType]): 
    pattern_type: ClassVar[PatternWithIntervalList] = ScalePattern

    def get_key(self) -> Key:
        return Key.from_note(self.lowest_note + self.pattern.interval_for_signature)
    
    def get_notes(self,
                  number_of_octaves: int = 1,
                  add_an_extra_note: bool = False) -> AbstractNoteList[NoteType, IntervalType, ScalePattern]:
        """The note, starting at self.lowest_note, following this pattern for nb_octave.
        If nb_octave is negative, the generated scale is decreasing."""
        assert number_of_octaves != 0
        relative_intervals = self.pattern.relative_intervals()
        if number_of_octaves < 0:
            relative_intervals = relative_intervals.map(lambda interval: - interval)
            relative_intervals = reversed(relative_intervals)
        notes = [self.lowest_note]
        for octave_number in range(abs(number_of_octaves)):
            for interval in relative_intervals:
                notes.append(notes[-1] + interval)
        if add_an_extra_note:
            notes.append(notes[-1] + relative_intervals[0])
        return self.note_list_type.make(notes=notes, list_order=ListOrder.INCREASING if number_of_octaves > 0 else ListOrder.DECREASING)
