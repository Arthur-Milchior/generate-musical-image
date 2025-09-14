# from __future__ import annotations
#
# # from dataclasses import dataclass
# from typing import List
#
# from lily.lily import compile_
# from lily.svg import display_svg_file
# from solfege.value.interval.set_of_intervals import SetOfIntervals
# from solfege.value.note.note import Note
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
#         from instruments.piano.progression.chord_progression import TwoHandsChord
#         return TwoHandsChord(self.role, self.left_hand + other, self.right_hand + other)
#
#
# @dataclass(frozen=True)
# class ChordProgressionPattern:
#     name: str
#     chords: List[NamedIntervalsPattern]
#
#     def __add__(self, other: Note):
#         from instruments.piano.progression.chord_progression import ChordProgression
#         return ChordProgression(self.name, "TODO", other, [chord + other for chord in self.chords])
#
#
#
#
