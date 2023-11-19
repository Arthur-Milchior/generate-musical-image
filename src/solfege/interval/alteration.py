from solfege.interval.TooBigAlterationException import TooBigAlterationException
from solfege.interval.chromatic import ChromaticInterval


# The usage of name of the alternations


class Alteration(ChromaticInterval):
    """Represents either bb, b, flat, #, or 𝄪.

    Raise in init for any other value."""

    def printable(self):
        """Whether the alteration is at most 2 halftone, and thus printable with at most 2 symbols."""
        number = self.get_number()
        return number is not None and abs(number) <= 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.printable():
            raise TooBigAlterationException(self.get_number())

    def __add__(self, other):
        raise Exception("Adding alteration ?")

    def get_in_base_octave(self):
        raise Exception("Alteration has no base octave")
