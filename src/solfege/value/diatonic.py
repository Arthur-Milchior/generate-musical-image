
from dataclasses import dataclass
from typing import ClassVar

from solfege.value.singleton import Singleton
from solfege.value.chromatic import Chromatic
from utils.util import assert_typing


@dataclass(frozen=True)
class Diatonic(Singleton):
    IntervalClass: ClassVar[type]
    number_of_interval_in_an_octave: ClassVar[int] = 7

    def get_chromatic(self, scale="Major") -> Chromatic:
        """
        Give the chromatic interval associated to the current diatonic interval in some scale.
        By default, the scale is the major one."""
        # TODO scale= scale.dic[scale] currently, only major is used
        assert (scale == "Major")
        assert_typing(self, Diatonic)
        return self.ChromaticClass(12 * self.octave() + [0, 2, 4, 5, 7, 9, 11][self.value % 7])
    
    def get_diatonic(self):
        return self