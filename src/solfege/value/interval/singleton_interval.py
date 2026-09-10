from dataclasses import dataclass
from typing import ClassVar, Self

from solfege.value.interval.abstract_interval import AbstractInterval
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class AbstractSingletonInterval(AbstractInterval, Singleton):
    """Base for an interval represented by a single int (i.e. `ChromaticInterval` or `DiatonicInterval`),
    combining `AbstractInterval`'s role/negation machinery with `Singleton`'s int-valued storage."""
    #Pragma mark - Singleton
    number_of_interval_in_an_octave: ClassVar[int]
    """Number of steps per octave for this representation (see `Singleton`)."""

    #pragma mark - AbstractInterval

    def __mul__(self, other: int) -> Self:
        """Scale the interval by the int `other` (e.g. a whole tone times 3 is a fourth augmented)."""
        assert_typing(other, int)
        return self.make_instance_of_selfs_class(value=self.value * other)

    def __add__(self, other: Self) ->Self:
        """Add two intervals of the same class. Returns `NotImplemented` for a different class."""
        if not other.__class__ == self.__class__:
            return NotImplemented
        return self.make_instance_of_selfs_class(value=self.value + other.value)

    def __neg__(self) -> Self:
        """Inverse interval"""
        return self.make_instance_of_selfs_class(value=-self.value)

    @classmethod
    def unison(cls) -> Self:
        """The unison (zero-valued) interval."""
        return cls.make(0)