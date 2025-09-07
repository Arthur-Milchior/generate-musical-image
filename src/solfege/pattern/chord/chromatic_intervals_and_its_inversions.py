
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.recordable import RecordedContainer


@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIntervalListAndItsInversions(RecordedContainer[InversionPattern], DataClassWithDefaultArgument):
    chromatic_intervals: ChromaticIntervalList
    inversions: List[InversionPattern] = field(default_factory=list, hash=False)

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