from dataclasses import dataclass
from typing import ClassVar, Optional, Self, TypeVar

from solfege.value.getters import ChromaticGetter
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class Chromatic(Singleton, ChromaticGetter[Self]):
    #Pragma mark - Singleton

    IntervalClass: ClassVar[type]
    number_of_interval_in_an_octave: ClassVar[int] = 12
    
    #Public

    def __add__(self, other):
        from solfege.value.pair import Pair
        if isinstance(other, Pair):
            return self + other.get_chromatic()
        return super().__add__(self, other)

    #pragma mark - ChromaticGetter

    def get_chromatic(self):
        return self

ChromaticType = TypeVar("ChromaticType", bound=Chromatic)