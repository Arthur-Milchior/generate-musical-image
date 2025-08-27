from dataclasses import dataclass
from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.interval.chromatic_interval import ChromaticInterval


# The usage of name of the alternations


@dataclass(frozen=True)
class IntervalMode(ChromaticInterval):
    """Represents either bb, b, flat, #, or 𝄪.

    Raise in init for any other value."""

    def printable(self):
        """Whether the alteration is at most 2 halftone, and thus printable with at most 2 symbols."""
        number = self.value
        return number is not None and abs(number) <= 2

    def __post_init__(self):
        super().__post_init__()
        if not self.printable():
            raise TooBigAlterationException(self.value)

    def _add(self, other):
        raise Exception("Adding alteration ?")

    def in_base_octave(self):
        raise Exception("Alteration has no base octave")

ChromaticInterval.AlterationClass = IntervalMode
