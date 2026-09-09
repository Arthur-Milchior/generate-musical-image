from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Generic, Self, TypeVar
from solfege.list_order import ListOrder
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.set.abstract_interval_list_pattern import AbstractIntervalListPattern
from solfege.value.key.key import Key
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.set.abstract_note_list import AbstractNoteList
from solfege.value.note.set.note_list import NoteList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.easyness import KeyType
from utils.frozenlist import FrozenList
from solfege.pattern.pattern_with_interval_lists import PatternType, PatternWithIntervalLists
from utils.util import T, assert_typing


NoteFrozenListType= TypeVar("NoteFrozenListType", bound = FrozenList)
IntervalFrozenListType= TypeVar("IntervalFrozenListType", bound = FrozenList)

@dataclass(frozen=True, eq=True)
class AbstractPatternInstantiation(DataClassWithDefaultArgument, ABC, Generic[PatternType, NoteType, IntervalType, KeyType]):
    """
    A data structure containing a `pattern` and the `lowest_note`. This represents the pattern starting at this note.
    """
    pattern: PatternType
    """The (still note-less) pattern being instantiated, e.g. a `ChordPattern`/`ScalePattern`/`InversionPattern`."""

    lowest_note: NoteType
    """The concrete note the pattern is anchored to. Must be in the base octave (see `__post_init__`); this is
    what turns an abstract shape into an actual, playable set of notes."""

    pattern_type: ClassVar[PatternWithIntervalLists]
    """The `PatternWithIntervalLists` subclass `pattern` is expected to be an instance of."""

    note_type: ClassVar[AbstractNote]
    """The `AbstractNote` subclass `lowest_note` is expected to be an instance of."""

    interval_type: ClassVar[AbstractInterval]
    """The interval class used by `get_intervals()`/`get_absolute_intervals()` for this instantiation kind."""

    interval_list_type: ClassVar[FrozenList[IntervalType]]
    """The frozen-list-of-intervals class used to hold `get_absolute_intervals()`'s result."""

    note_list_type: ClassVar[AbstractNoteList[NoteType, IntervalType, PatternWithIntervalLists]]
    """The frozen-list-of-notes class returned by `get_notes()`."""

    def __post_init__(self):
        """Validate that `lowest_note`/`pattern` have the expected types and that `lowest_note` sits in the
        base octave (an instantiation is always anchored on the base-octave lowest note; `add_octave` is used
        afterwards to shift the whole thing)."""
        assert_typing(self.lowest_note, self.note_type)
        assert_typing(self.pattern, self.pattern_type)
        assert self.lowest_note.is_in_base_octave(accepting_octave=False)
        super().__post_init__()

    def get_absolute_intervals(self) -> FrozenList[IntervalType]:
        """`get_intervals()`, as absolute (from-the-root) intervals rather than relative steps."""
        return self.get_intervals().absolute_intervals()

    def get_notes(self) -> AbstractNoteList[NoteType, IntervalType, PatternWithIntervalLists]:
        """The concrete, increasing list of notes this instantiation represents: `lowest_note` plus each of
        `get_absolute_intervals()`."""
        l =  []
        for interval in self.get_absolute_intervals():
            l.append(self.lowest_note + interval)
        return self.note_list_type.make(l, list_order=ListOrder.INCREASING)

    def key(self)->Key:
        """The key. Assuming notes are not diatonic"""
        return Key.from_note(self.lowest_note + self.pattern.interval_for_signature)

    def all_blacks(self):
        """Whether all notes are black on a piano. assert if note is diatonic."""
        return all(note.is_black_key_on_piano() for note in self.get_notes())

    def add_octave(self, nb_octave: int) -> Self:
        """A copy of this instantiation with `lowest_note` shifted up (or down, if negative) by `nb_octave`
        octaves; the pattern itself is unchanged."""
        return dataclasses.replace(self, lowest_note= self.lowest_note.add_octave(nb_octave))

    # must be implemented by subclasses

    @abstractmethod
    def get_intervals(self) -> AbstractIntervalListPattern[IntervalType]:
        """The pattern's intervals (relative steps), as seen from `lowest_note`."""
        ...

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> KeyType:
        """Delegates to the underlying pattern's own `easy_key()` (defined only if the pattern defines it)."""
        # Defined only if the pattern defines it.
        return self.pattern.easy_key()