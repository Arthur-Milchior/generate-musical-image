
from abc import abstractmethod
from dataclasses import dataclass

from solfege.value.interval.alteration.alteration import Alteration


@dataclass(frozen=True)
class IntervalAlteration(Alteration):
    
    @abstractmethod
    def letter(self) -> str:
        """The letter to display on guitar image"""

    @abstractmethod
    def name(self) -> str:
        """The name of this alteration"""

    def Name(self) -> str:
        return self.name().capitalize()

    def NAME(self) -> str:
        return self.name().upper()
