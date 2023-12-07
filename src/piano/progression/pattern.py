from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import List, Optional

from lily.lily import compile_
from lily.svg import display_svg_file
from solfege.interval.set_of_intervals import SetOfIntervals
from solfege.note import Note
from utils.constants import test_folder


@dataclass(frozen=True)
class NamedIntervalsPattern:
    role: str
    order: Optional[str]
    left_hand: SetOfIntervals
    right_hand: SetOfIntervals

    def __add__(self, other: Note):
        from piano.progression.chord_progression import NamedChord
        return NamedChord(self.role, self.left_hand + other, self.right_hand + other)


@dataclass(frozen=True)
class ChordProgressionPattern:
    name: str
    chords: List[NamedIntervalsPattern]

    def __add__(self, other: Note):
        from piano.progression.chord_progression import ChordProgression
        return ChordProgression(self.name, other, [chord + other for chord in self.chords])




class ProgressionPatternTest(unittest.TestCase):
    maxDiff = None

    def test_add_chord(self):
        from piano.progression.chord_progression import ProgressionTest
        s = self.ii_min_7 + Note(chromatic=0, diatonic=0)
        self.assertEquals(s, ProgressionTest.d_min_7)

    def test_add_progression(self):
        from piano.progression.chord_progression import ProgressionTest
        s = self.ii_v_i + Note("C")
        print(s)
        print(ProgressionTest.three_five_c)
        self.assertEquals(s, ProgressionTest.three_five_c)

    def test_see_all(self):
        for pattern in patterns:
            lily = pattern.lily()
            path = f"{test_folder}/{pattern.name}"
            compile_(lily, path, wav=True)
            display_svg_file(f"{path}.svg")
