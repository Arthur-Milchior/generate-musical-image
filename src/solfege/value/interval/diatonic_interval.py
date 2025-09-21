
from dataclasses import dataclass
from typing import ClassVar
from solfege.value.diatonic import Diatonic
from solfege.value.interval.singleton_interval import AbstractSingletonInterval
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class DiatonicInterval(AbstractSingletonInterval, Diatonic):
    """An interval, where we count the number of note in the major scale,
    and ignore the note which are absent. B and B# can't be
    distinguished, since A# does not really exist. However, this would
    allow to distinguish between B# and C"""

    #Pragma mark - Singleton
    number_of_interval_in_an_octave: ClassVar[int] = 7

    #public

    def get_interval_name(self, showOctave=True):
        if self.value == 0:
            return "unison"
        if self.value < 0:
            increasing_name = (-self).get_interval_name(showOctave=showOctave)
            return f"{increasing_name} decreasing"
        note_in_base_octave = self.in_base_octave()
        octave = self.octave()
        text = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh"][note_in_base_octave.value]

        if octave > 0 and showOctave:
            prefix = f"{octave} octaves" if (octave > 1) else "octave"
            if note_in_base_octave.value != 0:
                text = f"{prefix} and {text}"
            else:
                text = prefix
        return text


DiatonicInterval.DiatonicClass = DiatonicInterval
Diatonic.IntervalClass = DiatonicInterval


class DiatonicIntervalFrozenList(FrozenList[DiatonicInterval]):
    type = DiatonicInterval