from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Generic, Self, Union, Tuple, Optional

from solfege.chord.chord_pattern import chord_patterns
from solfege.key import nor_flat_nor_sharp, three_flats, one_sharp, seven_sharps, one_flat, two_flats, five_flats, \
    four_flats, three_sharps
from solfege.scale.scale import Scale
from solfege.interval.abstract_interval import IntervalType
from solfege.note.note import Note
from solfege.note.abstract_note import NoteType
from solfege.interval.interval_pattern import intervals_up_to_octave

"""Contains a class to represent a scale.

Also contains all scales from wikipedia, which can be done using the 12 note from chromatic scales."""

import sys

from solfege.interval.interval import Interval, octave
from solfege.solfege_pattern import SolfegePattern


@dataclass(frozen=True)
class ScalePattern(SolfegePattern):
    """Whether it's in increasing order."""
    increasing: bool
    """The descending pattern if different from the ascending one. Mostly used for minor melodic. It's stored in an ascending way.
    If it's none, the descending is self"""
    descending: Optional[Self] = None
    """If True, add a warning if the result is not a perfect octave"""
    suppress_warning: bool = field(compare = False, default=False)

    def __post_init__(self):
        super().__post_init__()
        if not self.suppress_warning:
            last_interval = self._absolute_intervals[-1]
            if last_interval != octave:
                print(f"Warning: scale {self.names[0]} has a last interval of {last_interval}", file=sys.stderr)

    def __neg__(self):
        """The same pattern, reversed. Ignore the descending option"""
        return ScalePattern(names=self.names, notation=self.notation, relative_intervals=[-interval for interval in reversed(self.relative_intervals)],
                            interval_for_signature=self.interval_for_signature, suppress_warning=True, increasing = not self.increasing, descending=self.descending,
                            record=False)

    def generate(self, tonic: NoteType, number_of_octaves=1,
                 add_an_extra_note: bool = False) -> Scale[NoteType]:
        """The note, starting at tonic, following this pattern for nb_octave.
        If nb_octave is negative, the generated scale is decreasing."""
        assert number_of_octaves != 0
        if number_of_octaves < 0:
            return (-self).generate(tonic, -number_of_octaves, add_an_extra_note=add_an_extra_note)
        current_note = tonic
        notes = [tonic]
        for _ in range(number_of_octaves):
            for interval in self.relative_intervals:
                current_note += interval
                notes.append(current_note)
        if add_an_extra_note:
            notes.append(notes[-1] + self.relative_intervals[0])
        return Scale[NoteType](notes=notes, pattern=self, key = notes[0] + self.interval_for_signature)

    def __len__(self):
        return len(self.relative_intervals)

# ré b, mi bb, f, g, a b, b bb, c

major_scale = ScalePattern(["Major"], [2, 2, 1, 2, 2, 2, 1], nor_flat_nor_sharp)
blues = ScalePattern(["Blues"], [(3, 2), 2, (1, 0), 1, (3, 2), 2], three_flats)
minor_harmonic = ScalePattern(["Minor harmonic"], [2, 1, 2, 2, 1, 3, 1], three_flats)
pentatonic_minor = ScalePattern(["Pentatonic minor"], [(3, 2), 2, 2, (3, 2), 2],
                                          three_flats)
pentatonic_major = ScalePattern(["Pentatonic major"], [2, 2, (3, 2), 2, (3, 2)], nor_flat_nor_sharp)
whole_tone = ScalePattern(["Whole tone"], [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 2)], one_sharp)
chromatic_scale_pattern = ScalePattern(["Chromatic"],
                                                 [(1, 0), (1, 1), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0),
                                                  (1, 1), (1, 0), (1, 1),
                                                  (1, 1), ], nor_flat_nor_sharp)
minor_natural = ScalePattern(["Minor natural", "Aeolian mode"], [2, 1, 2, 2, 1, 2, 2], three_flats)
minor_melodic = ScalePattern(["Minor melodic"], [2, 1, 2, 2, 2, 2, 1], three_flats, descending=minor_natural)

