
from dataclasses import dataclass
from typing import ClassVar, Optional, Self, Tuple, Union

from solfege.value.getters import ChromaticGetter, DiatonicGetter
from utils.frozenlist import MakeableWithSingleArgument
from utils.util import assert_typing



@dataclass(frozen=True, unsafe_hash=True, eq=False)
class Abstract(MakeableWithSingleArgument, ChromaticGetter, DiatonicGetter):
    """The class of interval similar to the current class"""
    IntervalClass: ClassVar[type] #abstract interval

    """The diatonic class similar to the current class"""
    DiatonicClass: ClassVar[type["Abstract"]]
    """The chromatic class similar to the current class"""
    ChromaticClass: ClassVar[type["Abstract"]]

    """The class with both Chromatic and Diatonic similar to the current class"""
    PairClass: ClassVar[type]# abstract interval

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
    
    def octave(self) -> int:
        return NotImplemented
    
    def __sub__(self, other):
        return self + (-other)
    
    def get_pair(self):
        return self.PairClass(self.get_chromatic(), self.get_diatonic())