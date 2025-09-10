


from typing import Generic

from utils.frozenlist import T


class DiatonicGetter(Generic[T]):
    """Protocol for class alowing to get a chromatic value."""
    def get_diatonic()-> T:
        return NotImplemented

class ChromaticGetter(Generic[T]):
    """Protocol for class alowing to get a chromatic value."""
    def get_chromatic()-> T:
        return NotImplemented