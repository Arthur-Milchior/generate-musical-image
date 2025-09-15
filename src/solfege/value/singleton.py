from dataclasses import dataclass
import math
from typing import Callable, ClassVar, Self, Type, TypeVar, Union

from solfege.value.abstract import Abstract
from utils.frozenlist import MakeableWithSingleArgument
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class Singleton(Abstract, MakeableWithSingleArgument):
    # Must be implemented by subclasses.
    IntervalClass: ClassVar[Type[Self]]

    """number of note by octave (7 for diatonic, 12 for chromatic)"""
    number_of_interval_in_an_octave: ClassVar[int]

    #public
    value: int

    @classmethod
    def make_instance_of_selfs_class(cls: Type[Self], value: int):
        return cls(value)

    def __post_init__(self):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used."""
        assert_typing(self.value, int)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise Exception(f"Comparison of two distinct classes: {self}:{self.__class__} and {other}:{other.__class__}")
        return self.value == other.value
    
    def __hash__(self):
        return self.value

    def __le__(self, other: Self):
        assert_typing(other, self.__class__)
        return self.value <= other.value

    def __lt__(self, other: Self):
        assert_typing(other, self.__class__)
        return self.value < other.value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"
    
    #pragma mark - MakeableWithSingleArgument

    def repr_single_argument(self) -> str:
        return f"""{self.value}"""

    @classmethod
    def _make_single_argument(cls, value: int) -> Self:
        assert_typing(value, int)
        return cls.make_instance_of_selfs_class(value)
    
    #pragma mark - Abstract
    
    def octave(self):
        """The octave number. 0 for unison/central C up to seventh/C one octave above."""
        return math.floor(self.value / self.__class__.number_of_interval_in_an_octave)

    @classmethod
    def one_octave(cls) -> Self:
        return cls.make_instance_of_selfs_class(value=cls.number_of_interval_in_an_octave)
        
    
SingletonType = TypeVar("SingletonType", bound=Singleton)