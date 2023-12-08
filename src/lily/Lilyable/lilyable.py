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


class TestLilyable(unittest.TestCase):
    def test_lily(self):
        self.assertEquals("aes", LiteralLilyable("aes").lily())

    def test_eq_diff_class(self):
        class MockLily(Lilyable):
            def lily(self):
                return "aes"

        self.assertEquals(LiteralLilyable("aes"), MockLily())

    def test_eq(self):
        self.assertEquals(LiteralLilyable("aes"), LiteralLilyable("aes"))