
from dataclasses import dataclass, field
from typing import List, TypeVar
from solfege.pattern.inversion.inversion_pattern import InversionPattern, InversionPatternGetter
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.recordable import RecordedContainer



class IdenticalInversionPatternGetter:
    def get_identical_inversion_pattern(self) -> "IdenticalInversionPattern":
        return NotImplemented
    
IdenticalInversionPatternGetterType = TypeVar("IdenticalInversionPatternGetterType", bound=IdenticalInversionPatternGetter)

@dataclass(frozen=True, unsafe_hash=True)
class IdentiticalInversionPatterns(RecordedContainer[InversionPattern], DataClassWithDefaultArgument):
    """A chromatic interval list and all chord inversion associated to it.
    
    It is the data entry for ChromaticIntervalListToInversion
    """
    chromatic_intervals: ChromaticIntervalListPattern
    inversions: List[InversionPattern] = field(default_factory=list, hash=False)

    def append(self, inversion: InversionPattern):
        expected = self.chromatic_intervals
        actuals = inversion.chromatic_interval_lists()
        assert expected in actuals, f"{expected} not in {actuals}"
        self.inversions.append(inversion)

    def easiest_inversion(self):
        return min(self.inversions)
    
    def easiest_name(self):
        return self.easiest_inversion().name()
    
    def alternative_names(self):
        return ",".join(inversion.name() for inversion in self.inversions[1:])
    
    def __iter__(self):
        return iter(self.inversions)
    
