
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.interval.interval_alteration import IntervalAlteration


@dataclass(frozen=True)
class JustAlteration(IntervalAlteration):
    """The alteration used for "perfect" diatonic degrees (unison, fourth, fifth), which only have
    diminished/just/augmented forms — no minor/major distinction. `value` ranges from -1 (diminished)
    to 1 (augmented), 0 being just."""

    #pragma mark - IntervalAlteration
    def letter(self) -> str:
        """"d"/""/"a" for diminished/just/augmented."""
        return ["d", "", "a"][self.value + 1]

    def name(self) -> str:
        """"diminished"/"just"/"augmented"."""
        return ["diminished", "just", "augmented"][self.value + 1]

    #pragma mark - Alteration

    min_value: ClassVar[int] = -1
    """-1: diminished is the smallest value."""
    max_value: ClassVar[int] = 1
    """1: augmented is the largest value."""

    #pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        """Delegates to the superclass chain (range validation happens in `Alteration.__post_init__`)."""
        super().__post_init__()