from __future__ import annotations

from typing import List, Generic, Union, Tuple, Optional

from solfege.chord.chord_pattern import chord_patterns
from solfege.key import nor_flat_nor_sharp, three_flats, one_sharp, seven_sharps, one_flat, two_flats, five_flats, \
    four_flats, three_sharps
from solfege.scale.scale import Scale
from solfege.interval.abstract import IntervalType
from solfege.note import Note
from solfege.note.abstract import NoteType

"""Contains a class to represent a scale.

Also contains all scales from wikipedia, which can be done using the 12 note from chromatic scales."""
import unittest

import sys

from solfege.interval.interval import Interval
from solfege.solfege_pattern import SolfegePattern


class ScalePattern(SolfegePattern, Generic[IntervalType]):
    _intervals: List[IntervalType]

    def __init__(self, names, intervals: List[Union[IntervalType, int, Tuple[int, int]]],
                 interval_for_signature: Interval,
                 increasing=True, suppress_warning: bool = False, descending: Optional[ScalePattern]=None , **kwargs):
        """
        intervals -- A list of intervals.
        An interval can be represented as:
        * A Interval
        * A pair (diatonic, chromatic) representing Interval(chromatic=chromatic, diatonic=diatonic)
        * An integral chromatic representing Interval(chromatic=chromatic, diatonic=1)

        The sum of the Interval should usually be Interval(chromatic=12, diatonic=7)


        Interval - the interval of difference between the key-signature and the first note.
        E.g. for a Minor scale, it would be Interval(chromatic=3, diatonic=2), as it's the way to go from A to C.
        I.e. to play A minor, you use the signature of C major."""

        assert isinstance(interval_for_signature, Interval)

        super().__init__(names, **kwargs)
        # The sum of all the diatonic in the interval. It should ends on 7.
        self._diatonic_sum = 0
        # The sum of all the diatonic in the interval. It should ends on 12.
        self._chromatic_sum = 0
        self._intervals = []
        if descending:
            self.descending = descending
        else:
            self.descending = self
        for interval in intervals:
            interval = Interval.factory(interval)
            self._intervals.append(interval)
            self._diatonic_sum += interval.get_diatonic().get_number()
            self._chromatic_sum += interval.get_chromatic().get_number()
        if self._diatonic_sum % 7 and not suppress_warning:
            print(f"Warning: scale {names[0]} has a diatonic sum of {self._diatonic_sum}", file=sys.stderr)
        elif self._chromatic_sum % 12 and not suppress_warning:
            print(f"Warning: scale {names[0]} has a chromatic sum of {self._chromatic_sum}", file=sys.stderr)
        self.interval_for_signature = interval_for_signature
        self.increasing = increasing

    def __repr__(self):
        return f"""ScalePattern(names={self.names}, intervals={self._intervals}, interval_for_signature={self.interval_for_signature}{", increasing=True" if self.increasing else ""})"""

    def __eq__(self, other: ScalePattern):
        return (self.names == other.names and self._intervals == other._intervals
                and self.interval_for_signature == other.interval_for_signature and self.increasing == other.increasing)

    def get_intervals(self):
        return self._intervals

    def get_chromatic_intervals(self):
        return [chromatic for (_, chromatic) in self._intervals]

    def get_diatonic_intervals(self):
        return [diatonic for (diatonic, _) in self._intervals]

    def get_notes(self, tonic):
        """This scale starting at [tonic]"""
        scale = [tonic]
        last_note = tonic
        for interval in self._intervals:
            last_note += interval
            scale.append(last_note)
        return scale

    def __neg__(self):
        return ScalePattern(names=self.names, intervals=[-interval for interval in reversed(self._intervals)],
                            interval_for_signature=self.interval_for_signature, increasing=not self.increasing,
                            record=False)

    def generate(self, fundamental: NoteType, number_of_octaves=1,
                 add_an_extra_note: bool = False) -> Scale[NoteType]:
        """The note, starting at tonic, following this pattern for nb_octave.
        If nb_octave is negative, the generated scale is decreasing."""
        assert number_of_octaves != 0
        if number_of_octaves < 0:
            return (-self).generate(fundamental, -number_of_octaves, add_an_extra_note=add_an_extra_note)
        current_note = fundamental
        notes = [fundamental]
        for _ in range(number_of_octaves):
            for interval in self._intervals:
                current_note += interval
                notes.append(current_note)
        if add_an_extra_note:
            notes.append(notes[-1] + self._intervals[0])
        return Scale[NoteType](notes=notes, pattern=self, key = notes[0] + self.interval_for_signature)

    def number_of_intervals(self):
        return len(self._intervals)

