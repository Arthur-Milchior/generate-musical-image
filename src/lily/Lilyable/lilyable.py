from __future__ import annotations

import unittest
from dataclasses import dataclass

from lily import Lilyable


class Lilyable:
    def lily(self, midi: bool = False):
        return NotImplemented

    def __eq__(self, other: Lilyable):
        return self.lily() == other.lily()


@dataclass(frozen=True)
class LiteralLilyable(Lilyable):
    _lily: str

    def lily(self, midi: bool = False):
        return self._lily

