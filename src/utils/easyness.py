from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar


KeyType = TypeVar("KeyType")
class ClassWithEasyness(ABC, Generic[KeyType]):
    """Mixin for values that can be ranked by difficulty, via a single abstract method, `easy_key()`. Used to
    sort/rank patterns (notes, chords, scales, ...) so the easiest ones are learned/practiced first."""

    @abstractmethod
    def easy_key(self) -> KeyType:
        """Return a key which can be used in < to sort by easyness. The easiest note will be reviewed firsts."""
        ...
