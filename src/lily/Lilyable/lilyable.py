from __future__ import annotations

from dataclasses import dataclass

from lily import Lilyable


class Lilyable:
    """Represents a class that implements `lily` that generates the lily code to put in a file to then call lilypond on it."""
    def lily(self, midi: bool = False):
        return NotImplemented

    def __eq__(self, other: Lilyable):
        return self.lily() == other.lily()


@dataclass(frozen=True, eq=True)
class LiteralLilyable(Lilyable):
    """A class representing a lilyable explicitly given. 
    
    Can be considered as a Fake."""
    _lily: str

    def lily(self, midi: bool = False) -> str:
        return self._lily

