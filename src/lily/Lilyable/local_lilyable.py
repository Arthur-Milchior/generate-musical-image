from __future__ import annotations

from dataclasses import dataclass


class LocalLilyable:
    def lily_in_scale(self):
        return NotImplemented

    def __eq__(self, other: LocalLilyable):
        return self.lily_in_scale == other.lily_in_scale


@dataclass(frozen=True)
class LiteralLocalLilyable(LocalLilyable):
    _lily: str

    def lily_in_scale(self):
        return self._lily
