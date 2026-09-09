
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.interval.interval_alteration import IntervalAlteration


@dataclass(frozen=True)
class MinorMajorAlteration(IntervalAlteration):
    """The alteration used for imperfect diatonic degrees (second, third, sixth, seventh), which have
    diminished/minor/major/augmented forms. `value` ranges from -2 (diminished) to 1 (augmented),
    -1 being minor and 0 being major."""

    #pragma mark - IntervalAlteration
    def letter(self) -> str:
        """"d"/"m"/"M"/"a" for diminished/minor/major/augmented."""
        return ["d", "m", "M", "a"][self.value +2]

    def name(self) -> str:
        """"diminished"/"minor"/"major"/"augmented"."""
        return ["diminished", "minor", "major", "augmented"][self.value +2]

    #pragma mark - Alteration

    min_value: ClassVar[int] = -2
    """-2: diminished is the smallest value."""
    max_value: ClassVar[int] = 1
    """1: augmented is the largest value."""

    #pragma mark - DataClassWithDefaultArgument

    def __post_init__(self):
        """Delegates to the superclass chain (range validation happens in `Alteration.__post_init__`)."""
        super().__post_init__()