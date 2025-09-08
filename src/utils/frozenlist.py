
from dataclasses import dataclass
from typing import Generic, Iterable, List, Tuple, TypeVar

from utils.util import assert_all_same_class, assert_iterable_typing, assert_typing


T = TypeVar('T')
class FrozenList(Generic[T]):
    _l: List[T]

    def __init__(self, arg: Iterable[T]):
        # make a copy of the list
        l = list(arg)
        assert_all_same_class(l)
        self._l = l

    def __iter__(self):
        return iter(self._l)

    def __hash__(self):
        return hash(tuple(self._l))

    def __eq__(self, other: "FrozenList"):
        assert_typing(other, FrozenList)
        return self._l == other._l
    
    def list(self):
        """Return a copy of the underlying list."""
        return list(self._l)

    def append(self, value):
        l = self.list()
        l.append(value)
        return FrozenList(l)
    
    def __add__(self, other: Iterable[T]):
        other = list(other)
        if self._l:
            assert_iterable_typing(other, self._l[0].__class__)
        else:
            assert_all_same_class(other)
        return FrozenList(self._l + other)

    def __getitem__(self, index):
        return self._l[index]
    
    def __repr__(self):
        return f"FrozenList({self._l!r})"

    def __len__(self):
        return len(self._l)
    
    def head_tail(self) -> Tuple[T, "FrozenList[T]"]:
        return (self._l[0], FrozenList(self._l[1:]))
    
    def __mul__(self, other: int):
        assert_typing(other, int)
        return FrozenList(self._l * other)