
from dataclasses import dataclass
from typing import ClassVar, Self, Tuple, Union

from utils.util import assert_typing


@dataclass(frozen=True)
class Abstract:
    """The class of interval similar to the current class"""
    IntervalClass: ClassVar[type] #abstract interval

    """The diatonic class similar to the current class"""
    DiatonicClass: ClassVar[type["Abstract"]]
    """The chromatic class similar to the current class"""
    ChromaticClass: ClassVar[type["Abstract"]]

    """The class with both Chromatic and Diatonic similar to the current class"""
    PairClass: ClassVar[type]# abstract interval

    def is_note(self) -> bool:
        """True if it's a note. False if it's an interval"""
        return False
    
    def _add(self, other: "Abstract")->"Abstract":
        return NotImplemented
    
    def __add__(self, other:"Abstract"):
        try:
            return self._add(other)
        except:
            return other._add(self)
    
    def __sub__(self, other: "Abstract") -> Self:
        """This interval minus the other one. Class of `self`"""
        from solfege.interval.abstract_interval import AbstractInterval
        assert_typing(other, AbstractInterval)
        neg = -other
        if neg.is_note():
            raise Exception("Neg is %s, which is a note" % neg)
        return self + neg

    def add_octave(self, nb: int) -> Self:
        """Same note with nb more octave"""
        return self + (self.IntervalClass.one_octave() * nb)

    def in_base_octave(self) -> Self:
        """Same note in the base octave"""
        return self.add_octave(-self.octave())

    def equals_modulo_octave(self, other) -> bool:
        """Whether self and other are same note, potentially at distinct octaves"""
        return self.in_base_octave() == other.in_base_octave()
    
    def octave(self) -> int:
        return NotImplemented
    
    def make_single_argument(cls, value: Union[int, "Abstract", Tuple[int, int]]):
        return NotImplemented