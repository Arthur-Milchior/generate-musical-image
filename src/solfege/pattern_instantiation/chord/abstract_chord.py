
from dataclasses import dataclass
from typing import ClassVar, Generic

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.pattern_with_interval_lists import PatternWithIntervalLists
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType


@dataclass(frozen=True)
class AbstractChord(AbstractPatternInstantiation[ChordPattern, NoteType, IntervalType, int],  Generic[NoteType, IntervalType]):
    """Shared base for `Chord` and `ChromaticChord`: an instantiation whose pattern is specifically a
    `ChordPattern`. Does not itself fix whether notes/intervals are diatonic+chromatic or chromatic-only --
    that split happens in the concrete `Chord`/`ChromaticChord` subclasses."""

    pattern_type: ClassVar[PatternWithIntervalLists] = ChordPattern
    """Restricts `pattern` (via `AbstractPatternInstantiation.__post_init__`'s type check) to `ChordPattern`."""
