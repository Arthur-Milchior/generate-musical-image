from dataclasses import dataclass
from typing import ClassVar, Self

from solfege.value.interval.abstract_interval import AbstractInterval
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class AbstractSingletonInterval(AbstractInterval, Singleton):
    #Pragma mark - Singleton
    number_of_interval_in_an_octave: ClassVar[int]

    #pragma mark - AbstractInterval

    def __mul__(self, other: int) -> Self:
        assert_typing(other, int)
        return self.make_instance_of_selfs_class(value=self.value * other)
    
    def __add__(self, other: Self) ->Self:
        if not other.__class__ == self.__class__:
            return NotImplemented
        return self.make_instance_of_selfs_class(value=self.value + other.value)

    def __neg__(self) -> Self:
        """Inverse interval"""
        return self.make_instance_of_selfs_class(value=-self.value)

    @classmethod
    def unison(cls):
        return cls.make(0)