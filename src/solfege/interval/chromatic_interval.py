from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TypeVar
from enum import Enum
from solfege.value.chromatic import Chromatic
from solfege.interval.singleton_interval import AbstractSingletonInterval
from utils.util import assert_typing

class IntervalNameCreasing(Enum):
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"
    DECREASING_ONLY = "DECREASING_ONLY"

@dataclass(frozen=True)
class ChromaticInterval(AbstractSingletonInterval, Chromatic):
    """A chromatic interval. Counting the number of half tone between two note"""
    number_of_interval_in_an_octave: ClassVar[int] = 12
    AlterationClass: ClassVar[type[ChromaticInterval]]  # more specific an alteration

    """the diatonic class to which such a chromatic class must be converted"""

    # DiatonicClass = solfege.Interval.diatonic.DiatonicInterval
    # moved to init because cyclic dependencies
    
    def __add__(self, other):
        assert_typing(other, Chromatic)
        return super().__add__(other)

    def get_interval_name(self, octave=True, side: IntervalNameCreasing=IntervalNameCreasing.NEVER):
        """The name of the interval.

        octave -- For example: if this variable is set true, the name is given as "supertonic and one octave".
        Otherwise, if it is set to None, the variable is given as "eight"

        side -- Whether to add "increasing" or "decreasing"
        """
        if self < unison:
            name = (-self).get_interval_name(octave=octave, side=False)
            if side != IntervalNameCreasing.NEVER:
                return name + " decreasing"
            else:
                return name
        if octave:
            nbOctave = self.octave()
            pos = self.value % 12
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
            if side == IntervalNameCreasing.ALWAYS and self.value != 0:
                name += " increasing"
            return name
        return NotImplemented


Chromatic.IntervalClass = ChromaticInterval
ChromaticInterval.ChromaticClass = ChromaticInterval

unison = ChromaticInterval(0)


ChromaticIntervalType = TypeVar('ChromaticIntervalType', bound=ChromaticInterval)