from dataclasses import dataclass
from itertools import pairwise
from typing import Callable, ClassVar, Dict, Generic, Iterable, List, Self, Tuple, Type, TypeVar, Union

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.interval.set.abstract_interval_list_pattern import AbstractIntervalListPattern
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern
from utils.frozenlist import FrozenList
from utils.util import assert_iterable_typing, assert_typing, sorted_unique

@dataclass(frozen=True, unsafe_hash=True, repr=False)
class IntervalList(AbstractIntervalListPattern[Interval]):
    """An `AbstractIntervalListPattern` holding full (chromatic+diatonic) `Interval`s — the shape used
    by chord/scale patterns before they're anchored to a tonic."""
    interval_type: ClassVar[Type[Interval]] = Interval
    """Intervals in this list are full `Interval`s."""
    _frozen_list_type: ClassVar[Type] = IntervalFrozenList
    """Storage type for `_absolute_intervals`."""

    @classmethod
    def _note_list_constructor(cls):
        """Return `NoteList`, the note-list type matching full (chromatic+diatonic) intervals."""
        from solfege.value.note.set.note_list import NoteList
        return NoteList

    @staticmethod
    def interval_repr(interval: Interval) -> str:
        "How to display the interval in make."
        return f"""({interval.get_chromatic().value}, {interval._diatonic.value})"""

    def get_chromatic_interval_list(self) -> ChromaticIntervalListPattern:
        """Return the chromatic-only projection of this list (dropping diatonic spelling)."""
        chromatic_interval_list = ChromaticIntervalListPattern.make_absolute([interval.get_chromatic() for interval in self._absolute_intervals], increasing=self.increasing)
        assert_typing(chromatic_interval_list, ChromaticIntervalListPattern)
        return chromatic_interval_list

    def get_interval_list(self) -> "IntervalList":
        """Return an equivalent `IntervalList` built directly from the raw dataclass fields (bypassing
        `make`'s coercion, since the fields are already the right types)."""
        return IntervalList(self._absolute_intervals, self.increasing)

    def best_enharmonic_starting_note(self, chromatic_note: "ChromaticNote"):
        """Among every enharmonic spelling of `chromatic_note` (e.g. C# vs Db), pick the one that
        yields the "easiest" (fewest/smallest alterations) instantiation of this pattern."""
        from solfege.value.note.chromatic_note import ChromaticNote
        from solfege.value.note.note import Note
        return min(Note.all_from_chromatic(chromatic_note), key = lambda note: self.from_note(note).easy_key())

    def intervals_from_diatonic(self, diatonic_interval: "DiatonicNote") -> Iterable["Interval"]:
        """Every interval in this list whose diatonic component equals `diatonic_interval` exactly
        (there can be more than one, e.g. a chromatic passing tone sharing a diatonic index)."""
        from solfege.value.interval.diatonic_interval import DiatonicInterval
        from solfege.value.interval.chromatic_interval import ChromaticInterval
        assert_typing(diatonic_interval, DiatonicInterval)
        return [interval for interval in self._absolute_intervals if interval.get_diatonic() == diatonic_interval]

    def alterations_from_diatonic(self, diatonic_interval: "DiatonicInterval") -> Iterable["IntervalAlteration"]:
        """The alteration (or a `WrongAlteration` placeholder if out of range) of every interval in
        this list whose diatonic component equals `diatonic_interval` exactly."""
        from solfege.value.interval.diatonic_interval import DiatonicInterval
        from solfege.value.interval.interval_alteration import IntervalAlteration
        assert_typing(diatonic_interval, DiatonicInterval)
        return [interval.get_alteration(throw=False) for interval in self.intervals_from_diatonic(diatonic_interval)]

class IntervalListFrozenList(FrozenList[IntervalList]):
    """A `FrozenList` specialized to hold `IntervalList` elements."""
    type = IntervalList
    """Element type enforced by `FrozenList`."""
