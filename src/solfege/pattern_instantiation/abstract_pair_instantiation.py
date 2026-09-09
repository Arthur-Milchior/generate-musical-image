
from dataclasses import dataclass
from typing import Callable, ClassVar, Generic, Type, TypeVar

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.pattern_with_interval_lists import PatternType
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.interval_list import AbstractIntervalListPattern, IntervalList
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.note import Note, NoteFrozenList
from solfege.value.note.set.note_list import NoteList
from utils.easyness import KeyType
from utils.frozenlist import FrozenList
from utils.util import assert_typing


class AbstractPairInstantiation(AbstractPatternInstantiation[PatternType, Note, Interval, KeyType], Generic[PatternType, KeyType]):
    """
    An instantiation specifically for Note and Interval with both diatonic and chromatic information.
    """

    note_type: ClassVar[AbstractNote] = Note
    """Notes here carry both diatonic and chromatic information (`Note`, not `ChromaticNote`)."""

    interval_type: ClassVar[AbstractInterval] = Interval
    """Intervals here carry both diatonic and chromatic information (`Interval`, not `ChromaticInterval`)."""

    interval_list_type: ClassVar[FrozenList[IntervalType]] = IntervalList
    """The frozen-list-of-intervals class used to hold this instantiation's intervals."""

    note_list_type: ClassVar[FrozenList[NoteType]] = NoteList
    """The frozen-list-of-notes class returned by `get_notes()`."""

    chromatic_instantiation_type: ClassVar[Type[AbstractChromaticInstantiation]]
    """The `AbstractChromaticInstantiation` subclass produced by `get_chromatic_instantiation()`."""

    related_chromatic_type: ClassVar[AbstractChromaticInstantiation[PatternType, KeyType]]
    """Declared but never assigned by any concrete subclass (`Chord`/`Scale`/`InversionInstantiation` all set
    `chromatic_instantiation_type` instead, which is what `get_chromatic_instantiation()` actually reads)."""

    def get_intervals(self) -> AbstractIntervalListPattern[Interval]:
        """The pattern's own interval list, unmodified (diatonic+chromatic intervals from `lowest_note`)."""
        return self.pattern.get_interval_list()

    def get_chromatic_instantiation(self) -> AbstractChromaticInstantiation[PatternType, KeyType]:
        """The chromatic-only (no diatonic spelling) equivalent of this instantiation, anchored on
        `lowest_note`'s chromatic note."""
        # Note that for c4-flat, and c4-double flat, `self` is in base octave but the returned value is not.
        return self.chromatic_instantiation_type(self.pattern, self.lowest_note.get_chromatic())