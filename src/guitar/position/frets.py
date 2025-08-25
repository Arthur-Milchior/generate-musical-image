from dataclasses import dataclass
from typing import Optional

from guitar.position.fret import OPEN_FRET, Fret, HIGHEST_FRET
from utils.util import assert_typing

@dataclass(frozen=True, eq=True)
class Frets:
    """Represents a set of allowed frets.

    We assume for now that the allowed frets are an interval, and potentially the open string.

    min_fret>0
    max_fret """
    min_fret: int=1
    max_fret: int=HIGHEST_FRET.value
    allow_open: bool = True
    
    def __post_init__(self):
        assert_typing(self.min_fret, int)
        assert_typing(self.max_fret, int)
        assert_typing(self.allow_open, int)

    def disallow_open(self):
        return Frets(self.min_fret, self.max_fret, False)
    
    def limit_min(self, min_fret):
        """Restrict interval to fret at least min_fret. If self.min_fret >= min_fret, the returned value equals self."""
        min_fret = max(min_fret, self.min_fret)
        return Frets(min_fret, self.max_fret, self.allow_open)
    
    def limit_max(self, max_fret):
        """Restrict interval to fret at least max_fret. If self.max_fret >= max_fret, the returned value equals self."""
        max_fret = min(max_fret, self.max_fret)
        return Frets(self.min_fret, max_fret, self.allow_open)
    
    def is_empty(self):
        return not self.allow_open and self.min_fret>self.max_fret
    
    def __iter__(self):
        if self.allow_open: 
            yield OPEN_FRET
        for fret in range(max(self.min_fret, 1), self.max_fret + 1):
            yield Fret(fret)

    def restrict_around(self, fret: Fret, interval_size: int = 4):
        if fret.value is None:
            return self
        return self.limit_max(fret.value + interval_size).limit_min(fret.value - interval_size)
    
    def svg(self, absolute: bool):
        """
        The svg to display current frets.
        """
        for fret in self:
            yield from fret.svg(absolute)