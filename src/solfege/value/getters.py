


from abc import ABC, abstractmethod
from typing import Generic

from utils.frozenlist import T


class DiatonicGetter(ABC, Generic[T]):
    """Protocol for class alowing to get a chromatic value."""
    @abstractmethod
    def get_diatonic()-> T:
        return NotImplemented

class ChromaticGetter(ABC, Generic[T]):
    """Protocol for class alowing to get a chromatic value."""
    @abstractmethod
    def get_chromatic()-> T:
        return NotImplemented