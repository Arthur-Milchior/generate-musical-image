from dataclasses import dataclass
from typing import ClassVar, Generic, Optional, Self, TypeVar

from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from utils.util import assert_optional_typing, assert_typing

T = TypeVar("T")
Ts = TypeVar("Ts")

@dataclass(frozen=True)
class AbstractDelta(Generic[Ts, T]):
    instrument: FrettedInstrument
    min_delta: Optional[int]= None
    max_delta: Optional[int]= None

    min_t: ClassVar[int]
    max_t: ClassVar[int]

    def __post_init__(self):
        assert_optional_typing(self.min_delta, int)
        assert_optional_typing(self.max_delta, int)

    @classmethod
    def create_T(cls, instrument: FrettedInstrument, i: int) -> T:
        return NotImplemented

    @classmethod
    def create_Ts(cls, instrument: FrettedInstrument, min: T, max: T) -> Ts:
        return NotImplemented
    
    @classmethod
    def create_empty_ts(cls, instrument: FrettedInstrument) -> Ts:
        return NotImplemented

    def min(self, t: T) -> Optional[T]:
        if self.min_delta is None:
            return self.create_T(self.instrument, self.min_t)
        theoretical_min = t.value + self.min_delta
        if theoretical_min > self.max_t:
            return None
        return self.create_T(self.instrument, max(self.min_t, theoretical_min))

    def max(self, t: T) -> Optional[T]:
        if self.max_delta is None:
            return self.create_T(self.instrument, self.max_t)
        theoretical_max = t.value + self.max_delta
        if theoretical_max < self.min_t:
            return None
        new_max = min(self.max_t, theoretical_max)
        return self.create_T(self.instrument, new_max)
    
    def set(self, t: T) -> Ts:
        min = self.min(t)
        max = self.max(t)
        if min is None or max is None:
            return self.create_empty_ts(self.instrument)
        return self.create_Ts(self.instrument, min, max)
    
    def __neg__(self) -> Self:
        return self.__class__(self.instrument, -self.max_delta, -self.min_delta)
    
    def contains_delta(self, delta: int):
        assert_typing(delta, int)
        if self.min_delta is not None:
            if self.min_delta > delta:
                return False
        
        if self.max_delta is not None:
            if self.max_delta < delta:
                return False
        return True
