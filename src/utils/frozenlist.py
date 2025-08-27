
from dataclasses import dataclass
from typing import Generic, List, TypeVar

from utils.util import assert_typing


T = TypeVar('T')

class FrozenList(Generic[T]):
    _l: List[T]

    def __init__(self, arg):
        # make a copy of the list
        self._l = list(arg)

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
    
    def __add__(self, l):
        return FrozenList(self._l + list(l))

    def __getitem__(self, index):
        return self._l[index]
    
    def __repr__(self):
        return f"FrozenList({self._l!r})"