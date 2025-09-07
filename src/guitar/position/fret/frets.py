from dataclasses import dataclass
from typing import Optional
from guitar.position.fret.fret import HIGHEST_FRET, NOT_PLAYED, OPEN_FRET, Fret
from utils.util import assert_typing

@dataclass(frozen=True)
class Frets:
    """Represents a set of allowed frets.

    We assume for now that the allowed frets are an interval, and potentially the open string.

    min_fret>0
    max_fret """
    min_fret: int=1
    max_fret: int=HIGHEST_FRET.value
    allow_open: bool = True
    allow_not_played: bool = False
    
    def __post_init__(self):
        assert_typing(self.min_fret, int)
        assert_typing(self.max_fret, int)
        assert_typing(self.allow_open, int)
        assert_typing(self.allow_not_played, bool)

    def disallow_open(self):
        return Frets(self.min_fret, self.max_fret, allow_not_played=self.allow_not_played, allow_open=False)

    def force_played(self):
        return Frets(self.min_fret, self.max_fret, allow_not_played=False, allow_open=self.allow_open)
    
    def limit_min(self, min_fret):
        """Restrict interval to fret at least min_fret. If self.min_fret >= min_fret, the returned value equals self."""
        min_fret = max(min_fret, self.min_fret)
        return Frets(min_fret, self.max_fret, self.allow_open)
    
    def limit_max(self, max_fret):
        """Restrict interval to fret at least max_fret. If self.max_fret >= max_fret, the returned value equals self."""
        max_fret = min(max_fret, self.max_fret)
        return Frets(self.min_fret, max_fret, self.allow_open)
    
    def is_empty(self):
        """Whether no note can be played"""
        return not self.allow_open and self.min_fret>self.max_fret
    
    def is_contradiction(self):
        """Whether no Fret oject satisfies this."""
        return self.is_empty() and not self.allow_not_played
    
    def __iter__(self):
        if self.allow_not_played:
            yield NOT_PLAYED
        if self.allow_open:
            yield OPEN_FRET
        yield from [Fret(fret) for fret in range(max(self.min_fret, 1), self.max_fret + 1)]

    def restrict_around(self, fret: Fret, interval_size: int = 4):
        if fret.value is None:
            return self
        return self.limit_max(fret.value + interval_size).limit_min(fret.value - interval_size)
    
    def svg(self, absolute: bool):
        """
        The svg to display current frets.
        """
        return [svg for fret in self for svg in fret.svg(absolute)]
    
EMPTY_FRETS = Frets(3, 2, False, False)