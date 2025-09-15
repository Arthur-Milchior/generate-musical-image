

# from typing import ClassVar, List, Type
# from solfege.pattern.inversion.chromatic_interval_list_to_inversion_pattern import ChromaticIntervalListToInversionPattern
# from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
# from solfege.pattern.inversion.inversion_pattern import InversionPattern
# from solfege.pattern.interval_list_to_patterns import IntervalListToPatterns
# from solfege.value.interval.set.interval_list_pattern import IntervalListPattern


# class IntervalListToIdenticalInversionPattern(IntervalListToPatterns[InversionPattern, list, IdenticalInversionPatterns]):
#     """Associate to each interval list all inversions that are related."""

#     #pragma mark - RecordKeeper
#     _recorded_type: ClassVar[Type] = InversionPattern
#     _recorded_container_type: ClassVar[Type] = list
#     _chromatic_recorded_container_type: ClassVar[Type] = IdenticalInversionPatterns

#     def is_key_valid(self, key: IntervalListPattern):
#         return key.is_in_base_octave()
    
#     @classmethod
#     def _new_container(self, key: IntervalListPattern) -> List[InversionPattern]:
#         return list()
    
#     #pragma mark - IntervalListToPatterns
#     @classmethod
#     def make_chromatic_record_keeper(self):
#         return ChromaticIntervalListToIdenticalInversionPattern.make()
    
