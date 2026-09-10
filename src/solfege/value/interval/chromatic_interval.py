from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TypeVar
from enum import Enum
from solfege.value.chromatic import Chromatic
from solfege.value.getters import ChromaticGetter
from solfege.value.interval.singleton_interval import AbstractSingletonInterval
from utils.frozenlist import FrozenList
from utils.util import assert_typing

class IntervalNameCreasing(Enum):
    """Whether/how `get_interval_name` should indicate the interval's direction (increasing/decreasing)."""
    ALWAYS = "ALWAYS"
    """Always suffix the name with "increasing"/"decreasing"."""
    NEVER = "NEVER"
    """Never mention direction in the name."""
    DECREASING_ONLY = "DECREASING_ONLY"
    """Only suffix the name when the interval is decreasing."""

@dataclass(frozen=True, eq=False)
class ChromaticInterval(AbstractSingletonInterval, Chromatic):
    """A chromatic interval. Counting the number of half tone between two notes."""

    #Pragma mark - Singleton
    number_of_interval_in_an_octave: ClassVar[int] = 12
    """Chromatic intervals divide the octave into 12 semitones."""
    AlterationClass: ClassVar[type[ChromaticInterval]]  # more specific an alteration
    """The alteration class used to represent this interval's chromatic value as a sharp/flat count."""

    #Public

    def get_interval_name(self, octave: bool=True, side: IntervalNameCreasing=IntervalNameCreasing.NEVER) -> str:
        """The name of the interval.

        octave -- For example: if this variable is set true, the name is given as "supertonic and one octave".
        Otherwise, if it is set to None, the variable is given as "eight"

        side -- Whether to add "increasing" or "decreasing"
        """
        if self < self.unison():
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

ChromaticInterval.ChromaticClass = ChromaticInterval
Chromatic.IntervalClass = ChromaticInterval


ChromaticIntervalType = TypeVar('ChromaticIntervalType', bound=ChromaticInterval)
class ChromaticIntervalFrozenList(FrozenList[ChromaticInterval]):
    type = ChromaticInterval