from dataclasses import dataclass
import math
from typing import Callable, ClassVar, Self, Type, Union

from solfege.value.abstract import Abstract
from utils.util import assert_typing


@dataclass(frozen=True)
class Singleton(Abstract):
    value: int
    IntervalClass: ClassVar[Type["Singleton"]]

    """number of note by octave (7 for diatonic, 12 for chromatic)"""
    number_of_interval_in_an_octave: ClassVar[int]

    @classmethod
    def make_instance_of_selfs_class(cls: Type["Singleton"], value: int):
        return cls(value)

    def __post_init__(self):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used."""
        assert_typing(self.value, int)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise Exception(f"Comparison of two distinct classes: {self.__class__} and {other.__class__}")
        return self.value == other.value
    
    def __hash__(self):
        return self.value

    def __le__(self, other: "Singleton"):
        assert_typing(other, self.__class__)
        return self.value <= other.value

    def __lt__(self, other: "Singleton"):
        assert_typing(other, self.__class__)
        return self.value < other.value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"
    
    def _add(self, other: "Singleton"):
        from solfege.value.note.abstract_note import AbstractNote
        from solfege.value.interval.abstract_interval import AbstractInterval
        assert (self.IntervalClass == other.IntervalClass, f"{self.IntervalClass} != {other.IntervalClass}")
        if isinstance(other, AbstractNote):
            assert_typing(self, AbstractInterval)
            return other.make_instance_of_selfs_class(self.value + other.value)
        assert_typing(other, AbstractInterval)
        return self.make_instance_of_selfs_class(self.value + other.value)
    
    def octave(self):
        """The octave number. 0 for unison/central C up to seventh/C one octave above."""
        return math.floor(self.value / self.__class__.number_of_interval_in_an_octave)

    @classmethod
    def make_single_argument(cls, value: Union[int, "Singleton"]) -> Self:
        if isinstance(value, int):
            return cls.make_instance_of_selfs_class(value)
        assert_typing(value, cls)
        return value