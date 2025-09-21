
from typing import List
from solfege.pattern.chord.chord_patterns import chord_patterns
from solfege.value.interval.role.interval_role_from_string import role_from_interval_index
from solfege.value.key.keys import *
from solfege.pattern.scale.scale_pattern import ScalePattern



pentatonic_major = ScalePattern.make_relative(names=["Pentatonic major"], relative_intervals=[2, 2, (3, 2), 2, (3, 2)], interval_for_signature=nor_flat_nor_sharp)
major_scale = ScalePattern.make_relative(names=["Major"], relative_intervals=[2, 2, 1, 2, 2, 2, 1], interval_for_signature=nor_flat_nor_sharp)
pentatonic_minor = ScalePattern.make_relative(names=["Pentatonic minor"], relative_intervals=[(3, 2), 2, 2, (3, 2), 2],
                                          interval_for_signature=three_flats)
minor_natural = ScalePattern.make_relative(names=["Minor natural", "Aeolian mode"], relative_intervals=[2, 1, 2, 2, 1, 2, 2], interval_for_signature=three_flats)
blues = ScalePattern.make_relative(names=["Blues"], relative_intervals=[(3, 2), 2, (1, 0, "b"), 1, (3, 2), 2], interval_for_signature=three_flats)
minor_harmonic = ScalePattern.make_relative(names=["Minor harmonic"], relative_intervals=[2, 1, 2, 2, 1, 3, 1], interval_for_signature=three_flats)
chromatic_scale_pattern = ScalePattern.make_relative(names=["Chromatic"], relative_intervals=
                                                 [(1, 0), (1, 1), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0),
                                                  (1, 1), (1, 0), (1, 1),
                                                  (1, 1), ], interval_for_signature=nor_flat_nor_sharp, role_maker=role_from_interval_index)
minor_melodic = ScalePattern.make_relative(names=["Minor melodic"], relative_intervals=[2, 1, 2, 2, 2, 2, 1], interval_for_signature=three_flats, _descending=minor_natural)

chord_patterns_as_scales = [chord_pattern.to_arpeggio_pattern() for chord_pattern in chord_patterns]
scale_patterns_I_practice: List[ScalePattern] = [pentatonic_major, major_scale, pentatonic_minor, minor_natural, blues, minor_harmonic, chromatic_scale_pattern,  minor_melodic] + chord_patterns_as_scales

