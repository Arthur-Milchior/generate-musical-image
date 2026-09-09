


from abc import ABC, abstractmethod
from typing import Generic

from utils.frozenlist import T


class DiatonicGetter(ABC, Generic[T]):
    """Protocol for classes allowing to get a diatonic value."""
    @abstractmethod
    def get_diatonic()-> T:
        """Return the diatonic (scale-degree) component of this value, as an instance of `T`."""
        ...
class ChromaticGetter(ABC, Generic[T]):
    """Protocol for classes allowing to get a chromatic value."""
    @abstractmethod
    def get_chromatic()-> T:
        """Return the chromatic (semitone) component of this value, as an instance of `T`."""
        ...