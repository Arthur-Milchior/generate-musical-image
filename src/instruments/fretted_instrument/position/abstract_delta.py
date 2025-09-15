from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, Optional, Self, Tuple, Type, TypeVar

from utils.util import T, assert_optional_typing, assert_typing

Ts = TypeVar("Ts")

@dataclass(frozen=True)
class AbstractDelta(ABC, Generic[Ts, T]):
    """
    If deltas is None, consider this as empty set.
    Otherwise, min_delta, max_delta = deltas.
    If min_delta is None, there is no lower bound limit, otherwise min_delta is the lower bound. Same for max bound. 
    """
    #Properties
    
    deltas: Optional[Tuple[Optional[int], Optional[int]]]

    #Must be implemented by subclasses

    type_t: ClassVar[Type]
    type_ts: ClassVar[Type]
    min_t: ClassVar[int]

    @classmethod
    @abstractmethod
    def max_t(cls, instrument: "FrettedInstrument") -> int:
        return NotImplemented

    @classmethod
    @abstractmethod
    def create_T(cls, instrument: "FrettedInstrument", i: int) -> T:
        return NotImplemented

    @classmethod
    @abstractmethod
    def create_Ts(cls, instrument: "FrettedInstrument", min: T, max: T) -> Ts:
        return NotImplemented

    @classmethod
    @abstractmethod
    def create_empty_ts(cls) -> Ts:
        return NotImplemented
    
    # Public

    def min(self, instrument: "FrettedInstrument", t: T) -> Optional[T]:
        """The minimal T that can be played, when delta is applied with reference point t. None if nothing can be played."""
        from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
        assert_typing(instrument, FrettedInstrument)
        assert_typing(t, self.type_t)
        if self.deltas is None:
            return None
        min_delta, max_delta = self.deltas
        if min_delta is None:
            return self.create_T(instrument, self.min_t)
        theoretical_min = t.value + min_delta
        if theoretical_min > self.max_t(instrument):
            return None
        return self.create_T(instrument, max(self.min_t, theoretical_min))

    def max(self, instrument: "FrettedInstrument", t: T) -> Optional[T]:
        """The maximal T that can be played, when delta is applied with reference point t. None if nothing can be played."""
        from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
        assert_typing(instrument, FrettedInstrument)
        assert_typing(t, self.type_t)
        if self.deltas is None:
            return None
        min_delta, max_delta = self.deltas
        if max_delta is None:
            return self.create_T(instrument, self.max_t(instrument))
        theoretical_max = t.value + max_delta
        if theoretical_max < self.min_t:
            return None
        new_max = min(self.max_t(instrument), theoretical_max)
        return self.create_T(instrument, new_max)
    
    def range(self, instrument: "FrettedInstrument", t: T) -> Ts:
        from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
        assert_typing(instrument, FrettedInstrument)
        assert_typing(t, self.type_t)
        min = self.min(instrument, t)
        max = self.max(instrument, t)
        if min is None or max is None:
            return self.create_empty_ts()
        return self.create_Ts(instrument, min, max)
    
    def __neg__(self) -> Self:
        if self.deltas is None:
            return self
        min_delta, max_delta = self.deltas
        return self.__class__((-max_delta, -min_delta))
    
    def contains_delta(self, delta: int):
        assert_typing(delta, int)
        if self.deltas is None:
            return False
        min_delta, max_delta = self.deltas

        if min_delta is not None:
            if min_delta > delta:
                return False
        
        if max_delta is not None:
            if max_delta < delta:
                return False
        return True

    
    #pragma mark - DataClass

    def __post_init__(self):
        if self.deltas is not None:
            min_delta, max_delta = self.deltas
            assert_optional_typing(min_delta, int)
            assert_optional_typing(max_delta, int)
