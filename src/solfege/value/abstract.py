
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Self

from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import MakeableWithSingleArgument
from utils.util import assert_typing



@dataclass(frozen=True, unsafe_hash=True, eq=False)
class Abstract(DataClassWithDefaultArgument, MakeableWithSingleArgument, ABC):
    """The class of interval similar to the current class"""
    IntervalClass: ClassVar[type] #abstract interval

    # """The diatonic class similar to the current class"""
    # DiatonicClass: ClassVar[type["Abstract"]]
    # """The chromatic class similar to the current class"""
    # ChromaticClass: ClassVar[type["Abstract"]]

    # """The class with both Chromatic and Diatonic similar to the current class"""
    # PairClass: ClassVar[type]# abstract interval

    def __radd__(self, other):
        return self.__add__(other)

    def is_note(self) -> bool:
        """True if it's a note. False if it's an interval"""
        return False

    def add_octave(self, nb: int) -> Self:
        """Same note with nb more octave"""
        assert_typing(nb, int)
        return self + (self.IntervalClass.one_octave() * nb)

    def in_base_octave(self) -> Self:
        """Same note in the base octave"""
        return self.add_octave(-self.octave())

    def equals_modulo_octave(self, other) -> bool:
        """Whether self and other are same note, potentially at distinct octaves"""
        return self.in_base_octave() == other.in_base_octave()
    
    def __sub__(self, other):
        return self + (-other)
    
    def is_in_base_octave(self, accepting_octave: bool) -> bool:
        """Whether the value is in base octave. Used to check value is canonify when octave don't matter."""
        return self.in_base_octave() == self or self == self.one_octave()
    
    # Must be implemented by subclasses.

    @abstractmethod
    def octave(self) -> int:...
    """The octave number. For an interval, it's negative iff the interval is decreasing. Unison up to seventh major are at octave 0. Add one for each extra octave.
    For note, it's the distance to C4. So C4 to B4 is 0, C5 to B5 is 1...
    
    """

    @classmethod
    @abstractmethod
    def one_octave(cls) -> Self:...
    """Return the value at exactly one octave about value 0. Should not be used for note except maybe to check for canonicity"""
