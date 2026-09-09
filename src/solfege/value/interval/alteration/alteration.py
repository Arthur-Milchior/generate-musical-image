
from dataclasses import dataclass
from typing import ClassVar, TypeVar

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
from utils.easyness import ClassWithEasyness


@dataclass(frozen=True)
class Alteration(ChromaticInterval, ClassWithEasyness[int]):
    """A small chromatic offset (sharp/flat count) applied on top of a "natural" diatonic value, e.g.
    the +1 in G# = G + 1 semitone. Represented as a `ChromaticInterval` whose `value` must stay within
    `[min_value, max_value]` (subclass-defined); out-of-range values raise `TooBigAlterationException`.
    `NoteAlteration`/`IntervalAlteration` are the two families of concrete subclasses."""

    #pragma mark - Abstract

    def in_base_octave(self):
        """Not meaningful for an alteration (it has no octave); always raises."""
        raise Exception("Alteration has no base octave")

    def is_in_base_octave(self, accepting_octave: bool) -> bool:
        """Always `True`: an alteration is not octave-bound, so it's trivially "in base octave"."""
        return True

    #pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        """Validate `value` falls within `[min_value, max_value]`, raising `TooBigAlterationException`
        otherwise."""
        super().__post_init__()
        if not self.min_value <= self.value <= self.max_value:
            raise TooBigAlterationException(self.value)

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> int:
        """Natural are esaier than flat and sharp, which are easier than double sharp and flat."""
        return abs(self.value)

    # must be implemented by subclass

    min_value: ClassVar[int]
    """Smallest `value` this alteration subclass allows (e.g. -1 for `JustAlteration`'s diminished)."""
    max_value: ClassVar[int]
    """Largest `value` this alteration subclass allows (e.g. 1 for `JustAlteration`'s augmented)."""

AlterationType = TypeVar("Alteration", bound=Alteration)
"""Type variable bound to `Alteration`, used to parametrize generic classes over the concrete alteration type."""