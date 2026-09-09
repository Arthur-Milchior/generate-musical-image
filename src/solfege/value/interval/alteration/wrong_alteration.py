
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.interval.interval_alteration import IntervalAlteration


@dataclass(frozen=True)
class WrongAlteration(IntervalAlteration):
    """A placeholder alteration used when a real one would be out of range (e.g. a triple sharp/flat).
    Returned by `Pair.get_alteration(throw=False)` instead of raising `TooBigAlterationException`;
    its `letter()`/`name()` just print the raw offset since it has no proper musical name."""

    #pragma mark - IntervalAlteration
    def letter(self) -> str:
        """The raw 1-based offset as a string, since there's no proper letter for an out-of-range
        alteration."""
        return str(self.value + 1)

    def name(self) -> str:
        """Same as `letter()`: the raw 1-based offset as a string."""
        return str(self.value + 1)

    #pragma mark - Alteration

    min_value: ClassVar[int] = -12
    """Wide bound so almost any out-of-range value can still be wrapped instead of raising."""
    max_value: ClassVar[int] = 12
    """Wide bound so almost any out-of-range value can still be wrapped instead of raising."""

    #pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        """Delegates to the superclass chain (range validation happens in `Alteration.__post_init__`)."""
        super().__post_init__()