

from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import Callable, ClassVar, Dict, Generic, List, Self, Type

from solfege.list_order import ListOrder, reverse_list_order
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.set.abstract_interval_ilst_pattern import IntervalListPatternType
from solfege.value.interval.set.interval_list_pattern import AbstractIntervalListPattern
from solfege.value.note.abstract_note import AbstractNote, NoteType
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.util import assert_decreasing, assert_increasing, assert_iterable_typing, assert_typing


@dataclass(frozen=True, unsafe_hash=True)
class AbstractNoteList(DataClassWithDefaultArgument, Generic[NoteType, IntervalType, IntervalListPatternType]):
    interval_list_type: ClassVar[Type[AbstractIntervalListPattern]]
    note_type: ClassVar[Type[AbstractNote]]
    _frozen_list_type: ClassVar[Type[FrozenList[AbstractNote]]]
    notes: FrozenList[NoteType]
    list_order: ListOrder

    def interval_list_from_min_note(self) -> IntervalListPatternType:
        assert self.list_order == ListOrder.INCREASING
        min_note = self.notes[0]
        return self.interval_list_type.make(note-min_note for note in self.notes)

    def __iter__(self):
        return iter (self.notes)
    
    def __len__(self):
        return len(self.notes)
    
    def is_in_base_octave(self, accepting_octave: bool = False):
        for note in self.notes:
            if not note.is_in_base_octave(accepting_octave):
                return False
        return True

    def all_blacks(self):
        return all(note.is_black_key_on_piano() for note in self.notes)
    
    def __reversed__(self) -> Self:
        return dataclasses.replace(self, notes=reversed(self.notes), list_order=reverse_list_order(self.list_order))
    
    def add_octave(self, nb_octave) -> Self:
        return dataclasses.replace(self, notes = self.notes.map(lambda note: note.add_octave(nb_octave)))

    # pragma mark - DataClassWithDefaultArgument
    
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["list_order"] = ListOrder.INCREASING
        return default

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_note(notes):
            return cls._frozen_list_type(cls.note_type.make_single_argument(note) for note in notes)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "notes", clean_note)
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        assert_typing(self.notes, self._frozen_list_type)
        assert_iterable_typing(self.notes, self.note_type)
        if self.list_order == ListOrder.INCREASING:
            assert_increasing(self)
        elif self.list_order == ListOrder.DECREASING:
            assert_decreasing(self)
        super().__post_init__()