whole_tone = ScalePattern.make_relative(names=["Whole tone"], relative_intervals=[(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 2)], interval_for_signature=one_sharp, role_maker=role_from_interval_index)
scale_patterns = scale_patterns_I_practice + [whole_tone,
    ScalePattern.make_relative(names=["Greek Dorian tonos (chromatic genus)"], relative_intervals=[1, 1, 3, 2, 1, 1, 3],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"], relative_intervals=[2, 2, 2, 1, 2, 1, 2], interval_for_signature=one_sharp),
    ScalePattern.make_relative(
        names=["Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],
        relative_intervals=[1, 2, 1, 2, 2, 2, 2], interval_for_signature=seven_sharps),
    ScalePattern.make_relative(names=["Augmented", ], relative_intervals=[(3, 2), (1, 0), (3, 2), (1, 0), (3, 2), 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Prometheus", "Mystic chord"], relative_intervals=[2, 2, 2, (3, 2), 1, 2],
                           interval_for_signature=nor_flat_nor_sharp),  # one flat one sharp, can't decide
    ScalePattern.make_relative(names=["Tritone", ], relative_intervals=[1, 3, (2, 2), (1, 0), (3, 2), 2], interval_for_signature=one_flat),
    ScalePattern.make_relative(names=["Bebop dominant", ], relative_intervals=[2, 2, 1, 2, 2, 1, (1, 0), 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Bebop dorian", "Bebop minor"], relative_intervals=[2, 1, (1, 0), 1, 2, 2, 1, 2, ], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Alternate bebop dorian"], relative_intervals=[2, 1, 2, 2, 2, 1, (1, 0), 1, ], interval_for_signature=two_flats),
    ScalePattern.make_relative(names=["Bebop major", ], relative_intervals=[2, 2, 1, 2, (1, 0), 1, 2, 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Bebop melodic minor", ], relative_intervals=[2, 1, 2, 2, (1, 0), 1, 2, 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Bebop harmonic minor", "Bebop natural minor"], relative_intervals=[2, 1, 2, 2, 1, 2, (1, 0), 1],
                           interval_for_signature=three_flats),
    ScalePattern.make_relative(names=["Double harmonic major", "Byzantine", "Arabic", "Gypsi major"], relative_intervals=[1, 3, 1, 2, 1, 3, 1],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Enigmatic"], relative_intervals=[1, 3, 2, 2, 2, 1, 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Descending Enigmatic"], relative_intervals=[1, 3, 1, 3, 2, 1, 1], interval_for_signature=nor_flat_nor_sharp),
    # ScalePattern.make_relative(names=["Flamenco mode"], relative_intervals=[1, 3, 1, 2, 1, 3, 1], unison) can't find anymore on wp
    ScalePattern.make_relative(names=["Hungarian", "Hungarian Gypsy"], relative_intervals=[2, 1, 3, 1, 1, 2, 2], interval_for_signature=three_flats),
    ScalePattern.make_relative(names=["Half diminished"], relative_intervals=[2, 1, 2, 1, 2, 2, 2], interval_for_signature=five_flats),
    ScalePattern.make_relative(names=["Harmonic major"], relative_intervals=[2, 2, 1, 2, 1, 3, 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Hirajōshi Burrows"], relative_intervals=[(4, 2), 2, 1, (4, 2), 1], interval_for_signature=one_sharp),
    ScalePattern.make_relative(names=["Hirajōshi Sachs-Slonimsky"], relative_intervals=[1, (4, 2), 1, (4, 2), 2], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Hirajōshi Kostka and Payne-Speed"], relative_intervals=[2, 1, (4, 2), 1, (4, 2)],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Hungarian minor"], relative_intervals=[2, 1, 3, 1, 1, 3, 1], interval_for_signature=three_flats),  # should also have one sharp
    ScalePattern.make_relative(names=["Greek Dorian tonos (diatonic genus)", "Phrygian mode"], relative_intervals=[1, 2, 2, 2, 1, 2, 2],
                           interval_for_signature=three_flats),
    ScalePattern.make_relative(names=["Miyako-bushi"], relative_intervals=[1, (4, 2), 2, 1, (4, 2)], interval_for_signature=two_flats),
    ScalePattern.make_relative(names=["Insen"], relative_intervals=[1, (4, 2), 2, (3, 2), 2], interval_for_signature=four_flats),
    ScalePattern.make_relative(names=["Iwato"], relative_intervals=[1, (4, 2), 1, (4, 2), 2], interval_for_signature=five_flats),
    ScalePattern.make_relative(names=["Lydian augmented"], relative_intervals=[2, 2, 2, 2, 1, 2, 1], interval_for_signature=three_sharps),
    ScalePattern.make_relative(names=["Major Locrian"], relative_intervals=[2, 2, 1, 1, 2, 2, 2], interval_for_signature=five_flats),
    ScalePattern.make_relative(names=["Minyo"], relative_intervals=[(3, 2), 2, (3, 2), 2, 2], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Neapolitan minor"], relative_intervals=[1, 2, 2, 2, 1, 3, 1], interval_for_signature=four_flats),
    ScalePattern.make_relative(names=["Neapolitan major"], relative_intervals=[1, 2, 2, 2, 2, 2, 1], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Pelog"], relative_intervals=[1, 2, 3, 1, 1, 2, 2, ], interval_for_signature=four_flats),
    ScalePattern.make_relative(names=["Pelog bem"], relative_intervals=[1, (5, 2), 1, 1, (4, 2)], interval_for_signature=four_flats),
    ScalePattern.make_relative(names=["Pelog barang"], relative_intervals=[2, (4, 2), 1, 2, (3, 2)], interval_for_signature=four_flats),
    ScalePattern.make_relative(names=["Persian"], relative_intervals=[1, 3, 1, 1, 2, 3, 1], interval_for_signature=five_flats),
    ScalePattern.make_relative(names=["Phrygian dominant"], relative_intervals=[1, 3, 1, 2, 1, 2, 2], interval_for_signature=four_flats),
    ScalePattern.make_relative(names=["Greek Phrygian tonos (diatonic genus)"], relative_intervals=[2, 1, 2, 2, 2, 1, 2],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Greek Phrygian tonos (chromatic genus)"], relative_intervals=[3, 1, 1, 2, 3, 1, 1],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Slendro"], relative_intervals=[2, (3, 2), 2, 2, (3, 2)], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Two-semitone tritone"], relative_intervals=[1, (1, 0), (4, 2), 1, 1, (4, 2)], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Ukrainian Dorian"], relative_intervals=[2, 1, 3, 1, 2, 1, 2], interval_for_signature=two_flats),  # shold also have one sharp
    ScalePattern.make_relative(names=["Misheberak"], relative_intervals=[2, 1, 3, 1, 2, 1, 2], interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Yo ascending"], relative_intervals=[2, (3, 2), 2, (3, 2), 2], interval_for_signature=two_flats),
    ScalePattern.make_relative(names=["Yo descending"], relative_intervals=[2, (3, 2), 2, 2, (3, 2)], interval_for_signature=two_flats),
    ScalePattern.make_relative(names=["Yo with auxiliary"], relative_intervals=[2, 1, 2, 2, 2, 1, 2], interval_for_signature=two_flats),
    ScalePattern.make_relative(names=["Dorian"], relative_intervals=[2, 1, 2, 2, 2, 1, 2], interval_for_signature=two_flats),
    ScalePattern.make_relative(names=["Locrian"], relative_intervals=[1, 2, 2, 1, 2, 2, 2], interval_for_signature=five_flats),
    ScalePattern.make_relative(names=["Lydian"], relative_intervals=[2, 2, 2, 1, 2, 2, 1], interval_for_signature=one_sharp),
    ScalePattern.make_relative(names=["Greek Lydian tonos (diatonic genus)"], relative_intervals=[2, 2, 1, 2, 2, 2, 1],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Greek Lydian tonos (chromatic genus)"], relative_intervals=[1, 3, 1, 1, 3, 2, 1],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Mixolydian", "Adonal malakh mode"], relative_intervals=[2, 2, 1, 2, 2, 1, 2], interval_for_signature=one_flat),
    ScalePattern.make_relative(names=["Greek Mixolydian tonos (diatonic genus)"], relative_intervals=[1, 2, 2, 1, 2, 2, 2],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Greek Mixolydian tonos (chromatic genus)"], relative_intervals=[2, 1, 3, 1, 1, 3, 1],
                           interval_for_signature=nor_flat_nor_sharp),
    ScalePattern.make_relative(names=["Octave"], relative_intervals=[(12, 7)], interval_for_signature=nor_flat_nor_sharp)
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
