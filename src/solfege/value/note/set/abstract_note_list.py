

from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import Callable, ClassVar, Dict, Generic, List, Self, Type

from solfege.list_order import ListOrder, reverse_list_order
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.set.abstract_interval_list_pattern import IntervalListPatternType
from solfege.value.interval.set.interval_list import AbstractIntervalListPattern
from solfege.value.note.abstract_note import AbstractNote, NoteType
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList
from utils.util import assert_decreasing, assert_increasing, assert_iterable_typing, assert_typing


@dataclass(frozen=True, unsafe_hash=True)
class AbstractNoteList(DataClassWithDefaultArgument, Generic[NoteType, IntervalType, IntervalListPatternType]):
    """Base for an ordered list of notes (chromatic-only or chromatic+diatonic), such as the
    notes making up a chord or scale. Subclasses fix the concrete note/interval/interval-list-
    pattern types via the `ClassVar`s below."""
    interval_list_type: ClassVar[Type[AbstractIntervalListPattern]]
    """The interval-list-pattern class produced by `interval_list_from_min_note`."""
    note_type: ClassVar[Type[AbstractNote]]
    """The concrete note class this list holds."""
    _frozen_list_type: ClassVar[Type[FrozenList[AbstractNote]]]
    """The `FrozenList` subclass used to store `notes`."""
    notes: FrozenList[NoteType]
    """The notes, in `list_order`."""
    list_order: ListOrder
    """Whether `notes` is sorted increasing, decreasing, or unsorted (`ListOrder.NOT`)."""

    def interval_list_from_min_note(self) -> IntervalListPatternType:
        """Return the pattern of intervals from the lowest note to each note in the list.
        Requires `list_order` to be `INCREASING` (so the first note is the lowest)."""
        assert self.list_order == ListOrder.INCREASING
        min_note = self.notes[0]
        return self.interval_list_type.make(note-min_note for note in self.notes)

    def __iter__(self):
        """Iterate over the notes in `list_order`."""
        return iter (self.notes)

    def __len__(self):
        """Number of notes in the list."""
        return len(self.notes)

    def is_in_base_octave(self, accepting_octave: bool = False):
        """Whether every note in the list is in its base octave (see
        `AbstractNote.is_in_base_octave`)."""
        for note in self.notes:
            if not note.is_in_base_octave(accepting_octave):
                return False
        return True

    def all_blacks(self):
        """Whether every note in the list is a black key on the piano."""
        return all(note.is_black_key_on_piano() for note in self.notes)

    def __reversed__(self) -> Self:
        """Return the same notes in reverse order, with `list_order` flipped accordingly."""
        return dataclasses.replace(self, notes=reversed(self.notes), list_order=reverse_list_order(self.list_order))

    def add_octave(self, nb_octave) -> Self:
        """Return the list with every note shifted by `nb_octave` whole octaves."""
        return dataclasses.replace(self, notes = self.notes.map(lambda note: note.add_octave(nb_octave)))

    # pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """Default `list_order` to `INCREASING` when not supplied."""
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["list_order"] = ListOrder.INCREASING
        return default

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Coerce each element of the `notes` argument into `note_type` via
        `make_single_argument`, and wrap the result in `_frozen_list_type`."""
        def clean_note(notes):
            """Coerce each element of `notes` into `note_type` and collect the result into `_frozen_list_type`."""
            return cls._frozen_list_type(cls.note_type.make_single_argument(note) for note in notes)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "notes", clean_note)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        """Validate `notes`' container/element types and that it respects the declared
        `list_order`."""
        assert_typing(self.notes, self._frozen_list_type)
        assert_iterable_typing(self.notes, self.note_type)
        if self.list_order == ListOrder.INCREASING:
            assert_increasing(self)
        elif self.list_order == ListOrder.DECREASING:
            assert_decreasing(self)
        super().__post_init__()