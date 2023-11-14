from __future__ import annotations

from solfege.Scale.scale import Scale
from solfege.note import Note
from solfege.note.base import AbstractNote

"""Contains a class to represent a scale.

Also contains all scales from wikipedia, which can be done using the 12 notes from chromatic scales."""
import unittest

import sys

from solfege.interval.interval import Interval
from solfege.note.with_tonic import NoteWithTonic
from solfege.solfege_pattern import SolfegePattern


class ScalePattern(SolfegePattern):
    def __init__(self, names, intervals, flats=0, sharps=0, increasing=True, **kwargs):
        """
        intervals -- A list of intervals.
        An interval can be represented as:
        * A SolfegeInterval
        * A pair (diatonic, chromatic) representing SolfegeInterval(chromatic=chromatic, diatonic=diatonic)
        * An integral chromatic representing SolfegeInterval(chromatic=chromatic, diatonic=1)

        The sum of the SolfegeInterval should usually be SolfegeInterval(chromatic=12, diatonic=7)

        `flats`, `sharp` -- the number of `flats`/`sharps` on the key when the tonic is C."""

        super().__init__(names, **kwargs)
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
        if self._diatonic_sum % 7:
            print(f"Warning: scale {names[0]} has a diatonic sum of {self._diatonic_sum}", file=sys.stderr)
        elif self._chromatic_sum % 12:
            print(f"Warning: scale {names[0]} has a chromatic sum of {self._chromatic_sum}", file=sys.stderr)
        self._flats = flats
        self._sharps = sharps
        self.increasing = increasing

    def __repr__(self):
        return f"ScalePattern(names={self.names}, intervals={self._intervals}, flats={self._flats}, sharps{self._sharps}, increasing={self.increasing})"

    def __eq__(self, other: ScalePattern):
        return (self.names == other.names and self._intervals == other._intervals and self._flats == other._flats
                and self._sharps == other._sharps and self.increasing == other.increasing)

    def get_number_of_bemols(self):
        return self._flats

    def get_number_of_sharps(self):
        return self._sharps

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
                            flats=self._flats, sharps=self._sharps, increasing=not self.increasing, record=False)

    def generate(self, tonic: AbstractNote, nb_octave=1):
        """The notes, starting at tonic, following this pattern for nb_octave.
        If nb_octave is negative, the generated scale is decreasing."""
        assert nb_octave != 0
        if nb_octave < 0:
            return (-self).generate(tonic, -nb_octave)
        current_note = tonic
        notes = [tonic]
        for _ in range(nb_octave):
            for interval in self._intervals:
                current_note += interval
                notes.append(current_note)
        return Scale(notes=notes)


ScalePattern(["Major arpeggio"], [(4, 2), (3, 2), (5, 3)], 0, 0)
ScalePattern(["Minor arpeggio"], [(3, 2), (4, 2), (5, 3)], 3, 0)
ScalePattern(["Greek Dorian tonos (chromatic genus)"], [1, 1, 3, 2, 1, 1, 3], 0, 0)
ScalePattern(["Major"], [2, 2, 1, 2, 2, 2, 1], 0, 0)
ScalePattern(["Dominant seventh arpeggio"], [(4, 2), (3, 2), (3, 2), 2], 0, 0)
ScalePattern(["Minor harmonic"], [2, 1, 2, 2, 1, 3, 1], 3, 0)
ScalePattern(["Blues"], [(3, 2), 2, (1, 0), 1, (3, 2), 2], 3, 0)
ScalePattern(["Pentatonic minor"], [(3, 2), 2, 2, (3, 2), 2], 3, 0)
ScalePattern(["Pentatonic major"], [2, 2, (3, 2), 2, (3, 2)], 0, 0)
ScalePattern(["Whole tone"], [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 2)], 0, 1)
ScalePattern(["Chromatic"],
             [(1, 0), (1, 1), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 1), ], 0, 0)
