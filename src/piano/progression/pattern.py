# from __future__ import annotations
#
# import unittest
# from dataclasses import dataclass
# from typing import List
#
# from lily.lily import compile_
# from lily.svg import display_svg_file
# from solfege.interval.set_of_intervals import SetOfIntervals
# from solfege.note import Note
# from utils.constants import test_folder
#
#
# @dataclass(frozen=True)
# class NamedIntervalsPattern:
#     role: str
#     left_hand: SetOfIntervals
#     right_hand: SetOfIntervals
#
#     def __add__(self, other: Note):
#         from piano.progression.chord_progression import TwoHandsChord
#         return TwoHandsChord(self.role, self.left_hand + other, self.right_hand + other)
#
#
# @dataclass(frozen=True)
# class ChordProgressionPattern:
#     name: str
#     chords: List[NamedIntervalsPattern]
#
#     def __add__(self, other: Note):
#         from piano.progression.chord_progression import ChordProgression
#         return ChordProgression(self.name, "TODO", other, [chord + other for chord in self.chords])
#
#
#
#
# class ProgressionPatternTest(unittest.TestCase):
#     maxDiff = None
#
#     def test_add_chord(self):
#         from piano.progression.chord_progression import ProgressionTest
#         s = (ProgressionTest.d_min_7-Note("C4")) + Note("C4")
#         self.assertEquals(s, ProgressionTest.d_min_7)
#
#     def test_add_progression(self):
#         from piano.progression.chord_progression import ProgressionTest
#         s = (ProgressionTest.three_five_c - Note("C4")) + Note("C")
#         self.assertEquals(s, ProgressionTest.three_five_c)
#
#     def test_see_all(self):
#         from piano.progression.progressions_in_C import patterns_in_C
#         for pattern in patterns_in_C:
#             lily = pattern.lily()
#             path = f"{test_folder}/{pattern.progression_name}"
#             compile_(lily, path, wav=True)
#             display_svg_file(f"{path}.svg")
