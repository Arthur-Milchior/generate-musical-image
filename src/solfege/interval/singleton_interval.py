
from dataclasses import dataclass
from typing import ClassVar, Self

from solfege.interval.abstract_interval import AbstractInterval
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True)
class AbstractSingletonInterval(AbstractInterval, Singleton):
    number_of_interval_in_an_octave: ClassVar[int]

    def __mul__(self, other: int) -> Self:
        assert_typing(other, int)
        return self.make_instance_of_selfs_class(value=self.value * other)

    def __neg__(self) -> Self:
        """Inverse interval"""
        return self.make_instance_of_selfs_class(value=-self.value)
    
    @classmethod
    def unison(cls):
        return cls(0)

    @classmethod
    def one_octave(cls) -> Self:
        return cls.make_instance_of_selfs_class(value=cls.number_of_interval_in_an_octave)

Singleton.IntervalClass = AbstractSingletonInterval