from typing import ClassVar, Optional, Type
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chord.interval_list_to_chord_pattern import IntervalListToChordPattern
from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.interval_list_to_patterns import PatternType
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from solfege.pattern.chord.chord_patterns import dominant_seventh_chord

interval_to_inversion = IntervalListToInversionPattern.make()
interval_to_chord = IntervalListToChordPattern.make()

dominant_seventh_chord._associate_keys_to_self(record_keeper=interval_to_chord)

def make_inversion(inversion: int, interval_list: IntervalListPattern, base: ChordPattern, position_of_lowest_interval_in_base_octave, fifth_omitted:bool = False):
    position_of_lowest_interval_in_base_octave = Interval.make_single_argument(position_of_lowest_interval_in_base_octave)
    inversion_pattern = InversionPattern.make(inversion=inversion,
                                              base=base, interval_list=interval_list,
                                              fifth_omitted=fifth_omitted,
                                              position_of_lowest_interval_in_base_octave = position_of_lowest_interval_in_base_octave,
                                              record=False)
    #inversion_pattern._associate_intervals_to_self(interval_to_pattern=interval_to_inversion)
    return inversion_pattern

dominant_seventh_chord_zeroth_inversion = make_inversion(
    0,
    IntervalListPattern.make_absolute([(4, 2), (7, 4), (10, 6)]),
    dominant_seventh_chord,
    (0,0),
)
dominant_seventh_chord_first_inversion = make_inversion(
    1,
    IntervalListPattern.make_absolute([(3, 2), (6, 4), (8, 5)]),
    dominant_seventh_chord,
    (4, 2)
)
dominant_seventh_chord_second_inversion = make_inversion(
    2,
    IntervalListPattern.make_absolute([(3, 2), (5, 3), (9, 5)]),
    dominant_seventh_chord,
    (7, 4),
)
dominant_seventh_chord_third_inversion = make_inversion(
    3,
    IntervalListPattern.make_absolute([(2, 1), (6, 3), (9, 5)]),
    dominant_seventh_chord,
    (10, 6)
)
dominant_seventh_chord_no_fifth_zeroth_inversion = make_inversion(
    0,
    IntervalListPattern.make_absolute([(4, 2), (10, 6)]),
    dominant_seventh_chord,
    (0,0),
    fifth_omitted=True,
)
dominant_seventh_chord_no_fifth_first_inversion = make_inversion(
    1,
    IntervalListPattern.make_absolute([ (6, 4), (8, 5)]),
    dominant_seventh_chord,
    (4, 2),
    fifth_omitted=True,
)
dominant_seventh_chord_no_fifth_third_inversion = make_inversion(
    3,
    IntervalListPattern.make_absolute([(2, 1), (6, 3), ]),
    dominant_seventh_chord,
    (10, 6),
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
    inversion._associate_keys_to_self(record_keeper=interval_to_inversion)