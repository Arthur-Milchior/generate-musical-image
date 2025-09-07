from dataclasses import dataclass
from typing import Dict, Generator, List, Optional, Tuple
from guitar.position.fret.fret import HIGHEST_FRET, NOT_PLAYED, OPEN_FRET, Fret
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing

@dataclass(frozen=True)
class Frets(DataClassWithDefaultArgument):
    """Represents a set of allowed frets.

    We assume for now that the allowed frets are an interval, and potentially the open string.

    min_fret>0
    max_fret """
    closed_fret_interval: Optional[Tuple[Fret, Fret]] = (Fret(1), HIGHEST_FRET)
    allow_open: bool = True
    allow_not_played: bool = False

    @classmethod
    def _default_arguments_for_constructor(cls):
        kwargs = super()._default_arguments_for_constructor()
        kwargs["closed_fret_interval"] = (Fret(1), HIGHEST_FRET)
        kwargs["allow_open"] = True
        kwargs["allow_not_played"] = False
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_closed_fret_interval(closed_fret_interval):
            if closed_fret_interval is None:
                return None
            m, M = closed_fret_interval
            return (Fret.make_single_argument(m), Fret.make_single_argument(M))
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "closed_fret_interval", clean_closed_fret_interval)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "allow_open")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "allow_not_played")
        return (args, kwargs)
    
    def __post_init__(self):
        assert_typing(self.allow_open, int)
        assert_typing(self.allow_not_played, bool)
        if self.closed_fret_interval is not None:
            assert_typing(self.closed_fret_interval, tuple)
            m, M = self.closed_fret_interval
            assert_typing(m, Fret)
            assert_typing(M, Fret)
            assert OPEN_FRET < m <= M, f"Wrong bounds {m}, {M}"

    def min_fret(self) -> Optional[Fret]:
        if self.closed_fret_interval is None:
            return None
        return self.closed_fret_interval[0]

    def max_fret(self) -> Optional[Fret]:
        if self.closed_fret_interval is None:
            return None
        return self.closed_fret_interval[1]

    def disallow_open(self) -> "Frets":
        return Frets.make(self.closed_fret_interval, allow_not_played=self.allow_not_played, allow_open=False)

    def force_played(self) -> "Frets":
        return Frets.make(self.closed_fret_interval, allow_not_played=False, allow_open=self.allow_open)
    
    def limit_min(self, min_fret: Fret) -> "Frets":
        """Restrict interval to fret at least min_fret. If self.min_fret >= min_fret, the returned value equals self."""
        assert_typing(min_fret, Fret)
        if self.closed_fret_interval is None:
            return self
        m, M = self.closed_fret_interval
        min_fret = max(min_fret, m)
        return Frets.make((min_fret, M), self.allow_open)
    
    def limit_max(self, max_fret: Fret) -> "Frets":
        """Restrict interval to fret at least max_fret. If self.max_fret >= max_fret, the returned value equals self."""
        assert_typing(max_fret, Fret)
        if self.closed_fret_interval is None:
            return self
        m, M = self.closed_fret_interval
        max_fret = min(max_fret, M)
        return Frets.make((m, max_fret), self.allow_open)
    
    def is_empty(self) -> bool:
        """Whether no note can be played"""
        return not self.allow_open and self.closed_fret_interval is None
    
    def is_contradiction(self) -> bool:
        """Whether no Fret oject satisfies this."""
        return self.is_empty() and not self.allow_not_played
    
    def __iter__(self) -> Generator[Fret]:
        if self.allow_not_played:
            yield NOT_PLAYED
        if self.allow_open:
            yield OPEN_FRET
        if self.closed_fret_interval is not None:
            min_fret, max_fret = self.closed_fret_interval
            yield from [Fret(fret) for fret in range(max(min_fret.value, 1), max_fret.value + 1)]

    def restrict_around(self, fret: Fret, interval_size: ChromaticInterval = ChromaticInterval(4)) -> "Frets":
        if fret.value is None:
            return self
        return self.limit_max(fret + interval_size).limit_min(fret - interval_size)
    
    def svg(self, absolute: bool)-> List[str]:
        """
        The svg to display current frets.
        """
        return [svg for fret in self for svg in fret.svg(absolute)]
    
EMPTY_FRETS = Frets.make(None, False, False)