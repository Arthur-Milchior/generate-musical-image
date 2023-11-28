import unittest

from dataclasses import dataclass
from typing import List

from solfege.scale.scale_pattern import major_scale, ScalePattern
from solfege.scale.scale import Scale
from solfege.note import Note
from solfege.note.set_of_notes import SetOfNotes


@dataclass
class ChordPattern:
    name: str
    intervals: List[int]


triad = ChordPattern("triad", [2, 2])
seventh = ChordPattern("seventh", [2, 2, 2])

chord_patterns = [triad, seventh]


def chord_from_scale_pattern_and_position(scale: Scale, chord_pattern: ChordPattern, position: int) -> SetOfNotes:
    chord = []
    for interval in [0] + chord_pattern.intervals:
        position = position + interval
        chord.append(scale.notes[position])
    return SetOfNotes(chord, fundamental=chord[0])


def chord_succession_for_scale(scale: Scale,
                               chord_pattern: ChordPattern,
                               nb_of_chords: int) -> List[SetOfNotes]:
    return [chord_from_scale_pattern_and_position(scale, chord_pattern, position) for position in
            range(nb_of_chords)]


def chord_succession_for_scale_pattern(key: Note,
                                       scale_pattern: ScalePattern,
                                       chord_pattern: ChordPattern,
                                       nb_octave: int = 1) -> List[SetOfNotes]:
    scale = scale_pattern.generate(fundamental=key, number_of_octaves=nb_octave + 1, add_an_extra_note=False)
    return chord_succession_for_scale(scale, chord_pattern, scale_pattern.number_of_intervals() * nb_octave + 1)


class TestChordSuccession(unittest.TestCase):
    triads_on_c_major = [
        SetOfNotes([Note.from_name("C"),
                    Note.from_name("E"),
                    Note.from_name("G")],
                   Note.from_name("C")),
        SetOfNotes([Note.from_name("D"),
                    Note.from_name("F"),
                    Note.from_name("A")],
                   Note.from_name("D")),
        SetOfNotes([Note.from_name("E"),
                    Note.from_name("G"),
                    Note.from_name("B")],
                   Note.from_name("E")),
        SetOfNotes([Note.from_name("F"),
                    Note.from_name("A"),
                    Note.from_name("C5")],
                   Note.from_name("F")),
        SetOfNotes([Note.from_name("G"),
                    Note.from_name("B"),
                    Note.from_name("D5")],
                   Note.from_name("G")),
        SetOfNotes([Note.from_name("A"),
                    Note.from_name("C5"),
                    Note.from_name("E5")],
                   Note.from_name("A")),
        SetOfNotes([Note.from_name("B"),
                    Note.from_name("D5"),
                    Note.from_name("F5")],
                   Note.from_name("B")),
        SetOfNotes([Note.from_name("C5"),
                    Note.from_name("E5"),
                    Note.from_name("G5")],
                   Note.from_name("C5")),
    ]

    two_octave_major_c4_scale = Scale([
        Note.from_name("C"),
        Note.from_name("D"),
        Note.from_name("E"),
        Note.from_name("F"),
        Note.from_name("G"),
        Note.from_name("A"),
        Note.from_name("B"),
        Note.from_name("C5"),
        Note.from_name("D5"),
        Note.from_name("E5"),
        Note.from_name("F5"),
        Note.from_name("G5"),
        Note.from_name("A5"),
        Note.from_name("B5"),
        Note.from_name("C6"),
    ], major_scale)

    def test_chord_from_scale_pattern_and_position(self):
        expected = SetOfNotes([Note.from_name("C"),
                               Note.from_name("E"),
                               Note.from_name("G")],
                              Note.from_name("C"))
        generated = chord_from_scale_pattern_and_position(self.two_octave_major_c4_scale, chord_pattern=triad, position=0)
        self.assertEquals(generated,
                          expected)

    def test_chord_succession_for_scale(self):
        generated = chord_succession_for_scale(self.two_octave_major_c4_scale,
                                               chord_pattern=triad,
                                               nb_of_chords=8
                                               )
        self.assertEquals(self.triads_on_c_major, generated)

    def test_chord_from_scale_pattern(self):
        generated = chord_succession_for_scale_pattern(key=Note.from_name("C"),
                                                       scale_pattern=major_scale,
                                                       chord_pattern=triad,
                                                       nb_octave=1,
                                                       )
        self.assertEquals(self.triads_on_c_major, generated)
