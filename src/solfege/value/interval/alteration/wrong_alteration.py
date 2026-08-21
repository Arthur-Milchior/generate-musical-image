
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.interval.interval_alteration import IntervalAlteration


@dataclass(frozen=True)
class WrongAlteration(IntervalAlteration):

    #pragma mark - IntervalAlteration
    def letter(self) -> str:
        return str(self.value + 1)

    def name(self) -> str:
        return str(self.value + 1)

    #pragma mark - Alteration

    min_value: ClassVar[int] = -12
    max_value: ClassVar[int] = 12

    #pragma mark - DataClassWithDefaultArgument
   
    def __post_init__(self):
        super().__post_init__()