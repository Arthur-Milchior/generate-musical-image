
from abc import abstractmethod
from dataclasses import dataclass

from solfege.value.interval.alteration.alteration import Alteration


@dataclass(frozen=True)
class IntervalAlteration(Alteration):
    """Base for the alteration attached to an `Interval`'s diatonic degree (e.g. minor/major, or
    diminished/just/augmented, depending on the degree). See `JustAlteration` and
    `MinorMajorAlteration` for the concrete subclasses used by `Interval.get_alteration_constructor`."""

    @abstractmethod
    def letter(self) -> str:
        """The letter to display on guitar image"""

    @abstractmethod
    def name(self) -> str:
        """The name of this alteration"""

    def Name(self) -> str:
        """`name()` with its first letter capitalized."""
        return self.name().capitalize()

    def NAME(self) -> str:
        """`name()` fully upper-cased."""
        return self.name().upper()
