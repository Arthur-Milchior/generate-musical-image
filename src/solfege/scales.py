"""Contains a class to represent a scale.

Also contains all scales from wikipedia, which can be done using the 12 notes from chromatic scales."""
import unittest

from solfege.interval import ChromaticInterval, DiatonicInterval
import sys

from .interval.interval import Interval
from .util import Solfege_Pattern


class ScalePattern(Solfege_Pattern):
    def __init__(self, names, intervals, flats=0, sharps=0):
        """
        intervals -- A list of intervals.
        An interval can be represented as:
        * A SolfegeInterval
        * A pair (diatonic, chromatic) representing SolfegeInterval(chromatic=chromatic, diatonic=diatonic)
        * An integral chromatic representing SolfegeInterval(chromatic=chromatic, diatonic=1)

        The sum of the SolfegeInterval should usually be SolfegeInterval(chromatic=12, diatonic=7)

        `flats`, `sharp` -- the number of `flats`/`sharps` on the key when the tonic is C."""

        super().__init__(names)
        # The sum of all the diatonic in the interval. It should ends on 7.
        self._diatonic_sum = 0
        # The sum of all the diatonic in the interval. It should ends on 12.
        self._chromatic_sum = 0
        self._intervals = []
        for interval in intervals:
            interval = Interval.factory(interval)
            self._intervals.append(interval)
            self._diatonic_sum += interval.get_diatonic().get_number()
            self._chromatic_sum += interval.get_chromatic().get_number()
        if self._diatonic_sum != 7:
            print(f"Warning: scale {names[0]} has a diatonic sum of {self._diatonic_sum}", file=sys.stderr)
        elif self._chromatic_sum != 12:
            print(f"Warning: scale {names[0]} has a chromatic sum of {self._chromatic_sum}", file=sys.stderr)
        self._flats = flats
        self._sharps = sharps

    def get_number_of_bemols(self):
        return self._flats

    def get_number_of_sharps(self):
        return self._sharps

    def get_intervals(self):
        return self._intervals

    def getChromaticIntervals(self):
        return [chromatic for (_, chromatic) in self._intervals]

    def getDiatonicInterval(self):
        return [diatonic for (diatonic, _) in self._intervals]

    def getNotes(self, tonic):
        """This scale starting at [tonic]"""
        return [tonic] + [tonic + interval for interval in self._intervals]


Solfege_Pattern.dic[ScalePattern] = dict()
Solfege_Pattern.set_[ScalePattern] = list()

