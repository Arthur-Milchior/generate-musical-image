from typing import ClassVar, List, Type

from solfege.pattern.scale.chromatic_interval_list_to_scale_pattern import ChromaticIntervalListToScalePattern
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.pattern.interval_list_to_pattern import IntervalListToPattern
from solfege.value.interval.set.interval_list import ChromaticIntervalListPattern, IntervalList
from utils.recording.singleton_container import SameKeyBehavior, SingletonContainer

class IntervalListToScalePattern(IntervalListToPattern[ScalePattern]):
    #pragma mark - RecordKeeper
    _recorded_type: ClassVar[Type] = ScalePattern

    def is_key_valid(self, key: ChromaticIntervalListPattern):
        return key.is_in_base_octave(accepting_octave=True)
    
    @classmethod
    def _new_container(self, key: IntervalList) -> SingletonContainer[ScalePattern]:
        return SingletonContainer[ScalePattern](same_key_behavior=SameKeyBehavior.IMPOSSIBLE)

    #pragma mark - IntervalListToPatterns    
    @classmethod
    def make_chromatic_record_keeper(self):
        return ChromaticIntervalListToScalePattern.make()
    
