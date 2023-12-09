from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import List

from lily.Lilyable.list_piano_lilyable import ListPianoLilyable
from lily.Lilyable.piano_lilyable import PianoLilyable
from lily.lily import compile_
# from piano.progression.pattern import NamedIntervalsPattern, ChordProgressionPattern
from solfege.interval.interval import Interval
from solfege.note import Note
from solfege.note.set_of_notes import SetOfNotes
from utils.constants import test_folder
from utils.util import indent


@dataclass(frozen=True)
class TwoHandsChord(PianoLilyable):
    name: str
    left_hand: SetOfNotes
    right_hand: SetOfNotes
    tonic: Note = Note("C4")

    def left_lily(self):
        return self.left_hand.lily_in_scale()

    def right_lily(self):
        return self.right_hand.lily_in_scale()

    def annotations_lily(self):
        return self.name

    def first_key(self) -> str:
        """The lily code for the annotation"""
        return self.tonic.lily_in_scale()

    def __add__(self, other: Interval):
        return TwoHandsChord(self.name, self.left_hand + other, self.right_hand + other, self.tonic + other)

    def __sub__(self, other: Interval
                # Union[Note, Interval]
                ):
        # if isinstance(other, Note):
        #     return NamedIntervalsPattern(role=self.name, left_hand=self.left_hand - other,
        #                                  right_hand=self.right_hand - other)
        return TwoHandsChord(self.name, left_hand=self.left_hand - other, right_hand=self.right_hand - other,
                             tonic=self.tonic - other)


class ChordProgression(ListPianoLilyable):
    progression_name: str
    disambiguation: str
    key: Note
    chords: List[TwoHandsChord]

    def __init__(self, progression_name: str, disambiguation: str, key: Note, chords: List[TwoHandsChord]):
        super().__init__(chords)
        self.progression_name = progression_name
        self.key = key
        self.disambiguation = disambiguation
        self.chords = chords

    def __add__(self, other: Interval):
        return ChordProgression(self.progression_name, self.disambiguation, self.key + other,
                                [chord + other for chord in self.chords])

    def __radd__(self, other: Interval):
        return self + other

    def first_chord(self):
        first_chord = self.chords[0]
        return ChordProgression(first_chord.name, disambiguation=self.disambiguation, key=self.key,
                                chords=[first_chord])

    def __sub__(self, other: Interval  # Optional[Note, Interval]
                ):
        # if isinstance(other, Note):
        #     return ChordProgressionPattern(name=self.progression_name, chords=[chord - other for chord in self.chords])
        return ChordProgression(progression_name=self.progression_name, disambiguation=self.progression_name,
                                key=self.key - other, chords=[chord - other for chord in self.chords])


class ProgressionTest(unittest.TestCase):
    maxDiff = None
    d_min_7 = TwoHandsChord("ii",
                            left_hand=SetOfNotes([
                                Note("D3"),
                            ]),
                            right_hand=SetOfNotes([
                                Note("F4"),
                                Note("C5"),
                            ]),
                            tonic=Note("C")
                            )
    e_min_7 = TwoHandsChord("ii",
                            left_hand=SetOfNotes([
                                Note("E3"),
                            ]),
                            right_hand=SetOfNotes([
                                Note("G4"),
                                Note("D5"),
                            ]),
                            tonic=Note("D")
                            )
    three_five_c = ChordProgression(
        progression_name="ii V I", disambiguation="ii V I",
        key=Note("C"),
        chords=[
            d_min_7,
            TwoHandsChord("V",
                          left_hand=SetOfNotes([
                              Note("G3"),
                          ]),
                          right_hand=SetOfNotes([
                              Note("F4"),
                              Note("B4"),
                          ]),
                          tonic=Note("C")
                          ),
            TwoHandsChord("I",
                          left_hand=SetOfNotes([
                              Note("C3"),
                          ]),
                          right_hand=SetOfNotes([
                              Note("E4"),
                              Note("B4"),
                          ]),
                          tonic=Note("C")
                          ),
        ]
    )
    three_five_d = ChordProgression(
        progression_name="ii V I", disambiguation="ii V I",
        key=Note("D"),
        chords=[
            e_min_7,
            TwoHandsChord("V",
                          left_hand=SetOfNotes([
                              Note("A3"),
                          ]),
                          right_hand=SetOfNotes([
                              Note("G4"),
                              Note("C#5"),
                          ]),
                          tonic=Note("D")
                          ),
            TwoHandsChord("I",
                          left_hand=SetOfNotes([
                              Note("D3"),
                          ]),
                          right_hand=SetOfNotes([
                              Note("F#4"),
                              Note("C#5"),
                          ]),
                          tonic=Note("D")
                          ),
        ]
    )

    mini = """\
\\version "2.20.0"
<<
\\new Lyrics {\\lyricmode{ii}}
\\new Staff {c''}
>>
"""

    three_five_c_lily = """\
\\version "2.20.0"
\\score{
  <<
    \\new Lyrics {
      \\lyricmode{
        ii V I
      }
    }
    \\new PianoStaff<<
      \\new Staff{
        \\clef treble
        \\key c' \\major
        <f' c''> <f' b'> <e' b'>
      }
      \\new Staff{
        \\clef bass
        \\key c' \\major
        <d> <g> <c>
      }
    >>
  >>
}"""

    right_lily = """<f' c''> <f' b'> <e' b'>"""

    def test_right(self):
        self.assertEquals(self.right_lily, self.three_five_c.right_lily())

    def test_lyrics(self):
        self.assertEquals("ii V I", self.three_five_c.annotations_lily())

    def test_lily(self):
        self.assertEquals(
            self.three_five_c.lily(),
            self.three_five_c_lily
        )

    def test_file(self):
        prefix = f"{test_folder}/test"
        compile_(self.three_five_c_lily, prefix, wav=False, force_recompile=True)()

    def test_mini(self):
        prefix = f"{test_folder}/test"
        compile_(self.mini, prefix, wav=False, force_recompile=True)()

    def test_add(self):
        s = self.d_min_7 + Interval(chromatic=2, diatonic=1)
        self.assertEquals(s, self.e_min_7)
        s = self.three_five_c + Interval(chromatic=2, diatonic=1)
        print(s)
        print(self.three_five_d)
        self.assertEquals(s, self.three_five_d)
