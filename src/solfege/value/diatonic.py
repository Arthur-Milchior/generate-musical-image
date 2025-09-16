
from dataclasses import dataclass
from typing import ClassVar, Self, TypeVar
from solfege.value.getters import DiatonicGetter
from solfege.value.singleton import Singleton
from utils.util import assert_typing

@dataclass(frozen=True, eq=False)
class Diatonic(Singleton, DiatonicGetter[Self]):
    #Pragma mark - Singleton
    IntervalClass: ClassVar[type]
    number_of_interval_in_an_octave: ClassVar[int] = 7

    #Pragma public
    def __add__(self, other):
        from solfege.value.pair import Pair
        if isinstance(other, Pair):
            return self + other.get_diatonic()
        return super().__add__(self, other)
    
    #pragma mark - DiatonicGetter
    
    def get_diatonic(self):
        return self
    
DiatonicType = TypeVar("DiatonicType", bound = Diatonic)