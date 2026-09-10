
from dataclasses import dataclass
from typing import ClassVar, Self, TypeVar, Union
from solfege.value.getters import DiatonicGetter
from solfege.value.singleton import Singleton
from utils.util import assert_typing

@dataclass(frozen=True, eq=False)
class Diatonic(Singleton, DiatonicGetter[Self]):
    """Base for values (notes or intervals) represented purely by a diatonic (scale-degree) position/count,
    with no chromatic information attached. `DiatonicNote` and `DiatonicInterval` are its concrete
    subclasses."""
    #Pragma mark - Singleton
    IntervalClass: ClassVar[type]
    """The diatonic interval class matching this diatonic value class."""
    number_of_interval_in_an_octave: ClassVar[int] = 7
    """Diatonic values divide the octave into 7 scale degrees."""

    #Pragma public
    def __add__(self, other: Union["Pair", Self]) -> Self:
        """Add another value. If `other` is a `Pair` (chromatic+diatonic), only its diatonic component
        is used, since a purely diatonic value has no chromatic part to add."""
        from solfege.value.pair import Pair
        if isinstance(other, Pair):
            return self + other.get_diatonic()
        return super().__add__(self, other)

    #pragma mark - DiatonicGetter

    def get_diatonic(self) -> Self:
        """Return self: a `Diatonic` value is already its own diatonic component."""
        return self

DiatonicType = TypeVar("DiatonicType", bound = Diatonic)
"""Type variable bound to `Diatonic`, used to parametrize generic classes over the concrete diatonic type."""