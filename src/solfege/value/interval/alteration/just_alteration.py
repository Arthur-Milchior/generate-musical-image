
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.interval.interval_alteration import IntervalAlteration


@dataclass(frozen=True)
class JustAlteration(IntervalAlteration):

    #pragma mark - IntervalAlteration
    def letter(self) -> str:
        return ["d", "", "a"][self.value + 1]

    def name(self) -> str:
        return ["diminished", "just", "augmented"][self.value + 1]

    #pragma mark - Alteration

    min_value: ClassVar[int] = -1
    max_value: ClassVar[int] = 1

    #pragma mark - DataClassWithDefaultArgument
   
    def __post_init__(self):
        super().__post_init__()