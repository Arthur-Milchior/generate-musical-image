"""Shared test fixtures for the chord/inversion tests: a fresh pair of record keepers (`interval_to_chord`,
`interval_to_inversion`) plus every inversion (fifth included and omitted) of `dominant_seventh_chord`,
pre-built and pre-registered so tests can assert against them without relying on the app-wide catalog."""

from typing import ClassVar, Optional, Tuple, Type, Union
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern.chord.interval_list_to_chord_pattern import IntervalListToChordPattern
from solfege.pattern.inversion.interval_list_to_inversion_pattern import IntervalListToInversionPattern
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern.interval_list_to_pattern import PatternType
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import IntervalList
from solfege.pattern.chord.chord_patterns import dominant_seventh_chord
from utils.util import assert_typing

interval_to_inversion = IntervalListToInversionPattern.make()
interval_to_chord = IntervalListToChordPattern.make()

dominant_seventh_chord._associate_keys_to_self(record_keeper=interval_to_chord)

def make_inversion(inversion: int, base: ChordPattern, tonic_minus_lowest_note: Union[Interval, Tuple[int, int]], fifth_omitted:bool = False) -> InversionPattern:
    """Build (without recording) an `InversionPattern` of `base` -- a lower-level, more direct constructor than
    `ChordPattern.inversion()`, letting the test fixtures pass `tonic_minus_lowest_note` explicitly rather than
    computing it from the chord's interval list."""
    assert_typing(inversion, int)
    assert_typing(base, ChordPattern)
    assert_typing(fifth_omitted, bool)
    tonic_minus_lowest_note = Interval.make_single_argument(tonic_minus_lowest_note)
    inversion_pattern = InversionPattern.make(inversion=inversion,
                                              base=base, 
                                              fifth_omitted=fifth_omitted,
                                              tonic_minus_lowest_note = tonic_minus_lowest_note,
                                              record=False)
    #inversion_pattern._associate_intervals_to_self(interval_to_pattern=interval_to_inversion)
    return inversion_pattern

dominant_seventh_chord_zeroth_inversion = make_inversion(
    0,
    dominant_seventh_chord,
    (0,0),
)
dominant_seventh_chord_first_inversion = make_inversion(
    1,
    dominant_seventh_chord,
    (4, 2)
)
dominant_seventh_chord_second_inversion = make_inversion(
    2,
    dominant_seventh_chord,
    (7, 4),
)
dominant_seventh_chord_third_inversion = make_inversion(
    3,
    dominant_seventh_chord,
    (10, 6)
)
dominant_seventh_chord_no_fifth_zeroth_inversion = make_inversion(
    0,
    dominant_seventh_chord,
    (0,0),
    fifth_omitted=True,
)
dominant_seventh_chord_no_fifth_first_inversion = make_inversion(
    1,
    dominant_seventh_chord,
    (4, 2),
    fifth_omitted=True,
)
dominant_seventh_chord_no_fifth_third_inversion = make_inversion(
    3,
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