# ré b, mi bb, f, g, a b, b bb, c

major_scale = ScalePattern[Interval](["Major"], [2, 2, 1, 2, 2, 2, 1], nor_flat_nor_sharp)
blues = ScalePattern[Interval](["Blues"], [(3, 2), 2, (1, 0), 1, (3, 2), 2], three_flats)
minor_harmonic = ScalePattern[Interval](["Minor harmonic"], [2, 1, 2, 2, 1, 3, 1], three_flats)
pentatonic_minor = ScalePattern[Interval](["Pentatonic minor"], [(3, 2), 2, 2, (3, 2), 2],
                                          three_flats)
pentatonic_major = ScalePattern[Interval](["Pentatonic major"], [2, 2, (3, 2), 2, (3, 2)], nor_flat_nor_sharp)
whole_tone = ScalePattern[Interval](["Whole tone"], [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 2)], one_sharp)
chromatic_scale_pattern = ScalePattern[Interval](["Chromatic"],
                                                 [(1, 0), (1, 1), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0),
                                                  (1, 1), (1, 0), (1, 1),
                                                  (1, 1), ], nor_flat_nor_sharp)
minor_natural = ScalePattern[Interval](["Minor natural", "Aeolian mode"], [2, 1, 2, 2, 1, 2, 2], three_flats)
minor_melodic = ScalePattern[Interval](["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], three_flats, descending=minor_natural)

scale_patterns_I_practice = [major_scale, blues, minor_natural, minor_harmonic, minor_melodic, chromatic_scale_pattern,
                             whole_tone, pentatonic_major, pentatonic_minor] + [chord_pattern.to_arpeggio_pattern() for
                                                                                chord_pattern in chord_patterns]

scale_patterns = scale_patterns_I_practice + [
    ScalePattern[Interval](["Greek Dorian tonos (chromatic genus)"], [1, 1, 3, 2, 1, 1, 3],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"], [2, 2, 2, 1, 2, 1, 2], one_sharp),
    ScalePattern[Interval](
        ["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],
        [1, 2, 1, 2, 2, 2, 2], seven_sharps),
    ScalePattern[Interval](["Augmented", ], [(3, 2), (1, 0), (3, 2), (1, 0), (3, 2), 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Prometheus", "Mystic chord"], [2, 2, 2, (3, 2), 1, 2],
                           nor_flat_nor_sharp),  # one flat one sharp, can't decide
    ScalePattern[Interval](["Tritone", ], [1, 3, (2, 2), (1, 0), (3, 2), 2], one_flat),
    ScalePattern[Interval](["Bebop dominant", ], [2, 2, 1, 2, 2, 1, (1, 0), 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Bebop dorian", "Bebop minor"], [2, 1, (1, 0), 1, 2, 2, 1, 2, ], nor_flat_nor_sharp),
    ScalePattern[Interval](["Alternate bebop dorian"], [2, 1, 2, 2, 2, 1, (1, 0), 1, ], two_flats),
    ScalePattern[Interval](["Bebop major", ], [2, 2, 1, 2, (1, 0), 1, 2, 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Bebop melodic minor", ], [2, 1, 2, 2, (1, 0), 1, 2, 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Bebop harmonic minor", "Bebop natural minor"], [2, 1, 2, 2, 1, 2, (1, 0), 1],
                           three_flats),
    ScalePattern[Interval](["Double harmonic major", "Byzantine", "Arabic", "Gypsi major"], [1, 3, 1, 2, 1, 3, 1],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Enigmatic"], [1, 3, 2, 2, 2, 1, 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Descending Enigmatic"], [1, 3, 1, 3, 2, 1, 1], nor_flat_nor_sharp),
    # ScalePattern[Interval](["Flamenco mode"], [1, 3, 1, 2, 1, 3, 1], unison) can't find anymore on wp
    ScalePattern[Interval](["Hungarian", "Hungarian Gypsy"], [2, 1, 3, 1, 1, 2, 2], three_flats),
    ScalePattern[Interval](["Half diminished"], [2, 1, 2, 1, 2, 2, 2], five_flats),
    ScalePattern[Interval](["Harmonic major"], [2, 2, 1, 2, 1, 3, 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Hirajōshi Burrows"], [(4, 2), 2, 1, (4, 2), 1], one_sharp),
    ScalePattern[Interval](["Hirajōshi Sachs-Slonimsky"], [1, (4, 2), 1, (4, 2), 2], nor_flat_nor_sharp),
    ScalePattern[Interval](["Hirajōshi Kostka and Payne-Speed"], [2, 1, (4, 2), 1, (4, 2)],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Hungarian minor"], [2, 1, 3, 1, 1, 3, 1], three_flats),  # should also have one sharp
    ScalePattern[Interval](["Greek Dorian tonos (diatonic genus)", "Phrygian mode"], [1, 2, 2, 2, 1, 2, 2],
                           three_flats),
    ScalePattern[Interval](["Miyako-bushi"], [1, (4, 2), 2, 1, (4, 2)], two_flats),
    ScalePattern[Interval](["Insen"], [1, (4, 2), 2, (3, 2), 2], four_flats),
    ScalePattern[Interval](["Iwato"], [1, (4, 2), 1, (4, 2), 2], five_flats),
    ScalePattern[Interval](["Lydian augmented"], [2, 2, 2, 2, 1, 2, 1], three_sharps),
    ScalePattern[Interval](["Major Locrian"], [2, 2, 1, 1, 2, 2, 2], five_flats),
    ScalePattern[Interval](["Minyo"], [(3, 2), 2, (3, 2), 2, 2], nor_flat_nor_sharp),
    ScalePattern[Interval](["Neapolitan minor"], [1, 2, 2, 2, 1, 3, 1], four_flats),
    ScalePattern[Interval](["Neapolitan major"], [1, 2, 2, 2, 2, 2, 1], nor_flat_nor_sharp),
    ScalePattern[Interval](["Pelog"], [1, 2, 3, 1, 1, 2, 2, ], four_flats),
    ScalePattern[Interval](["Pelog bem"], [1, (5, 2), 1, 1, (4, 2)], four_flats),
    ScalePattern[Interval](["Pelog barang"], [2, (4, 2), 1, 2, (3, 2)], four_flats),
    ScalePattern[Interval](["Persian"], [1, 3, 1, 1, 2, 3, 1], five_flats),
    ScalePattern[Interval](["Phrygian dominant"], [1, 3, 1, 2, 1, 2, 2], four_flats),
    ScalePattern[Interval](["Greek Phrygian tonos (diatonic genus)"], [2, 1, 2, 2, 2, 1, 2],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Greek Phrygian tonos (chromatic genus)"], [3, 1, 1, 2, 3, 1, 1],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Slendro"], [2, (3, 2), 2, 2, (3, 2)], nor_flat_nor_sharp),
    ScalePattern[Interval](["Two-semitone tritone"], [1, (1, 0), (4, 2), 1, 1, (4, 2)], nor_flat_nor_sharp),
    ScalePattern[Interval](["Ukrainian Dorian"], [2, 1, 3, 1, 2, 1, 2], two_flats),  # shold also have one sharp
    ScalePattern[Interval](["Misheberak"], [2, 1, 3, 1, 2, 1, 2], nor_flat_nor_sharp),
    ScalePattern[Interval](["Yo ascending"], [2, (3, 2), 2, (3, 2), 2], two_flats),
    ScalePattern[Interval](["Yo descending"], [2, (3, 2), 2, 2, (3, 2)], two_flats),
    ScalePattern[Interval](["Yo with auxiliary"], [2, 1, 2, 2, 2, 1, 2], two_flats),
    ScalePattern[Interval](["Dorian"], [2, 1, 2, 2, 2, 1, 2], two_flats),
    ScalePattern[Interval](["Locrian"], [1, 2, 2, 1, 2, 2, 2], five_flats),
    ScalePattern[Interval](["Lydian"], [2, 2, 2, 1, 2, 2, 1], one_sharp),
    ScalePattern[Interval](["Greek Lydian tonos (diatonic genus)"], [2, 2, 1, 2, 2, 2, 1],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Greek Lydian tonos (chromatic genus)"], [1, 3, 1, 1, 3, 2, 1],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Mixolydian", "Adonal malakh mode"], [2, 2, 1, 2, 2, 1, 2], one_flat),
    ScalePattern[Interval](["Greek Mixolydian tonos (diatonic genus)"], [1, 2, 2, 1, 2, 2, 2],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Greek Mixolydian tonos (chromatic genus)"], [2, 1, 3, 1, 1, 3, 1],
                           nor_flat_nor_sharp),
    ScalePattern[Interval](["Octave"], [(12, 7)], nor_flat_nor_sharp)
]


# Ignored=[
#     "Bohlen-Pierce",
#     "alpha",
#     "Beta",
#     "Delta",
#     "Gamma",
#     "Istrian",
#      "Pfluke",
#     "Non-Pythagorean",
# ]
# (["Algerian"],
#  [2,1,3,1,1,3,1,1, 2,1,2,2,1,3,1,1]),
# (["Greek Dorian tonos (enharmonic genus)"],[0,1,4,2,0,1,4]),
# (["Greek Lydian tonos (enharmonic genus)"],[1,]),
# (["Medieval Lydian mode"],[2,2,2,1,0,2,2,1]),
# (["Greek Mixolydian tonos (enharmonic genus)"],[1,0,1,4,]),
# (["Vietnamese scale of harmonics"],[3,0,1,1,2,5]),
# (["Octatonic"],[2,1,2,1,2,1,2,1]),
# (["Greek Phrygian tonos (enharmonic genus)"],[4,1,0, 2, 4,1,0]),
# (["Medieval Phrygian mode"],[2,2,2,1,0,1,2,2]),
# (["Hypophrygian mode"],[2,2,1,2,0,1,2]),
# (["Harmonic"],0,0,[3,1,1,2,2,3]),

class TestScalePattern(unittest.TestCase):

    def test_ne(self):
        self.assertNotEquals(minor_melodic,
                             ScalePattern[Interval](["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], four_flats))
        self.assertNotEquals(minor_melodic, ScalePattern[Interval](["Minor melodic"], [2, 1, 2, 2, 2, 2],
                                                                   three_flats, suppress_warning=False))
        self.assertNotEquals(minor_melodic, ScalePattern[Interval](["Minor"], [2, 1, 2, 2, 2, 2, 1],
                                                                   three_flats))

    def test_eq(self):
        self.assertEquals(minor_melodic.interval_for_signature, three_flats)
        self.assertEquals(minor_melodic._diatonic_sum, 7)
        self.assertEquals(minor_melodic._chromatic_sum, 12)
        self.assertEquals(minor_melodic._intervals, [
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=1, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=1, diatonic=1),
        ])

    def test_get_notes(self):
        tonic = Note(diatonic=0, chromatic=0)
        self.assertEquals(minor_melodic.get_notes(tonic),
                          [
                              Note(diatonic=0, chromatic=0),
                              Note(diatonic=1, chromatic=2),
                              Note(diatonic=2, chromatic=3),
                              Note(diatonic=3, chromatic=5),
                              Note(diatonic=4, chromatic=7),
                              Note(diatonic=5, chromatic=9),
                              Note(diatonic=6, chromatic=11),
                              Note(diatonic=7, chromatic=12),
                          ])

    def test_neg(self):
        reversed = -minor_melodic
        expected = ScalePattern[Interval](["Minor melodic"],
                                          [
                                              Interval(diatonic=-1, chromatic=- 1),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-2),
                                              Interval(diatonic=-1, chromatic=-1),
                                              Interval(diatonic=-1, chromatic=-2)], three_flats, increasing=False,
                                          record=False)
        self.assertEquals(reversed,
                          expected)

    def test_generate(self):
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=2, diatonic=1),
            Note(chromatic=3, diatonic=2),
            Note(chromatic=5, diatonic=3),
            Note(chromatic=7, diatonic=4),
            Note(chromatic=9, diatonic=5),
            Note(chromatic=11, diatonic=6),
            Note(chromatic=12, diatonic=7),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0))
        self.assertEquals(expected, generated)

    def test_generate_two(self):
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=2, diatonic=1),
            Note(chromatic=3, diatonic=2),
            Note(chromatic=5, diatonic=3),
            Note(chromatic=7, diatonic=4),
            Note(chromatic=9, diatonic=5),
            Note(chromatic=11, diatonic=6),
            Note(chromatic=12, diatonic=7),
            Note(chromatic=14, diatonic=8),
            Note(chromatic=15, diatonic=9),
            Note(chromatic=17, diatonic=10),
            Note(chromatic=19, diatonic=11),
            Note(chromatic=21, diatonic=12),
            Note(chromatic=23, diatonic=13),
            Note(chromatic=24, diatonic=14),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=2)
        self.assertEquals(expected, generated)
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=2, diatonic=1),
            Note(chromatic=3, diatonic=2),
            Note(chromatic=5, diatonic=3),
            Note(chromatic=7, diatonic=4),
            Note(chromatic=9, diatonic=5),
            Note(chromatic=11, diatonic=6),
            Note(chromatic=12, diatonic=7),
            Note(chromatic=14, diatonic=8),
            Note(chromatic=15, diatonic=9),
            Note(chromatic=17, diatonic=10),
            Note(chromatic=19, diatonic=11),
            Note(chromatic=21, diatonic=12),
            Note(chromatic=23, diatonic=13),
            Note(chromatic=24, diatonic=14),
            Note(chromatic=26, diatonic=15),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=2, add_an_extra_note=True)
        self.assertEquals(expected, generated)

    def test_generate_minus_two(self):
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=-1, diatonic=-1),
            Note(chromatic=-3, diatonic=-2),
            Note(chromatic=-5, diatonic=-3),
            Note(chromatic=-7, diatonic=-4),
            Note(chromatic=-9, diatonic=-5),
            Note(chromatic=-10, diatonic=-6),
            Note(chromatic=-12, diatonic=-7),
            Note(chromatic=-13, diatonic=-8),
            Note(chromatic=-15, diatonic=-9),
            Note(chromatic=-17, diatonic=-10),
            Note(chromatic=-19, diatonic=-11),
            Note(chromatic=-21, diatonic=-12),
            Note(chromatic=-22, diatonic=-13),
            Note(chromatic=-24, diatonic=-14),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=-2)
        self.assertEquals(expected, generated)
        expected = Scale(notes=[
            Note(chromatic=0, diatonic=0),
            Note(chromatic=-1, diatonic=-1),
            Note(chromatic=-3, diatonic=-2),
            Note(chromatic=-5, diatonic=-3),
            Note(chromatic=-7, diatonic=-4),
            Note(chromatic=-9, diatonic=-5),
            Note(chromatic=-10, diatonic=-6),
            Note(chromatic=-12, diatonic=-7),
            Note(chromatic=-13, diatonic=-8),
            Note(chromatic=-15, diatonic=-9),
            Note(chromatic=-17, diatonic=-10),
            Note(chromatic=-19, diatonic=-11),
            Note(chromatic=-21, diatonic=-12),
            Note(chromatic=-22, diatonic=-13),
            Note(chromatic=-24, diatonic=-14),
            Note(chromatic=-25, diatonic=-15),
        ], pattern=minor_melodic)
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), number_of_octaves=-2, add_an_extra_note=True)
        self.assertEquals(expected, generated)

    def test_number_of_intervals(self):
        self.assertEquals(minor_melodic.number_of_intervals(), 7)
        self.assertEquals(pentatonic_minor.number_of_intervals(), 5)