scale_patterns_I_practice: List[ScalePattern] = [major_scale, blues, minor_natural, minor_harmonic, minor_melodic, chromatic_scale_pattern,
                             whole_tone, pentatonic_major, pentatonic_minor] + [chord_pattern.to_arpeggio_pattern() for
                                                                                chord_pattern in chord_patterns]

scale_patterns = scale_patterns_I_practice + [
    ScalePattern(["Greek Dorian tonos (chromatic genus)"], [1, 1, 3, 2, 1, 1, 3],
                           nor_flat_nor_sharp),
    ScalePattern(["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"], [2, 2, 2, 1, 2, 1, 2], one_sharp),
    ScalePattern(
        ["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],
        [1, 2, 1, 2, 2, 2, 2], seven_sharps),
    ScalePattern(["Augmented", ], [(3, 2), (1, 0), (3, 2), (1, 0), (3, 2), 1], nor_flat_nor_sharp),
    ScalePattern(["Prometheus", "Mystic chord"], [2, 2, 2, (3, 2), 1, 2],
                           nor_flat_nor_sharp),  # one flat one sharp, can't decide
    ScalePattern(["Tritone", ], [1, 3, (2, 2), (1, 0), (3, 2), 2], one_flat),
    ScalePattern(["Bebop dominant", ], [2, 2, 1, 2, 2, 1, (1, 0), 1], nor_flat_nor_sharp),
    ScalePattern(["Bebop dorian", "Bebop minor"], [2, 1, (1, 0), 1, 2, 2, 1, 2, ], nor_flat_nor_sharp),
    ScalePattern(["Alternate bebop dorian"], [2, 1, 2, 2, 2, 1, (1, 0), 1, ], two_flats),
    ScalePattern(["Bebop major", ], [2, 2, 1, 2, (1, 0), 1, 2, 1], nor_flat_nor_sharp),
    ScalePattern(["Bebop melodic minor", ], [2, 1, 2, 2, (1, 0), 1, 2, 1], nor_flat_nor_sharp),
    ScalePattern(["Bebop harmonic minor", "Bebop natural minor"], [2, 1, 2, 2, 1, 2, (1, 0), 1],
                           three_flats),
    ScalePattern(["Double harmonic major", "Byzantine", "Arabic", "Gypsi major"], [1, 3, 1, 2, 1, 3, 1],
                           nor_flat_nor_sharp),
    ScalePattern(["Enigmatic"], [1, 3, 2, 2, 2, 1, 1], nor_flat_nor_sharp),
    ScalePattern(["Descending Enigmatic"], [1, 3, 1, 3, 2, 1, 1], nor_flat_nor_sharp),
    # ScalePattern(["Flamenco mode"], [1, 3, 1, 2, 1, 3, 1], unison) can't find anymore on wp
    ScalePattern(["Hungarian", "Hungarian Gypsy"], [2, 1, 3, 1, 1, 2, 2], three_flats),
    ScalePattern(["Half diminished"], [2, 1, 2, 1, 2, 2, 2], five_flats),
    ScalePattern(["Harmonic major"], [2, 2, 1, 2, 1, 3, 1], nor_flat_nor_sharp),
    ScalePattern(["Hirajōshi Burrows"], [(4, 2), 2, 1, (4, 2), 1], one_sharp),
    ScalePattern(["Hirajōshi Sachs-Slonimsky"], [1, (4, 2), 1, (4, 2), 2], nor_flat_nor_sharp),
    ScalePattern(["Hirajōshi Kostka and Payne-Speed"], [2, 1, (4, 2), 1, (4, 2)],
                           nor_flat_nor_sharp),
    ScalePattern(["Hungarian minor"], [2, 1, 3, 1, 1, 3, 1], three_flats),  # should also have one sharp
    ScalePattern(["Greek Dorian tonos (diatonic genus)", "Phrygian mode"], [1, 2, 2, 2, 1, 2, 2],
                           three_flats),
    ScalePattern(["Miyako-bushi"], [1, (4, 2), 2, 1, (4, 2)], two_flats),
    ScalePattern(["Insen"], [1, (4, 2), 2, (3, 2), 2], four_flats),
    ScalePattern(["Iwato"], [1, (4, 2), 1, (4, 2), 2], five_flats),
    ScalePattern(["Lydian augmented"], [2, 2, 2, 2, 1, 2, 1], three_sharps),
    ScalePattern(["Major Locrian"], [2, 2, 1, 1, 2, 2, 2], five_flats),
    ScalePattern(["Minyo"], [(3, 2), 2, (3, 2), 2, 2], nor_flat_nor_sharp),
    ScalePattern(["Neapolitan minor"], [1, 2, 2, 2, 1, 3, 1], four_flats),
    ScalePattern(["Neapolitan major"], [1, 2, 2, 2, 2, 2, 1], nor_flat_nor_sharp),
    ScalePattern(["Pelog"], [1, 2, 3, 1, 1, 2, 2, ], four_flats),
    ScalePattern(["Pelog bem"], [1, (5, 2), 1, 1, (4, 2)], four_flats),
    ScalePattern(["Pelog barang"], [2, (4, 2), 1, 2, (3, 2)], four_flats),
    ScalePattern(["Persian"], [1, 3, 1, 1, 2, 3, 1], five_flats),
    ScalePattern(["Phrygian dominant"], [1, 3, 1, 2, 1, 2, 2], four_flats),
    ScalePattern(["Greek Phrygian tonos (diatonic genus)"], [2, 1, 2, 2, 2, 1, 2],
                           nor_flat_nor_sharp),
    ScalePattern(["Greek Phrygian tonos (chromatic genus)"], [3, 1, 1, 2, 3, 1, 1],
                           nor_flat_nor_sharp),
    ScalePattern(["Slendro"], [2, (3, 2), 2, 2, (3, 2)], nor_flat_nor_sharp),
    ScalePattern(["Two-semitone tritone"], [1, (1, 0), (4, 2), 1, 1, (4, 2)], nor_flat_nor_sharp),
    ScalePattern(["Ukrainian Dorian"], [2, 1, 3, 1, 2, 1, 2], two_flats),  # shold also have one sharp
    ScalePattern(["Misheberak"], [2, 1, 3, 1, 2, 1, 2], nor_flat_nor_sharp),
    ScalePattern(["Yo ascending"], [2, (3, 2), 2, (3, 2), 2], two_flats),
    ScalePattern(["Yo descending"], [2, (3, 2), 2, 2, (3, 2)], two_flats),
    ScalePattern(["Yo with auxiliary"], [2, 1, 2, 2, 2, 1, 2], two_flats),
    ScalePattern(["Dorian"], [2, 1, 2, 2, 2, 1, 2], two_flats),
    ScalePattern(["Locrian"], [1, 2, 2, 1, 2, 2, 2], five_flats),
    ScalePattern(["Lydian"], [2, 2, 2, 1, 2, 2, 1], one_sharp),
    ScalePattern(["Greek Lydian tonos (diatonic genus)"], [2, 2, 1, 2, 2, 2, 1],
                           nor_flat_nor_sharp),
    ScalePattern(["Greek Lydian tonos (chromatic genus)"], [1, 3, 1, 1, 3, 2, 1],
                           nor_flat_nor_sharp),
    ScalePattern(["Mixolydian", "Adonal malakh mode"], [2, 2, 1, 2, 2, 1, 2], one_flat),
    ScalePattern(["Greek Mixolydian tonos (diatonic genus)"], [1, 2, 2, 1, 2, 2, 2],
                           nor_flat_nor_sharp),
    ScalePattern(["Greek Mixolydian tonos (chromatic genus)"], [2, 1, 3, 1, 1, 3, 1],
                           nor_flat_nor_sharp),
    ScalePattern(["Octave"], [(12, 7)], nor_flat_nor_sharp)
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
