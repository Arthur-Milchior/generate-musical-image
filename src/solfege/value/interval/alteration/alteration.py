
from dataclasses import dataclass
from typing import ClassVar, TypeVar

from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
from utils.easyness import ClassWithEasyness


@dataclass(frozen=True)
class Alteration(ChromaticInterval, ClassWithEasyness[int]):

    #pragma mark - Abstract

    def in_base_octave(self):
        raise Exception("Alteration has no base octave")

    def is_in_base_octave(self, accepting_octave: bool) -> bool:
        return True
    
    #pragma mark - DataClassWithDefaultArgument
   
    def __post_init__(self):
        super().__post_init__()
        if not self.min_value <= self.value <= self.max_value:
            raise TooBigAlterationException(self.value) 

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> int:
        return abs(self.value)
    
    # must be implemented by subclass

    min_value: ClassVar[int]
    max_value: ClassVar[int]

AlterationType = TypeVar("Alteration", bound=Alteration)