from typing import Optional
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.interval_to_pattern import IntervalToPattern, PatternType
from solfege.value.interval.set.list import IntervalList
from solfege.pattern.chord.chord_patterns import dominant_seventh_chord

class FakeIntervalToPattern(IntervalToPattern[InversionPattern]):
    def register(self, pattern: InversionPattern, interval_list: Optional[IntervalList] = None):
        super().register(pattern, interval_list)


interval_to_inversion = FakeIntervalToPattern(InversionPattern)
interval_to_chord = IntervalToPattern[ChordPattern](ChordPattern)

dominant_seventh_chord._associate_intervals_to_self(interval_to_pattern=interval_to_chord)

def make_inversion(inversion: int, interval_list: IntervalList, base: ChordPattern, fifth_omitted:bool = False):
    inversion_pattern = InversionPattern.make(inversion=inversion,
                                              base=base, interval_list=interval_list,
                                              fifth_omitted=fifth_omitted,
                                              record=False)
    #inversion_pattern._associate_intervals_to_self(interval_to_pattern=interval_to_inversion)
    return inversion_pattern

dominant_seventh_chord_zeroth_inversion = make_inversion(
    0,
    IntervalList.make_absolute([(4, 2), (7, 4), (10, 6)]),
    dominant_seventh_chord
)
dominant_seventh_chord_first_inversion = make_inversion(
    1,
    IntervalList.make_absolute([(3, 2), (6, 4), (8, 5)]),
    dominant_seventh_chord
)
dominant_seventh_chord_second_inversion = make_inversion(
    2,
    IntervalList.make_absolute([(3, 2), (5, 3), (9, 5)]),
    dominant_seventh_chord
)
dominant_seventh_chord_third_inversion = make_inversion(
    3,
    IntervalList.make_absolute([(2, 1), (6, 3), (9, 5)]),
    dominant_seventh_chord
)
dominant_seventh_chord_no_fifth_zeroth_inversion = make_inversion(
    0,
    IntervalList.make_absolute([(4, 2), (10, 6)]),
    dominant_seventh_chord,
    fifth_omitted=True,
)
dominant_seventh_chord_no_fifth_first_inversion = make_inversion(
    1,
    IntervalList.make_absolute([ (6, 4), (8, 5)]),
    dominant_seventh_chord,
    fifth_omitted=True,
)
dominant_seventh_chord_no_fifth_third_inversion = make_inversion(
    3,
    IntervalList.make_absolute([(2, 1), (6, 3), ]),
    dominant_seventh_chord,
    fifth_omitted=True,
)

inversions = [dominant_seventh_chord_zeroth_inversion, 
              dominant_seventh_chord_no_fifth_zeroth_inversion,
              dominant_seventh_chord_first_inversion,
              dominant_seventh_chord_no_fifth_first_inversion,
              dominant_seventh_chord_second_inversion,
              dominant_seventh_chord_third_inversion,
              dominant_seventh_chord_no_fifth_third_inversion
              ]

for inversion in inversions:
    inversion._associate_intervals_to_self(interval_to_pattern=interval_to_inversion)