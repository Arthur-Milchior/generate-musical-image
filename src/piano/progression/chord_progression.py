from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import List, Optional, Union

from lily.lily import compile_
from piano.progression.pattern import NamedIntervalsPattern, ChordProgressionPattern
from solfege.interval.interval import Interval
from solfege.note import Note
from solfege.note.set_of_notes import SetOfNotes
from utils.constants import test_folder
from utils.util import indent


@dataclass(frozen=True)
class NamedChord:
    name: str
    left_hand: SetOfNotes
    right_hand: SetOfNotes

    def left_lily(self):
        return self.left_hand.lily()

    def right_lily(self):
        return self.right_hand.lily()

    def __add__(self, other: Interval):
        return NamedChord(self.name, self.left_hand + other, self.right_hand + other)

    def __sub__(self, other: Union[Note, Interval]):
        if isinstance(other, Note):
            return NamedIntervalsPattern(role=self.name, order=None, left_hand=self.left_hand - other,
                                         right_hand=self.right_hand - other)
        return NamedChord(self.name, left_hand=self.left_hand - other, right_hand=self.right_hand - other)


@dataclass(frozen=True)
class ChordProgression:
    name: str
    key: Note
    chords: List[NamedChord]
    pattern: Optional[ChordProgressionPattern] = None

    def left_lily(self):
        inside = "\n".join(
            ["\\clef bass", f"\\key {self.key.lily()} \\major"] + [
                chord.left_lily() for chord in self.chords
            ])
        return f"""\\new Staff {{
{indent(inside)}
}}"""

    def right_lily(self):
        inside = "\n".join(
            ["\\clef treble", f"\\key {self.key.lily()} \\major"] + [
                chord.right_lily() for chord in self.chords
            ])
        return f"""\\new Staff {{
{indent(inside)}
}}"""

    def chord_names_lily(self):
        return f"""\\new Lyrics {{
  \\lyricmode{{{" ".join(chord.name for chord in self.chords)}}}
}}"""

    def lily(self):
        return f"""\
\\version "2.20.0"
\\score {{
  <<
{indent(self.chord_names_lily(), 4)}
    \\new PianoStaff<<
{indent(self.right_lily(), 6)}
{indent(self.left_lily(), 6)}
    >>
  >>
}}"""

    def __add__(self, other: Interval):
        return ChordProgression(self.name, self.key + other, [chord + other for chord in self.chords])

    def __radd__(self, other: Interval):
        return self + other

    def first_chord(self):
        first_chord = self.chords[0]
        return ChordProgression(first_chord.name, self.key, [first_chord])


class ProgressionTest(unittest.TestCase):
    maxDiff = None
    d_min_7 = NamedChord("ii",
                         left_hand=SetOfNotes([
                             Note("D3"),
                         ]),
                         right_hand=SetOfNotes([
                             Note("F4"),
                             Note("C5"),
                         ]),

                         )
    e_min_7 = NamedChord("ii",
                         left_hand=SetOfNotes([
                             Note("E3"),
                         ]),
                         right_hand=SetOfNotes([
                             Note("G4"),
                             Note("D5"),
                         ]),
                         )
    three_five_c = ChordProgression(
        name="ii V I",
        key=Note("C"),
        chords=[
            d_min_7,
            NamedChord("V",
                       left_hand=SetOfNotes([
                           Note("G3"),
                       ]),
                       right_hand=SetOfNotes([
                           Note("F4"),
                           Note("B4"),
                       ]),
                       ),
            NamedChord("I",
                       left_hand=SetOfNotes([
                           Note("C3"),
                       ]),
                       right_hand=SetOfNotes([
                           Note("E4"),
                           Note("B4"),
                       ]),
                       ),
        ]
    )
    three_five_d = ChordProgression(
        name="ii V I",
        key=Note("D"),
        chords=[
            e_min_7,
            NamedChord("V",
                       left_hand=SetOfNotes([
                           Note("A3"),
                       ]),
                       right_hand=SetOfNotes([
                           Note("G4"),
                           Note("C#5"),
                       ]),
                       ),
            NamedChord("I",
                       left_hand=SetOfNotes([
                           Note("D3"),
                       ]),
                       right_hand=SetOfNotes([
                           Note("F#4"),
                           Note("C#5"),
                       ]),
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
\\score {
  <<
    \\new Lyrics {
      \\lyricmode{ii V I}
    }
    \\new PianoStaff<<
      \\new Staff {
        \\clef treble
        \\key c' \\major
        <f' c''>
        <f' b'>
        <e' b'>
      }
      \\new Staff {
        \\clef bass
        \\key c' \\major
        <d>
        <g>
        <c>
      }
    >>
  >>
}"""

    names_lily = """\
\\new Lyrics {
  \\lyricmode{ii V I}
}"""

    right_lily = """\
\\new Staff {
  \\clef treble
  \\key c' \\major
  <f' c''>
  <f' b'>
  <e' b'>
}"""

    def test_left(self):
        self.assertEquals(self.right_lily, self.three_five_c.right_lily())

    def test_lyrics(self):
        self.assertEquals(self.names_lily, self.three_five_c.chord_names_lily())

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
        self.assertEquals(self.d_min_7 + Interval(chromatic=2, diatonic=1), self.e_min_7)
        generated = self.three_five_c + Interval(chromatic=2, diatonic=1)
        self.assertEquals(generated, self.three_five_d)
