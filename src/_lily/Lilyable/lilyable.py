from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from _lily import Lilyable


class Lilyable(ABC):
    """Represents a class that implements `lily` that generates the lily code to put in a file to then call lilypond on it."""
    @abstractmethod
    def lily(self, midi: bool = False):...
    def __eq__(self, other: Lilyable):
        return self.lily() == other.lily()


@dataclass(frozen=True)
class LiteralLilyable(Lilyable):
    """A class representing a lilyable explicitly given. 
    
    Can be considered as a Fake."""
    _lily: str

    def lily(self, midi: bool = False) -> str:
        return self._lily

