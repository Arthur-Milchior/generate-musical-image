
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.value.interval.set.list import ChromaticIntervalList, IntervalList
from utils.recordable import RecordedContainer


@dataclass(frozen=True)
class ChromaticIntervalListAndItsInversions(RecordedContainer[InversionPattern]):
    chromatic_intervals: ChromaticIntervalList
    inversions: List[InversionPattern] = field(default_factory=list)

    def append(self, inversion):
        self.inversions.append(inversion)

    def easiest_inversion(self):
        return min(self.inversions)
    
    def easiest_name(self):
        return self.easiest_inversion().name()
    
    def alternative_names(self):
        return ",".join(inversion.name() for inversion in self.inversions[1:])
    
    def __iter__(self):
        return iter(self.inversions)