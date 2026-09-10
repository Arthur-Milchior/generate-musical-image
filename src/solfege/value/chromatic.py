from dataclasses import dataclass
from typing import ClassVar, Optional, Self, TypeVar, Union

from solfege.value.getters import ChromaticGetter
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class Chromatic(Singleton, ChromaticGetter[Self]):
    """Base for values (notes or intervals) represented purely by a chromatic (semitone) position/count,
    with no diatonic information attached. `ChromaticNote` and `ChromaticInterval` are its concrete
    subclasses."""
    #Pragma mark - Singleton

    IntervalClass: ClassVar[type]
    """The chromatic interval class matching this chromatic value class."""
    number_of_interval_in_an_octave: ClassVar[int] = 12
    """Chromatic values divide the octave into 12 semitones."""

    #Public

    def __add__(self, other: Union["Pair", Self]) -> Self:
        """Add another value. If `other` is a `Pair` (chromatic+diatonic), only its chromatic component
        is used, since a purely chromatic value has no diatonic part to add."""
        from solfege.value.pair import Pair
        if isinstance(other, Pair):
            return self + other.get_chromatic()
        return super().__add__(self, other)

    #pragma mark - ChromaticGetter

    def get_chromatic(self) -> Self:
        """Return self: a `Chromatic` value is already its own chromatic component."""
        return self

ChromaticType = TypeVar("ChromaticType", bound=Chromatic)
"""Type variable bound to `Chromatic`, used to parametrize generic classes over the concrete chromatic type."""