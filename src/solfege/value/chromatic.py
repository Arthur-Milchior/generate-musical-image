from dataclasses import dataclass
from typing import ClassVar, Optional

from solfege.value.singleton import Singleton


@dataclass(frozen=True)
class Chromatic(Singleton):
    IntervalClass: ClassVar[type]
    number_of_interval_in_an_octave: ClassVar[int] = 12
    
    def get_chromatic(self):
        return self
    
    def get_diatonic(self):
        """If this note belong to the diatonic scale, give it.
        Otherwise, give the adjacent diatonic note."""
        return self.DiatonicClass([0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6][
                                             self.in_base_octave().value] + 7 * self.octave())

    def get_pair(self, diatonicNumber: Optional[int] = None):
        """A note. Same chromatic. Diatonic is as close as possible (see getDiatonicNote) or is the note given."""
        if diatonicNumber is None:
            diatonic = self.get_diatonic()
        return self.PairClass(diatonic=diatonic, chromatic=self)