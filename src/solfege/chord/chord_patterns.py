
from .chord_pattern import ChordPattern
from solfege.key.key import *

major_triad = ChordPattern.make_absolute(names=["Major triad"], notation="M",
                           absolute_intervals=[(4, 2), (7, 4)], interval_for_signature=nor_flat_nor_sharp)
minor_triad = ChordPattern.make_absolute(names=[ "Minor triad"], notation="m",
                           absolute_intervals=[(3, 2), (7, 4)], interval_for_signature=three_flats)
augmented_triad = ChordPattern.make_absolute(names=["Augmented triad"], notation="+",
                               absolute_intervals=[(4, 2), (8, 4)], interval_for_signature=nor_flat_nor_sharp)
diminished_triad = ChordPattern.make_absolute(names=["Diminished triad"], notation="-", 
                                absolute_intervals=[(3, 2), (6, 4)], interval_for_signature=five_flats)

minor_major_seventh_chord = ChordPattern.make_absolute(names=["Minor major seventh chord"], notation="m<sup>Δ</sup>",
                                         absolute_intervals=[(3, 2), (7, 4), (11, 6)], optional_fifth=True, interval_for_signature=three_flats)
augmented_major_seventh_chord = ChordPattern.make_absolute(names=["Augmented major seventh chord"], notation="+<sup>Δ7</sup>",
                                             absolute_intervals=[(4, 2), (8, 4), (11, 6)], interval_for_signature=nor_flat_nor_sharp)
diminished_major_seventh_chord = ChordPattern.make_absolute(names=["Diminished major seventh chord"], notation="<sup>oM7</sup>",
                                              absolute_intervals=[(3, 2), (6, 4), (11, 6)], interval_for_signature=five_flats)
half_diminished_seventh_chord = ChordPattern.make_absolute(
    names=["Half-diminished seventh chord", "Half-diminished chord", "Minor seventh flat five"], notation="<sup>ø7</sup>",
    absolute_intervals=[(3, 2), (6, 4), (10, 6)], interval_for_signature=five_flats)
augmented_seventh_chord = ChordPattern.make_absolute(
    names=["Augmented seventh chord", "seventh augmented fifth chord", "seventh sharp five chord"], notation="+<sup>7</sup>",
    absolute_intervals=[(4, 2), (8, 4), (10, 6)], interval_for_signature=one_flat)
dominant_seventh_flat_five_chord = ChordPattern.make_absolute(names=["Dominant seventh flat five chord"], notation="<sup>7♭5</sup>",
                                                absolute_intervals=[(4, 2), (6, 4), (10, 6)], interval_for_signature=five_flats)
dominant_seventh_chord = ChordPattern.make_absolute(names=["Dominant seventh chord", "major minor seventh chord"], notation="<sup>7</sup>",
                                      absolute_intervals=[(4, 2), (7, 4), (10, 6)], optional_fifth=True,
                                      interval_for_signature=one_flat)
major_seventh_chord = ChordPattern.make_absolute(names=["Major seventh chord"], notation="<sup>Δ</sup>",
                                   absolute_intervals=[(4, 2), (7, 4), (11, 6)], optional_fifth=True, interval_for_signature=nor_flat_nor_sharp)
major_seventh_flat_five_chord = ChordPattern.make_absolute(names=["Major seventh flat five chord"], notation="<sup>7♭5</sup>",
                                             absolute_intervals=[(4, 2), (6, 4), (11, 6)], optional_fifth=True, interval_for_signature=nor_flat_nor_sharp)
minor_seven = ChordPattern.make_absolute(names=["Minor seventh chord"], notation="-<sup>7</sup>",
                           absolute_intervals=[(3, 2), (7, 4), (10, 6)], optional_fifth=True, interval_for_signature=three_flats)

"""Patterns with three notes"""
triad_patterns = [major_triad, minor_triad, augmented_triad, diminished_triad]
"""Patterns with four notes"""
fourad_patterns = [minor_major_seventh_chord, augmented_seventh_chord, diminished_major_seventh_chord,
                   half_diminished_seventh_chord, augmented_major_seventh_chord, dominant_seventh_chord,
                   dominant_seventh_flat_five_chord, major_seventh_chord, major_seventh_flat_five_chord, minor_seven]

"""All patterns"""
chord_patterns = triad_patterns + fourad_patterns
