from solfege.interval.chromatic import ChromaticInterval

# The usage of name of the alternations



class TooBigAlteration(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self):
        return "number %d corresponds to no Alteration.\n%s" % (self.value, super().__str__())


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
            raise TooBigAlteration(self.get_number())

    def __add__(self, other):
        raise Exception("Adding alteration ?")

    def get_in_base_octave(self):
        raise Exception("Alteration has no base octave")
