from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from _lily import Lilyable


class Lilyable(ABC):
    """Represents a class that implements `lily` that generates the lily code to put in a file to then call lilypond on it."""
    @abstractmethod
    def lily(self, midi: bool = False):
        """Return the full LilyPond source code (a `\\score{...}` block or similar), optionally including a
        `\\midi{}`/`\\layout{}` block when `midi` is true."""
        ...

    def __eq__(self, other: Lilyable):
        """Two `Lilyable`s are equal if they generate the same LilyPond code."""
        return self.lily() == other.lily()


@dataclass(frozen=True)
class LiteralLilyable(Lilyable):
    """A class representing a lilyable explicitly given.

    Can be considered as a Fake."""
    _lily: str
    """The fixed LilyPond source string returned verbatim by `lily()`."""

    def lily(self, midi: bool = False) -> str:
        """Return the fixed `_lily` string, ignoring `midi`."""
        return self._lily