ScalePattern(["Minor natural", "Aeolian mode"], [2, 1, 2, 2, 1, 2, 2], 3, 0)
minor_melodic = ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], 3, 0)
ScalePattern(["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"], [2, 2, 2, 1, 2, 1, 2], 0, 1)
ScalePattern(["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],
             [1, 2, 1, 2, 2, 2, 2], 7, 0)
ScalePattern(["Augmented", ], [(3, 2), (1, 0), (3, 2), (1, 0), (3, 2), 1], 0, 0)
ScalePattern(["Prometheus", "Mystic chord"], [2, 2, 2, (3, 2), 1, 2], 1, 1)
ScalePattern(["Tritone", ], [1, 3, (2, 2), (1, 0), (3, 2), 2], 1, 0)
ScalePattern(["Bebop dominant", ], [2, 2, 1, 2, 2, 1, (1, 0), 1], 0, 0)
ScalePattern(["Bebop dorian", "Bebop minor"], [2, 1, (1, 0), 1, 2, 2, 1, 2, ], 1, 0)
ScalePattern(["Alternate bebop dorian"], [2, 1, 2, 2, 2, 1, (1, 0), 1, ], 2, 0)
ScalePattern(["Bebop major", ], [2, 2, 1, 2, (1, 0), 1, 2, 1], 0, 0)
ScalePattern(["Bebop melodic minor", ], [2, 1, 2, 2, (1, 0), 1, 2, 1], 0, 0)
ScalePattern(["Bebop harmonic minor", "Bebop natural minor"], [2, 1, 2, 2, 1, 2, (1, 0), 1], 3, 0)
ScalePattern(["Double harmonic major", "Byzantine", "Arabic", "Gypsi major"], [1, 3, 1, 2, 1, 3, 1], 0, 0)
ScalePattern(["Enigmatic"], [1, 3, 2, 2, 2, 1, 1], 0, 0)
ScalePattern(["Descending Enigmatic"], [1, 3, 1, 3, 2, 1, 1], 0, 0)
ScalePattern(["Flamenco mode"], [1, 3, 1, 2, 1, 3, 1], 0, 0)
ScalePattern(["Hungarian", "Hungarian Gypsy"], [2, 1, 3, 1, 1, 2, 2], 3, 0)
ScalePattern(["Half diminished"], [2, 1, 2, 1, 2, 2, 2], 5, 0)
ScalePattern(["Harmonic major"], [2, 2, 1, 2, 1, 3, 1], 0, 0)
ScalePattern(["Hirajōshi Burrows"], [(4, 2), 2, 1, (4, 2), 1], 0, 1)
ScalePattern(["Hirajōshi Sachs-Slonimsky"], [1, (4, 2), 1, (4, 2), 2], 0, 0)
ScalePattern(["Hirajōshi Kostka and Payne-Speed"], [2, 1, (4, 2), 1, (4, 2)], 0, 0)
ScalePattern(["Hungarian minor"], [2, 1, 3, 1, 1, 3, 1], 3, 1)
ScalePattern(["Greek Dorian tonos (diatonic genus)", "Phrygian mode"], [1, 2, 2, 2, 1, 2, 2], 3, 0)
ScalePattern(["Miyako-bushi"], [1, (4, 2), 2, 1, (4, 2)], 2, 0)
ScalePattern(["Insen"], [1, (4, 2), 2, (3, 2), 2], 4, 0)
ScalePattern(["Iwato"], [1, (4, 2), 1, (4, 2), 2], 5, 0)
ScalePattern(["Lydian augmented"], [2, 2, 2, 2, 1, 2, 1], 0, 3)
ScalePattern(["Major Locrian"], [2, 2, 1, 1, 2, 2, 2], 5, 0)
ScalePattern(["Minyo"], [(3, 2), 2, (3, 2), 2, 2], 0, 0)
ScalePattern(["Neapolitan minor"], [1, 2, 2, 2, 1, 3, 1], 4, 0)
ScalePattern(["Neapolitan major"], [1, 2, 2, 2, 2, 2, 1], 0, 0)
ScalePattern(["Pelog"], [1, 2, 3, 1, 1, 2, 2, ], 4, 0)
ScalePattern(["Pelog bem"], [1, (5, 2), 1, 1, (4, 2)], 4, 0)
ScalePattern(["Pelog barang"], [2, (4, 2), 1, 2, (3, 2)], 4, 0)
ScalePattern(["Persian"], [1, 3, 1, 1, 2, 3, 1], 5, 0)
ScalePattern(["Phrygian dominant"], [1, 3, 1, 2, 1, 2, 2], 4, 0)
ScalePattern(["Greek Phrygian tonos (diatonic genus)"], [2, 1, 2, 2, 2, 1, 2], 0, 0)
ScalePattern(["Greek Phrygian tonos (chromatic genus)"], [3, 1, 1, 2, 3, 1, 1], 0, 0)
ScalePattern(["Slendro"], [2, (3, 2), 2, 2, (3, 2)], 0, 0)
ScalePattern(["Two-semitone tritone"], [1, (1, 0), (4, 2), 1, 1, (4, 2)], 0, 0)
ScalePattern(["Ukrainian Dorian"], [2, 1, 3, 1, 2, 1, 2], 2, 1)
ScalePattern(["Misheberak"], [2, 1, 3, 1, 2, 1, 2], 0, 0)
ScalePattern(["Yo ascending"], [2, (3, 2), 2, (3, 2), 2], 2, 0)
ScalePattern(["Yo descending"], [2, (3, 2), 2, 2, (3, 2)], 2, 0)
ScalePattern(["Yo with auxiliary"], [2, 1, 2, 2, 2, 1, 2], 2, 0)
ScalePattern(["Dorian"], [2, 1, 2, 2, 2, 1, 2], 2, 0)
ScalePattern(["Locrian"], [1, 2, 2, 1, 2, 2, 2], 5, 0)
ScalePattern(["Lydian"], [2, 2, 2, 1, 2, 2, 1], 0, 1)
ScalePattern(["Greek Lydian tonos (diatonic genus)"], [2, 2, 1, 2, 2, 2, 1], 0, 0)
ScalePattern(["Greek Lydian tonos (chromatic genus)"], [1, 3, 1, 1, 3, 2, 1], 0, 0)
ScalePattern(["Mixolydian", "Adonal malakh mode"], [2, 2, 1, 2, 2, 1, 2], 1, 0)
ScalePattern(["Greek Mixolydian tonos (diatonic genus)"], [1, 2, 2, 1, 2, 2, 2], 0, 0)
ScalePattern(["Greek Mixolydian tonos (chromatic genus)"], [2, 1, 3, 1, 1, 3, 1], 0, 0)
ScalePattern(["Octave"], [(12, 7)], 0, 0)


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
        self.assertNotEquals(minor_melodic, ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], 3, 1))
        self.assertNotEquals(minor_melodic, ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], 4, 0))
        self.assertNotEquals(minor_melodic, ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2], 3, 0))
        self.assertNotEquals(minor_melodic, ScalePattern(["Minor"], [2, 1, 2, 2, 2, 2, 1], 3, 0))

    def test_eq(self):
        self.assertEquals(minor_melodic._flats, 3)
        self.assertEquals(minor_melodic._sharps, 0)
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
        tonic = NoteWithTonic(diatonic=0, chromatic=0, tonic=True)
        self.assertEquals(minor_melodic.get_notes(tonic),
                          [
                              NoteWithTonic(diatonic=0, chromatic=0, tonic=tonic),
                              NoteWithTonic(diatonic=1, chromatic=2, tonic=tonic),
                              NoteWithTonic(diatonic=2, chromatic=3, tonic=tonic),
                              NoteWithTonic(diatonic=3, chromatic=5, tonic=tonic),
                              NoteWithTonic(diatonic=4, chromatic=7, tonic=tonic),
                              NoteWithTonic(diatonic=5, chromatic=9, tonic=tonic),
                              NoteWithTonic(diatonic=6, chromatic=11, tonic=tonic),
                              NoteWithTonic(diatonic=7, chromatic=12, tonic=tonic),
                          ])

    def test_neg(self):
        reversed = -minor_melodic
        expected = ScalePattern(["Minor melodic"],
                                [
                                    Interval(diatonic=-1, chromatic=- 1),
                                    Interval(diatonic=-1, chromatic=-2),
                                    Interval(diatonic=-1, chromatic=-2),
                                    Interval(diatonic=-1, chromatic=-2),
                                    Interval(diatonic=-1, chromatic=-2),
                                    Interval(diatonic=-1, chromatic=-1),
                                    Interval(diatonic=-1, chromatic=-2)], 3, 0, increasing=False,
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
        ])
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
        ])
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), nb_octave=2)
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
        ])
        generated = minor_melodic.generate(Note(chromatic=0, diatonic=0), nb_octave=-2)
        self.assertEquals(expected, generated)
