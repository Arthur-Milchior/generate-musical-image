from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar


KeyType = TypeVar("KeyType")
class ClassWithEasyness(ABC, Generic[KeyType]):

    @abstractmethod
    def easy_key(self) -> KeyType:
        """Return a key which can be used in < to sort by easyness. The easiest note will be reviewed firsts."""
        return NotImplemented