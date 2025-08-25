
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.diatonic import Diatonic
from solfege.interval.singleton_interval import AbstractSingletonInterval
from utils.util import assert_typing


@dataclass(frozen=True)
class DiatonicInterval(AbstractSingletonInterval, Diatonic):
    """An interval, where we count the number of note in the major scale,
    and ignore the note which are absent. B and B# can't be
    distinguished, since A# does not really exist. However, this would
    allow to distinguish between B# and C"""
    number_of_interval_in_an_octave: ClassVar[int] = 7

    def get_interval_name(self, showOctave=True):
        if self.value == 0:
            return "unison"
        size = abs(self.value)
        role = size % 7
        nb_octave = size // 7
        text = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh"][role]

        if nb_octave > 0 and showOctave:
            prefix = f"{nb_octave} octaves" if (nb_octave > 1) else "octave"
            if role != 0:
                text = f"{prefix} and {text}"
            else:
                text = prefix
        if self.value < 0:
            text += " decreasing"
        return text


Diatonic.IntervalClass = DiatonicInterval
DiatonicInterval.DiatonicClass = DiatonicInterval


