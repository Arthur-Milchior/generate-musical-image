from typing import Dict, Iterable, List, Optional, Tuple

from solfege.interval.interval import Interval, unison
from solfege.key import three_flats, five_flats, one_flat
from solfege.solfege_pattern import SolfegePattern
from solfege.interval.chromatic_interval import ChromaticInterval
from solfege.interval.set_of_intervals import SetOfIntervals
from utils.util import assert_all_same_class


def chord_to_arpeggio_name(name: str):
    if "chord" in name:
        return name.replace("chord", "arpeggio")
    if "triad" in name:
        return name.replace("triad", "arpeggio")
    else:
        return f"{name} arpeggio"


class ChordPattern(SolfegePattern):
    """A pattern describing a chord."""

    "Associate to a set of interval the chord it represents."
    set_of_interval_to_pattern: Dict[SetOfIntervals[Interval], "ChordPattern"] = dict()
    "associate to a set of chromatic interval the chord it represents."
    set_of_chromatic_interval_to_pattern: Dict[SetOfIntervals[ChromaticInterval], "ChordPattern"] = dict()

    """set of chromatic interval, between the tonic and a note of the chord."""
    _intervals: List[Interval]
    _intervals_without_fifth: List[Interval]

    """Whether the 5th is optional"""
    _optional_fifth: bool
    _interval_for_signature: Interval
    class_to_chord_patterns: Dict[type, List['ChordPattern']]
    """the notation representing the chord. E.g. "m" for "minor"."""
    notation: str
    """the list of names of this chord. Or a single name."""
    names:List[str]

    def __init__(self, names, notation: str, intervals: List[Tuple[int, int]], interval_for_signature: Interval, optional_fifth: bool = False,
                 ):
        """A sequence of interval between the tonic and the other note of this chord.
        
        Unison is not present in the param. Other intervals are presented as a pair of Chromatic, Diatonic
        """
        super().__init__(names)
        self.fifthOptional = optional_fifth
        self.notation = notation
        intervals = [(0, 0)] + intervals
        self._intervals = [Interval.make(chromatic, diatonic) for chromatic, diatonic in intervals]
        self._intervals_without_fifth = [
            interval for interval in self._intervals if interval.get_diatonic().value != 4]
        self._add(self._intervals)
        if optional_fifth:
            self._add(self._intervals_without_fifth)
        self._optional_fifth = optional_fifth
        self._interval_for_signature = interval_for_signature

    @classmethod
    def getFromInterval(cls, intervals: Iterable[Interval]):
        """Given a set of interval, return the object having this set of intervals."""
        assert_all_same_class(intervals)
        intervals = frozenset(intervals)
        return cls.set_of_interval_to_pattern.get(intervals)

    @classmethod
    def getFromChromaticInterval(cls, intervals: Iterable[Interval]) -> Optional["ChordPattern"]:
        """Given a set of interval, return the object having this set of intervals."""
        assert_all_same_class(intervals)
        intervals = frozenset(intervals)
        return cls.set_of_chromatic_interval_to_pattern.get(intervals)

    def _add(self, intervals: Iterable[Interval]):
        """ensure that, given the set of intervals, current object can be retrieved"""
        self.set_of_interval_to_pattern[frozenset(intervals)] = self
        self.set_of_chromatic_interval_to_pattern[frozenset(interval.get_chromatic() for interval in intervals)] = self

    def get_notes(self, base):
        return frozenset({base + interval for interval in self._intervals})

    def to_arpeggio_pattern(self):
        from solfege.scale.scale_pattern import ScalePattern
        intervals_of_the_scales = self._intervals + [Interval.make(chromatic=12, diatonic=7)]
        intervals_of_the_arpeggio = []
        for i in range(len(intervals_of_the_scales) - 1):
            intervals_of_the_arpeggio.append(intervals_of_the_scales[i + 1] - intervals_of_the_scales[i])

        return ScalePattern(relative_intervals=intervals_of_the_arpeggio,
                            names=[chord_to_arpeggio_name(name) for name in self.names],
                            notation = self.notation,
                            interval_for_signature=self._interval_for_signature, record=True)


major_triad = ChordPattern(["Major triad"], "M",
                           [(4, 2), (7, 4)], interval_for_signature=unison)
minor_triad = ChordPattern([ "Minor triad"], "m",
                           [(3, 2), (7, 4)], interval_for_signature=three_flats)
augmented_triad = ChordPattern(["Augmented triad"], "+",
                               [(4, 2), (8, 4)], interval_for_signature=unison)
diminished_triad = ChordPattern(["Diminished triad"], "-", 
                                [(3, 2), (6, 4)], interval_for_signature=five_flats)

minor_major_seventh_chord = ChordPattern(["Minor major seventh chord"], "m<sup>Δ</sup>",
                                         [(3, 2), (7, 4), (11, 6)], optional_fifth=True, interval_for_signature=three_flats)
augmented_major_seventh_chord = ChordPattern(["Augmented major seventh chord"], "+<sup>Δ7</sup>",
                                             [(4, 2), (8, 4), (11, 6)], interval_for_signature=unison)
diminished_major_seventh_chord = ChordPattern(["Diminished major seventh chord"], "<sup>oM7</sup>",
                                              [(3, 2), (6, 4), (11, 6)], interval_for_signature=five_flats)
half_diminished_seventh_chord = ChordPattern(
    ["Half-diminished seventh chord", "Half-diminished chord", "Minor seventh flat five"], "<sup>ø7</sup>",
    [(3, 2), (6, 4), (10, 6)], interval_for_signature=five_flats)
augmented_seventh_chord = ChordPattern(
    ["Augmented seventh chord", "seventh augmented fifth chord", "seventh sharp five chord"], "+<sup>7</sup>",
    [(4, 2), (8, 4), (10, 6)], interval_for_signature=one_flat)
dominant_seventh_flat_five_chord = ChordPattern(["Dominant seventh flat five chord"], "<sup>7♭5</sup>",
                                                [(4, 2), (6, 4), (10, 6)], interval_for_signature=five_flats)
dominant_seventh_chord = ChordPattern(["Dominant seventh chord", "major minor seventh chord"], "<sup>7</sup>",
                                      [(4, 2), (7, 4), (10, 6)], optional_fifth=True,
                                      interval_for_signature=one_flat)
major_seventh_chord = ChordPattern(["Major seventh chord"], "<sup>Δ</sup>",
                                   [(4, 2), (7, 4), (11, 6)], optional_fifth=True, interval_for_signature=unison)
major_seventh_flat_five_chord = ChordPattern(["Major seventh flat five chord"],  "<sup>7♭5</sup>",
                                             [(4, 2), (6, 4), (11, 6)], optional_fifth=True, interval_for_signature=unison)
minor_seven = ChordPattern(["Minor seventh chord"], "-<sup>7</sup>",
                           [(3, 2), (7, 4), (10, 6)], optional_fifth=True, interval_for_signature=three_flats)

triad_patterns = [major_triad, minor_triad, augmented_triad, diminished_triad]
fourad_patterns = [minor_major_seventh_chord, augmented_seventh_chord, diminished_major_seventh_chord,
                   half_diminished_seventh_chord, augmented_major_seventh_chord, dominant_seventh_chord,
                   dominant_seventh_flat_five_chord, major_seventh_chord, major_seventh_flat_five_chord, minor_seven]

chord_patterns = triad_patterns + fourad_patterns

def add_arpeggios_to_scales():
    print("Arpeggios added to scales")
    for chord in ChordPattern.class_to_patterns[ChordPattern]:
        chord.to_arpeggio_pattern()
