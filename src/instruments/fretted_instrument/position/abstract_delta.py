from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, Optional, Self, Tuple, Type, TypeVar

from utils.util import T, assert_optional_typing, assert_typing

Ts = TypeVar("Ts")

@dataclass(frozen=True)
class AbstractDelta(ABC, Generic[Ts, T]):
    """
    Common base for `FretDelta` and `StringDelta`: an allowed range of *offsets* from a reference point (a fret
    or a string), rather than an absolute range like `Frets`/`Strings`.

    If deltas is None, consider this as empty set.
    Otherwise, min_delta, max_delta = deltas.
    If min_delta is None, there is no lower bound limit, otherwise min_delta is the lower bound. Same for max bound.
    """
    #Properties

    deltas: Optional[Tuple[Optional[int], Optional[int]]]
    """`(min_delta, max_delta)`, each possibly `None` for "no bound", or `None` itself for "empty set" (see class
    docstring). Values are offsets to add to a reference `T` (e.g. a fret or string number)."""

    #Must be implemented by subclasses

    type_t: ClassVar[Type]
    """The single-value type this delta is applied to/from (e.g. `Fret`, `String`)."""
    type_ts: ClassVar[Type]
    """The range/collection type this delta resolves to (e.g. `Frets`, `Strings`)."""
    min_t: ClassVar[int]
    """The smallest valid raw value of `type_t` (independent of any instrument), used to clamp lower bounds."""

    @classmethod
    @abstractmethod
    def max_t(cls, instrument: "FrettedInstrument") -> int:
        """The largest valid raw value of `type_t` on `instrument` (e.g. the instrument's last fret), used to clamp upper bounds."""
        ...
    @classmethod
    @abstractmethod
    def create_T(cls, instrument: "FrettedInstrument", i: int, origine: T) -> T:
        """Build a concrete `T` (e.g. `Fret`/`String`) with raw value `i`, in the context of `instrument` and the reference point `origine`."""
        ...
    @classmethod
    @abstractmethod
    def create_Ts(cls, instrument: "FrettedInstrument", min: T, max: T, origine: T) -> Ts:
        """Build the `Ts` range/collection (e.g. `Frets`/`Strings`) spanning from `min` to `max`, relative to `origine`."""
        ...
    @classmethod
    @abstractmethod
    def create_empty_ts(cls) -> Ts:
        """Build the empty `Ts` range/collection, used when the delta resolves to no valid value."""
        ...
    # Public

    def min(self, instrument: "FrettedInstrument", origine: T) -> Optional[T]:
        """The minimal T that can be played, when delta is applied with reference point t. None if nothing can be played."""
        from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
        assert_typing(instrument, FrettedInstrument)
        assert_typing(origine, self.type_t)
        if self.deltas is None:
            return None
        min_delta, max_delta = self.deltas
        if min_delta is None:
            return self.create_T(instrument, self.min_t, origine=origine)
        theoretical_min = origine.value + min_delta
        instrument_max_fret = self.max_t(instrument)
        if theoretical_min > instrument_max_fret:
            return None
        return self.create_T(instrument, max(self.min_t, theoretical_min), origine=origine)

    def max(self, instrument: "FrettedInstrument", origine: T) -> Optional[T]:
        """The maximal T that can be played, when delta is applied with reference point t. None if nothing can be played."""
        from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
        assert_typing(instrument, FrettedInstrument)
        assert_typing(origine, self.type_t)
        if self.deltas is None:
            return None
        min_delta, max_delta = self.deltas
        if max_delta is None:
            return self.create_T(instrument, self.max_t(instrument), origine=origine)
        theoretical_max = origine.value + max_delta
        if theoretical_max < self.min_t:
            return None
        new_max = min(self.max_t(instrument), theoretical_max)
        return self.create_T(instrument, new_max, origine=origine)
    
    def range(self, instrument: "FrettedInstrument", t: T) -> Ts:
        """The full `Ts` range reachable from reference point `t` on `instrument` when this delta is applied
        (i.e. `create_Ts` between `self.min(instrument, t)` and `self.max(instrument, t)`), or the empty `Ts` if
        either bound is unreachable."""
        from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
        assert_typing(instrument, FrettedInstrument)
        assert_typing(t, self.type_t)
        min = self.min(instrument, t)
        max = self.max(instrument, t)
        if min is None or max is None:
            return self.create_empty_ts()
        return self.create_Ts(instrument, min, max, t)

    def __neg__(self) -> Self:
        """The delta describing the opposite offset (swap and negate min/max), used when a relation is read from
        the other endpoint (e.g. the delta from finger B to finger A given the delta from A to B)."""
        if self.deltas is None:
            return self
        min_delta, max_delta = self.deltas
        return self.__class__((-max_delta, -min_delta))

    def contains_delta(self, delta: int):
        """Whether the raw integer offset `delta` falls within `[min_delta, max_delta]` (unbounded sides always match, and an empty delta set matches nothing)."""
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
        """Validate that `deltas`, when not `None`, is a pair of optional ints."""
        if self.deltas is not None:
            min_delta, max_delta = self.deltas
            assert_optional_typing(min_delta, int)
            assert_optional_typing(max_delta, int)
