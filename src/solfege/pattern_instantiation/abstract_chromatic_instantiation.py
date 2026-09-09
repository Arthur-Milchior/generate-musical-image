
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import AbstractInterval, IntervalType
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import AbstractIntervalListPattern, ChromaticIntervalListPattern
from solfege.value.note.abstract_note import AbstractNote, NoteType
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.easyness import KeyType
from utils.frozenlist import FrozenList
from utils.util import T, assert_typing


@dataclass(frozen=True, eq=True)
class AbstractChromaticInstantiation(AbstractPatternInstantiation[T, ChromaticNote, ChromaticInterval, KeyType], Generic[T, KeyType]):
    """An instantiation anchored on a `ChromaticNote` (chromatic pitch only, no diatonic spelling) rather than
    a full `Note`. Produced by `AbstractPairInstantiation.get_chromatic_instantiation()`."""

    note_type: ClassVar[AbstractNote] = ChromaticNote
    """Notes here are chromatic-only (`ChromaticNote`), unlike `AbstractPairInstantiation`'s `Note`."""

    interval_type: ClassVar[AbstractInterval] = ChromaticInterval
    """Intervals here are chromatic-only (`ChromaticInterval`)."""

    interval_list_type: ClassVar[FrozenList[IntervalType]] = ChromaticIntervalListPattern
    """The frozen-list-of-intervals class used to hold this instantiation's intervals."""

    note_list_type: ClassVar[FrozenList[NoteType]] = ChromaticNoteList
    """The frozen-list-of-notes class returned by `get_notes()`."""


    def get_intervals(self) -> AbstractIntervalListPattern[Interval]:
        """The pattern's full set of intervals (`intervals_with_all_notes()`, all notes -- e.g. a chord's fifth
        is never dropped here even if `optional_fifth`), as chromatic-only intervals from `lowest_note`. Only
        `ChordPattern`/`InversionPattern` define `intervals_with_all_notes()`; `ScalePattern` does not, so this
        is only exercised through `ChromaticChord`/`ChromaticInversionInstantiation` in practice."""
        return self.pattern.intervals_with_all_notes()