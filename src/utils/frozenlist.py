
from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from typing import Callable, ClassVar, Generic, Iterable, List, Self, Tuple, Type, TypeVar

from utils.util import T, assert_all_same_class, assert_iterable_typing, assert_typing

class MakeableWithSingleArgument(ABC):
    """Protocol for "this type can be built from one loosely-typed argument, or passed through unchanged if
    already an instance" — used so pattern definitions can pass plain tuples/ints/strings instead of constructing
    value objects by hand (see `utils/README.md`)."""

    @classmethod
    def make_single_argument(cls, arg) -> Self:
        """Return `arg` unchanged if it's already an instance of `cls`, otherwise build one from it via
        `_make_single_argument` (and assert the result really is a `cls`)."""
        if isinstance(arg, cls):
            return arg
        r = cls._make_single_argument(arg)
        assert_typing(r, cls)
        return r

    # Must be implemented by subclasses

    @classmethod
    @abstractmethod
    def _make_single_argument(cls, arg) -> Self:
        """Build an instance of `cls` from the loosely-typed `arg`. Only called when `arg` isn't already a `cls`."""

    @abstractmethod
    def repr_single_argument(self) -> str:
        """Shows the value only, not parenthesis nor class."""
        ...

class FrozenList(Generic[T]):
    """An immutable, hashable list of elements of type `type`. Subclasses fix `type` (see `IntFrozenList`,
    `StrFrozenList` below, or any of the many per-value-type frozen lists elsewhere in the codebase) so the
    constructor knows both what to validate against and, when `type` implements `MakeableWithSingleArgument`, how
    to coerce loosely-typed elements."""

    _l: List[T]
    """The wrapped, ordinary mutable list backing this instance. Never mutated in place after `__init__`; every
    operation that "changes" a `FrozenList` returns a new instance instead."""

    type: ClassVar[Type]
    """The element type this list is restricted to; set by each concrete subclass."""

    def __init__(self, arg: Iterable[T] = None):
        """Build from `arg` (defaulting to empty). Makes a private copy of `arg`; if `type` implements
        `MakeableWithSingleArgument`, each element is coerced via `type.make_single_argument(...)` first. Asserts
        every resulting element is an instance of `type`."""
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
        """Return a new instance of the same class with `f` applied to every element."""
        return self.__class__([f(t) for t in self._l])

    def __iter__(self):
        """Iterate over the elements, in order."""
        return iter(self._l)

    def __hash__(self):
        """Hash based on the elements as a tuple, so equal `FrozenList`s hash equal."""
        return hash(tuple(self._l))

    def __eq__(self, other: Self):
        """Equal iff `other` is the same class and holds the same elements in the same order."""
        assert_typing(other, self.__class__)
        return self._l == other._l

    def list(self):
        """Return a copy of the underlying list."""
        return list(self._l)

    def append(self, value):
        """Return a new instance with `value` appended (does not mutate `self`)."""
        l = self.list()
        l.append(value)
        return self.__class__(l)

    def __add__(self, other: Iterable[T]) -> Self:
        """Return a new instance concatenating `self`'s elements with `other`'s. Asserts `other`'s elements share
        a single class, matching `self`'s element class when `self` is non-empty."""
        other = list(other)
        if self._l:
            assert_iterable_typing(other, self._l[0].__class__)
        else:
            assert_all_same_class(other)
        return self.__class__(self._l + other)

    def __getitem__(self, index) -> T:
        """Return the element at `index` (`int`) or a new plain list slice (`slice`)."""
        assert isinstance(index, int) or isinstance(index, slice)
        return self._l[index]

    def __repr__(self):
        """`ClassName([elt1, elt2, ...])`; elements use `repr_single_argument()` when `type` implements
        `MakeableWithSingleArgument` (to avoid nested class-name noise), else plain `repr()`."""
        if issubclass(self.type, MakeableWithSingleArgument):
            l = [elt.repr_single_argument() for elt in self]
        else:
            l = [repr(elt) for elt in self]
        return f"{self.__class__.__name__}([{", ".join(l)}])"

    def __len__(self):
        """Number of elements."""
        return len(self._l)

    def head_tail(self) -> Tuple[T, Self]:
        """Return `(first element, remaining elements as a new instance)`. Raises `IndexError` if empty."""
        return (self._l[0], self.__class__(self._l[1:]))

    def __mul__(self, other: int):
        """Return a new instance with the elements repeated `other` times, like `list * int`."""
        assert_typing(other, int)
        return self.__class__(self._l * other)

    def __reversed__(self) -> Self:
        """Return a new instance with the elements in reverse order."""
        return self.__class__(list(reversed(self._l)))

class IntFrozenList(FrozenList[int]):
    """A `FrozenList` of `int`."""
    type = int
    """Restricts elements to `int`."""

class StrFrozenList(FrozenList[str]):
    """A `FrozenList` of `str`."""
    type = str
    """Restricts elements to `str`."""

FrozenListType = TypeVar("FrozenListType", bound=FrozenList)