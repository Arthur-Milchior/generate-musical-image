
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.interval.interval_alteration import IntervalAlteration


@dataclass(frozen=True)
class MinorMajorAlteration(IntervalAlteration):

    #pragma mark - IntervalAlteration
    def letter(self) -> str:
        return ["d", "m", "M", "a"][self.value +2]

    def name(self) -> str:
        return ["diminished", "minor", "major", "augmented"][self.value +2]

    #pragma mark - Alteration

    min_value: ClassVar[int] = -2
    max_value: ClassVar[int] = 1

    #pragma mark - DataClassWithDefaultArgument
   
    def __post_init__(self):
        super().__post_init__()