ScalePattern(["Major arpeggio"], [(2, 4), (2, 3), (3, 5)], 0, 0),
ScalePattern(["Minor arpeggio"], [(2, 3), (2, 4), (3, 5)], 3, 0),
ScalePattern(["Greek Dorian tonos (chromatic genus)"], [1, 1, 3, 2, 1, 1, 3], 0, 0),
ScalePattern(["Major"], [2, 2, 1, 2, 2, 2, 1], 0, 0),
ScalePattern(["Dominant seventh arpeggio"], [(2, 4), (2, 3), (2, 3), 2], 0, 0),
ScalePattern(["Minor harmonic"], [2, 1, 2, 2, 1, 3, 1], 3, 0),
ScalePattern(["Blues"], [(2, 3), 2, (0, 1), 1, (2, 3), 2], 3, 0),
ScalePattern(["Pentatonic minor"], [(2, 3), 2, 2, (2, 3), 2], 3, 0),
ScalePattern(["Pentatonic major"], [2, 2, (2, 3), 2, (2, 3)], 0, 0),
ScalePattern(["Whole tone"], [(1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (2, 2)], 0, 1),
ScalePattern(["Chromatic"],
             [(0, 1), (1, 1), (0, 1), (1, 1), (1, 1), (0, 1), (1, 1), (0, 1), (1, 1), (0, 1), (1, 1), (1, 1), ], 0, 0),
ScalePattern(["Minor natural", "Aeolian mode"], [2, 1, 2, 2, 1, 2, 2], 3, 0),
ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], 3, 0),
ScalePattern(["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"], [2, 2, 2, 1, 2, 1, 2], 0, 1),
ScalePattern(["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],
             [1, 2, 1, 2, 2, 2, 2], 7, 0),
ScalePattern(["Augmented", ], [(2, 3), (0, 1), (2, 3), (0, 1), (2, 3), 1], 0, 0),
ScalePattern(["Prometheus", "Mystic chord"], [2, 2, 2, (2, 3), 1, 2], 1, 1),
ScalePattern(["Tritone", ], [1, 3, (2, 2), (0, 1), (2, 3), 2], 1, 0),
ScalePattern(["Bebop dominant", ], [2, 2, 1, 2, 2, 1, (0, 1), 1], 0, 0),
ScalePattern(["Bebop dorian", "Bebop minor"], [2, 1, (0, 1), 1, 2, 2, 1, 2, ], 1, 0),
ScalePattern(["Alternate bebop dorian"], [2, 1, 2, 2, 2, 1, (0, 1), 1, ], 2, 0),
ScalePattern(["Bebop major", ], [2, 2, 1, 2, (0, 1), 1, 2, 1], 0, 0),
ScalePattern(["Bebop melodic minor", ], [2, 1, 2, 2, (0, 1), 1, 2, 1], 0, 0),
ScalePattern(["Bebop harmonic minor", "Bebop natural minor"], [2, 1, 2, 2, 1, 2, (0, 1), 1], 3, 0),
ScalePattern(["Double harmonic major", "Byzantine", "Arabic", "Gypsi major"], [1, 3, 1, 2, 1, 3, 1], 0, 0),
ScalePattern(["Enigmatic"], [1, 3, 2, 2, 2, 1, 1], 0, 0),
ScalePattern(["Descending Enigmatic"], [1, 3, 1, 3, 2, 1, 1], 0, 0),
ScalePattern(["Flamenco mode"], [1, 3, 1, 2, 1, 3, 1], 0, 0),
ScalePattern(["Hungarian", "Hungarian Gypsy"], [2, 1, 3, 1, 1, 2, 2], 3, 0),
ScalePattern(["Half diminished"], [2, 1, 2, 1, 2, 2, 2], 5, 0),
ScalePattern(["Harmonic major"], [2, 2, 1, 2, 1, 3, 1], 0, 0),
ScalePattern(["Hirajōshi Burrows"], [(2, 4), 2, 1, (2, 4), 1], 0, 1),
ScalePattern(["Hirajōshi Sachs-Slonimsky"], [1, (2, 4), 1, (2, 4), 2], 0, 0),
ScalePattern(["Hirajōshi Kostka and Payne-Speed"], [2, 1, (2, 4), 1, (2, 4)], 0, 0),
ScalePattern(["Hungarian minor"], [2, 1, 3, 1, 1, 3, 1], 3, 1),
ScalePattern(["Greek Dorian tonos (diatonic genus)", "Phrygian mode"], [1, 2, 2, 2, 1, 2, 2], 3, 0),
ScalePattern(["Miyako-bushi"], [1, (2, 4), 2, 1, (2, 4)], 2, 0),
ScalePattern(["Insen"], [1, (2, 4), 2, (2, 3), 2], 4, 0),
ScalePattern(["Iwato"], [1, (2, 4), 1, (2, 4), 2], 5, 0),
ScalePattern(["Lydian augmented"], [2, 2, 2, 2, 1, 2, 1], 0, 3),
ScalePattern(["Major Locrian"], [2, 2, 1, 1, 2, 2, 2], 5, 0),
ScalePattern(["Minyo"], [(2, 3), 2, (2, 3), 2, 2], 0, 0),
ScalePattern(["Neapolitan minor"], [1, 2, 2, 2, 1, 3, 1], 4, 0),
ScalePattern(["Neapolitan major"], [1, 2, 2, 2, 2, 2, 1], 0, 0),
ScalePattern(["Pelog"], [1, 2, 3, 1, 1, 2, 2, ], 4, 0),
ScalePattern(["Pelog bem"], [1, (2, 5), 1, 1, (2, 4)], 4, 0),
ScalePattern(["Pelog barang"], [2, (2, 4), 1, 2, (2, 3)], 4, 0),
ScalePattern(["Persian"], [1, 3, 1, 1, 2, 3, 1], 5, 0),
ScalePattern(["Phrygian dominant"], [1, 3, 1, 2, 1, 2, 2], 4, 0),
ScalePattern(["Greek Phrygian tonos (diatonic genus)"], [2, 1, 2, 2, 2, 1, 2], 0, 0),
ScalePattern(["Greek Phrygian tonos (chromatic genus)"], [3, 1, 1, 2, 3, 1, 1], 0, 0),
ScalePattern(["Slendro"], [2, (2, 3), 2, 2, (2, 3)], 0, 0),
ScalePattern(["Two-semitone tritone"], [1, (0, 1), (2, 4), 1, 1, (2, 4)], 0, 0),
ScalePattern(["Ukrainian Dorian"], [2, 1, 3, 1, 2, 1, 2], 2, 1),
ScalePattern(["Misheberak"], [2, 1, 3, 1, 2, 1, 2], 0, 0),
ScalePattern(["Yo ascending"], [2, (2, 3), 2, (2, 3), 2], 2, 0),
ScalePattern(["Yo descending"], [2, (2, 3), 2, 2, (2, 3)], 2, 0),
ScalePattern(["Yo with auxiliary"], [2, 1, 2, 2, 2, 1, 2], 2, 0),
ScalePattern(["Dorian"], [2, 1, 2, 2, 2, 1, 2], 2, 0),
ScalePattern(["Locrian"], [1, 2, 2, 1, 2, 2, 2], 5, 0),
ScalePattern(["Lydian"], [2, 2, 2, 1, 2, 2, 1], 0, 1),
ScalePattern(["Greek Lydian tonos (diatonic genus)"], [2, 2, 1, 2, 2, 2, 1], 0, 0),
ScalePattern(["Greek Lydian tonos (chromatic genus)"], [1, 3, 1, 1, 3, 2, 1], 0, 0),
ScalePattern(["Mixolydian", "Adonal malakh mode"], [2, 2, 1, 2, 2, 1, 2], 1, 0),
ScalePattern(["Greek Mixolydian tonos (diatonic genus)"], [1, 2, 2, 1, 2, 2, 2], 0, 0),
ScalePattern(["Greek Mixolydian tonos (chromatic genus)"], [2, 1, 3, 1, 1, 3, 1], 0, 0),
ScalePattern(["Octave"], [(7, 12)], 0, 0),


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
    def test_minor(self):
        pat = ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], 3, 0)
        self.assertEquals(pat._flats, 3)
        self.assertEquals(pat._sharps, 0)
        self.assertEquals(pat._diatonic_sum, 7)
        self.assertEquals(pat._chromatic_sum, 12)
        self.assertEquals(pat._intervals, [
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=1, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=2, diatonic=1),
            Interval(chromatic=1, diatonic=1),
        ])
