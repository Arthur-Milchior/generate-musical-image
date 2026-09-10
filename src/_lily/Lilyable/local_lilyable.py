from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass


class LocalLilyable:
    """Represents a single note/chord/token-level chunk of LilyPond syntax (as opposed to `Lilyable`, which
    represents a full renderable score). Used for the individual elements fed into
    `piano_lilyable._for_list_of_notes`."""
    def __eq__(self, other: LocalLilyable):
        """Two `LocalLilyable`s are equal iff they generate the same LilyPond syntax, regardless of type."""
        return self.syntax_for_lily() == other.syntax_for_lily()

    # Must be implemented by subclasses

    @abstractmethod
    def syntax_for_lily(self):
        """Return the LilyPond syntax for this single note/chord/token."""
        ...

@dataclass(frozen=True)
class LiteralLocalLilyable(LocalLilyable):
    """A `LocalLilyable` whose syntax is given explicitly; usable as a fake in tests or for injecting raw
    LilyPond snippets."""
    _lily: str
    """The fixed LilyPond syntax string returned verbatim by `syntax_for_lily()`."""

    def syntax_for_lily(self):
        """Return the fixed `_lily` string."""
        return self._lily
