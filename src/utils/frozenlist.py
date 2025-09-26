
from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from typing import Callable, ClassVar, Generic, Iterable, List, Self, Tuple, Type, TypeVar

from utils.util import T, assert_all_same_class, assert_iterable_typing, assert_typing

class MakeableWithSingleArgument(ABC):

    @classmethod
    def make_single_argument(cls, arg) -> Self:
        if isinstance(arg, cls):
            return arg
        r = cls._make_single_argument(arg)
        assert_typing(r, cls)
        return r
    
    # Must be implemented by subclasses

    @classmethod
    @abstractmethod
    def _make_single_argument(cls, arg) -> Self:...

    @abstractmethod
    def repr_single_argument(self) -> str:...
    """Shows the value only, not parenthesis nor class."""

class FrozenList(Generic[T]):
    _l: List[T]
    type: ClassVar[Type]

    def __init__(self, arg: Iterable[T] = None):
        if arg is None:
            self._l = []
            return
        # make a copy of the list
        l = list(arg)
        if issubclass(self.type, MakeableWithSingleArgument):
            l = [self.type.make_single_argument(arg) for arg in l]
        assert_iterable_typing(l, self.type)
        self._l = l

    def map(self, f: Callable[[T], T]) -> Self:
        return self.__class__([f(t) for t in self._l])

    def __iter__(self):
        return iter(self._l)

    def __hash__(self):
        return hash(tuple(self._l))

    def __eq__(self, other: Self):
        assert_typing(other, self.__class__)
        return self._l == other._l
    
    def list(self):
        """Return a copy of the underlying list."""
        return list(self._l)

    def append(self, value):
        l = self.list()
        l.append(value)
        return self.__class__(l)
    
    def __add__(self, other: Iterable[T]) -> Self:
        other = list(other)
        if self._l:
            assert_iterable_typing(other, self._l[0].__class__)
        else:
            assert_all_same_class(other)
        return self.__class__(self._l + other)

    def __getitem__(self, index) -> T:
        assert isinstance(index, int) or isinstance(index, slice)
        return self._l[index]
    
    def __repr__(self):
        if issubclass(self.type, MakeableWithSingleArgument):
            l = [elt.repr_single_argument() for elt in self]
        else:
            l = [repr(elt) for elt in self]
        return f"{self.__class__.__name__}([{", ".join(l)}])"

    def __len__(self):
        return len(self._l)
    
    def head_tail(self) -> Tuple[T, Self]:
        return (self._l[0], self.__class__(self._l[1:]))
    
    def __mul__(self, other: int):
        assert_typing(other, int)
        return self.__class__(self._l * other)
    
    def __reversed__(self) -> Self:
        return self.__class__(list(reversed(self._l)))
    
class IntFrozenList(FrozenList[int]):
    type = int

class StrFrozenList(FrozenList[str]):
    type = str

FrozenListType = TypeVar("FrozenListType", bound=FrozenList)