from dataclasses import dataclass
import dataclasses
from typing import Dict, Generator, List, Optional, Tuple
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fret.fret import Fret
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing

@dataclass(frozen=True)
class Frets(DataClassWithDefaultArgument):
    """Represents a set of allowed frets.

    We assume for now that the allowed frets are an interval, and potentially the open string.

    min_fret>0
    max_fret """
    instrument: FrettedInstrument

    """If `closed_fret_interval` is None, no closed fret can be played.
    If it's [m, None] then it should be interpreted as all frets starting at m.
    If it's [m, M], it's all frets betwee m and M included."""
    _closed_fret_interval: Optional[Tuple[Fret, Optional[Fret]]]
    allow_open: bool
    allow_not_played: bool

    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        default = super()._default_arguments_for_constructor(args, kwargs)
        default["_closed_fret_interval"] = (kwargs["instrument"].fret(1), None)
        default["allow_open"] = True
        default["allow_not_played"] = False
        return default

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_closed_fret_interval(closed_fret_interval):
            instrument: FrettedInstrument = kwargs["instrument"]
            assert_typing(instrument, FrettedInstrument)
            if closed_fret_interval is None:
                return None
            if isinstance(closed_fret_interval, Tuple):
                m, M = closed_fret_interval
            else:
                m = closed_fret_interval
                M = None
            m = instrument.fret(m)
            M = None if M is None else instrument.fret(M)
            return (m, M)
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_closed_fret_interval", clean_closed_fret_interval)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "allow_open")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "allow_not_played")
        return (args, kwargs)
    
    def __post_init__(self):
        assert_typing(self.instrument, FrettedInstrument)
        assert_typing(self.allow_open, int)
        assert_typing(self.allow_not_played, bool)
        if self._closed_fret_interval is not None:
            assert_typing(self._closed_fret_interval, tuple)
            m, M = self.closed_fret_interval()
            assert_typing(m, Fret)
            assert_typing(M, Fret)
            assert 0 < m.value <= M.value, f"Wrong bounds {m}, {M}"

    def closed_fret_interval(self):
        if self._closed_fret_interval is None:
            return None
        m, M = self._closed_fret_interval
        if M is None:
            M = self.instrument.last_fret()
        return (m, M)

    def min_fret(self) -> Optional[Fret]:
        if self._closed_fret_interval is None:
            return None
        return self._closed_fret_interval[0]

    def max_fret(self) -> Optional[Fret]:
        if self._closed_fret_interval is None:
            return None
        return self.closed_fret_interval()[1]

    def disallow_open(self) -> "Frets":
        return dataclasses.replace(self, allow_open=False)

    def force_played(self) -> "Frets":
        return dataclasses.replace(self, allow_not_played=False)
    
    def limit_min(self, min_fret: Fret) -> "Frets":
        """Restrict interval to fret at least min_fret. If self.min_fret >= min_fret, the returned value equals self."""
        assert_typing(min_fret, Fret)
        if self._closed_fret_interval is None:
            return self
        m, M = self._closed_fret_interval
        min_fret = max(min_fret, m)
        return dataclasses.replace(self, _closed_fret_interval=(min_fret, M))
    
    def limit_max(self, max_fret: Fret) -> "Frets":
        """Restrict interval to fret at least max_fret. If self.max_fret >= max_fret, the returned value equals self."""
        assert_typing(max_fret, Fret)
        if self._closed_fret_interval is None:
            return self
        m, M = self.closed_fret_interval()
        max_fret = min(max_fret, M)
        return dataclasses.replace(self, _closed_fret_interval=(m, max_fret))
    
    def is_empty(self) -> bool:
        """Whether no note can be played"""
        return not self.allow_open and self._closed_fret_interval is None
    
    def is_contradiction(self) -> bool:
        """Whether no Fret oject satisfies this."""
        return self.is_empty() and not self.allow_not_played
    
    def __iter__(self) -> Generator[Fret]:
        if self.allow_not_played:
            yield self.instrument.fret(None)
        if self.allow_open:
            yield self.instrument.fret(0)
        if self._closed_fret_interval is not None:
            min_fret, max_fret = self.closed_fret_interval()
            yield from [self.instrument.fret(fret) for fret in range(max(min_fret.value, 1), max_fret.value + 1)]

    # def restrict_around(self, fret: Fret, interval_size: ChromaticInterval = ChromaticInterval(4)) -> "Frets":
    #     assert_typing(fret, Fret)
    #     assert_typing()
    #     if fret.value is None:
    #         return self
    #     return self.limit_max(fret + interval_size).limit_min(fret - interval_size)
    
    def svg(self, absolute: bool)-> List[str]:
        """
        The svg to display current frets.
        """
        return [svg for fret in self for svg in fret.svg(absolute)]
    
    @classmethod
    def empty(cls, instrument:FrettedInstrument):
        return cls(instrument, None, False, False)