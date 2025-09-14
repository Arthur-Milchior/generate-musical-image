from dataclasses import dataclass
from typing import ClassVar, Optional, Self, TypeVar

from solfege.value.getters import ChromaticGetter, DiatonicGetter
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class Chromatic(Singleton, ChromaticGetter[Self], DiatonicGetter):
    IntervalClass: ClassVar[type]
    number_of_interval_in_an_octave: ClassVar[int] = 12
    


    def __add__(self, other):
        from solfege.value.pair import Pair
        if isinstance(other, Pair):
            return self + other.get_chromatic()
        return super().__add__(self, other)

#pragma mark - ChromaticGetter

    def get_chromatic(self):
        return self
    
#pragma mark - DiatonicGetter
    
    def get_diatonic(self):
        """If this note belong to the diatonic scale, give it.
        Otherwise, give the adjacent diatonic note."""
        return self.DiatonicClass([0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6][
                                             self.in_base_octave().value] + 7 * self.octave())
    
ChromaticType = TypeVar("ChromaticType", bound=Chromatic)