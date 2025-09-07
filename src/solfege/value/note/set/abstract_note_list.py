

from dataclasses import dataclass
from enum import Enum
from typing import Callable, ClassVar, Dict, Generic, List, Type

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.set.interval_list import AbstractIntervalList, IntervalListType
from solfege.value.note.abstract_note import AbstractNote, NoteType
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.util import assert_decreasing, assert_increasing, assert_iterable_typing, assert_typing

class ListOrder(Enum):
    INCREASING = "INCREASING"
    DECREASING = "DECREASING"
    NOT = "NOT"

@dataclass(frozen=True, unsafe_hash=True)
class AbstractNoteList(Generic[NoteType, IntervalType, IntervalListType], DataClassWithDefaultArgument):
    interval_list_type: ClassVar[Type[AbstractIntervalList]]
    note_type: ClassVar[Type[AbstractNote]]
    notes: FrozenList[NoteType]
    list_order: ListOrder

    def interval_list_from_min_note(self) -> IntervalListType:
        assert self.list_order == ListOrder.INCREASING
        min_note = self.notes[0]
        return self.interval_list_type.make(note-min_note for note in self.notes)

    @classmethod
    def _default_arguments_for_constructor(cls):
        kwargs = super()._default_arguments_for_constructor()
        kwargs["list_order"] = ListOrder.INCREASING
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_note(notes):
            return FrozenList(cls.note_type.make_single_argument(note) for note in notes)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "notes", clean_note)
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        assert_typing(self.notes, FrozenList)
        assert_iterable_typing(self.notes, self.note_type)
        if self.list_order == ListOrder.INCREASING:
            assert_increasing(self)
        elif self.list_order == ListOrder.DECREASING:
            assert_decreasing(self)
        super().__post_init__()

    def __iter__(self):
        return iter (self.notes)
    
    def __len__(self):
        return len(self.notes)