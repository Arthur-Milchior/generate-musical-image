from __future__ import annotations

from typing import Optional
from enum import Enum
from solfege.interval.abstract import AbstractInterval
from solfege.interval.too_big_alterations_exception import TooBigAlterationException

class IntervalNameCreasing(Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    DECREASING_ONLY = "DECREASING_ONLY"

class ChromaticInterval(AbstractInterval):
    """A chromatic interval. Counting the number of half tone between two note"""
    number_of_interval_in_an_octave = 12
    AlterationClass: type[ChromaticInterval]  # more specific an alteration

    """the diatonic class to which such a chromatic class must be converted"""

    # RelatedDiatonicClass = solfege.Interval.diatonic.DiatonicInterval
    # moved to init because cyclic dependencies

    def __add__(self, other):
    # No idea why this check does not work. But self is a solfege.interval.chromatic.ChromaticInterval while other is a solfege.interval.chromatic.ChromaticInterval , note the src
        if not isinstance(other, ChromaticInterval.clazz):
            raise Exception(
                f"Adding a ChromaticInterval {self}: {self.__class__}: {self.__class__.__bases__} interval to something which is not a ChromaticInterval but {other}: {other.clazz}")
        return super().__add__(other)

    def get_diatonic(self):
        """If this note belong to the diatonic scale, give it.
        Otherwise, give the adjacent diatonic note."""
        return self.RelatedDiatonicClass([0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6][
                                             self.get_in_base_octave().get_number()] + 7 * self.get_octave())

    def get_alteration(self) -> ChromaticInterval:
        """The alteration, added to `self.getDiatonic()` to obtain `self`"""
        import solfege.interval.intervalmode
        diatonic = self.get_diatonic()
        chromatic_from_diatonic = diatonic.get_chromatic()
        try:
            return self.AlterationClass(self.get_number() - chromatic_from_diatonic.get_number())
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

    def get_solfege(self, diatonicNumber: Optional[int] = None):
        """A note. Same chromatic. Diatonic is as close as possible (see getDiatonicNote) or is the note given."""
        if diatonicNumber is None:
            diatonic = self.get_diatonic().get_number()
        return self.RelatedSolfegeClass(diatonic=diatonic, chromatic=self.get_number())

    def get_interval_name(self, octave=True, side: IntervalNameCreasing=IntervalNameCreasing.NEVER):
        """The name of the interval.

        octave -- For example: if this variable is set true, the name is given as "supertonic and one octave".
        Otherwise, if it is set to None, the variable is given as "eight"

        side -- Whether to add "increasing" or "decreasing"
        """
        if self < 0:
            name = (-self).get_interval_name(octave=octave, side=False)
            if side != IntervalNameCreasing.NEVER:
                return name + " decreasing"
            else:
                return name
        if octave:
            nbOctave = self.get_octave()
            pos = self.get_number() % 12
            if nbOctave > 1:
                octave_name = "%d octaves" % nbOctave
            elif nbOctave == 1:
                octave_name = "octave"
            else:
                octave_name = ""
            mode_name = \
                ["" if nbOctave else "unison", "second minor", "second major", "third minor", "third major", "fourth",
                 "tritone", "fifth", "sixth minor", "sixth major", "seventh minor", "seventh major"][pos]
            if octave_name and mode_name:
                name = f"{octave_name} and {mode_name}"
            else:
                name = octave_name or mode_name
            if side == IntervalNameCreasing.ALWAYS and self.get_number() != 0:
                name += " increasing"
            return name
        return NotImplemented


ChromaticInterval.IntervalClass = ChromaticInterval
ChromaticInterval.clazz = ChromaticInterval


