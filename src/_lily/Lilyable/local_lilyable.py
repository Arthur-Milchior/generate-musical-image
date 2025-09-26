from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass


class LocalLilyable:
    def __eq__(self, other: LocalLilyable):
        return self.syntax_for_lily == other.syntax_for_lily

    # Must be implemented by subclasses
    
    @abstractmethod
    def syntax_for_lily(self):...

@dataclass(frozen=True)
class LiteralLocalLilyable(LocalLilyable):
    _lily: str

    def syntax_for_lily(self):
        return self._lily
