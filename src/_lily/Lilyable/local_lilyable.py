from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass


class LocalLilyable:
    """Represents a single note/chord/token-level chunk of LilyPond syntax (as opposed to `Lilyable`, which
    represents a full renderable score). Used for the individual elements fed into
    `piano_lilyable._for_list_of_notes`."""
    def __eq__(self, other: LocalLilyable):
        """Intended to compare by generated syntax, but compares the bound methods `self.syntax_for_lily` /
        `other.syntax_for_lily` rather than calling them: bound-method equality falls back to identity of
        `__self__`, so this is effectively identity comparison (`self is other`), not value equality, unless a
        subclass supplies its own `__eq__` (e.g. `LiteralLocalLilyable`'s dataclass-generated one, which
        overrides this). Verified: two distinct instances with identical `syntax_for_lily()` results compare
        unequal here. Left as-is; likely a latent bug in this base class."""
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
