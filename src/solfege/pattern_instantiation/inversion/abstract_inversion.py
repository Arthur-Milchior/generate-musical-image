
from dataclasses import dataclass
from typing import ClassVar, Generic, Tuple

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.pattern_with_interval_lists import PatternWithIntervalLists
from solfege.pattern_instantiation.pattern_instantiation import AbstractPatternInstantiation, IntervalFrozenListType, NoteFrozenListType
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.note.abstract_note import NoteType



@dataclass(frozen=True)
class AbstractInversionInstantiation(AbstractPatternInstantiation[InversionPattern, NoteType, IntervalType, Tuple[int, int]],  Generic[NoteType, IntervalType]):
    """Shared base for `InversionInstantiation` and `ChromaticInversionInstantiation`: an instantiation whose
    pattern is specifically an `InversionPattern`. Does not itself fix whether notes/intervals are
    diatonic+chromatic or chromatic-only -- that split happens in the concrete subclasses."""

    pattern_type: ClassVar[PatternWithIntervalLists] = InversionPattern
    """Restricts `pattern` (via `AbstractPatternInstantiation.__post_init__`'s type check) to `InversionPattern`."""
