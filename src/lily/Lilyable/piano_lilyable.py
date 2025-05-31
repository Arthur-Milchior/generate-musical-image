from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Optional, List, Iterable

from lily.Lilyable.lilyable import Lilyable
from lily.Lilyable.local_lilyable import LocalLilyable
from lily.lily import compile_
from solfege.note import Note
from utils.constants import test_folder
from utils.util import indent


class PianoLilyable(Lilyable):

    def first_key(self) -> str:
        return NotImplemented

    def right_lily(self) -> Optional[str]:
        """The lily code for the right hand scale, without the first key"""
        return NotImplemented

    def left_lily(self) -> Optional[str]:
        """The lily code for the left hand scale, without the first key"""
        return NotImplemented

    def annotations_lily(self) -> Optional[str]:
        """The lily code for the annotation"""
        return NotImplemented

    def __eq__(self, other: PianoLilyable):
        return self.first_key() == other.first_key() and self.left_lily() == other.left_lily() and self.right_lily() == other.right_lily() and self.annotations_lily() == other.annotations_lily()

    def _staff(self, clef: str, content: Optional[str]) -> Optional[str]:
        """A lilypond staff.

        The key is the given one.

        The note are decorated with the fingering given in argument.

        Bass for left hand and treble for right

        Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
        """
        if content is None:
            return None
        return f"""\\new Staff{{
  \\override Staff.TimeSignature.stencil = ##f
  \\omit Staff.BarLine
  \\omit PianoStaff.SpanBar
  \\set Staff.printKeyCancellation = ##f
  \\clef {clef}
  \\key {self.first_key()} \\major
{indent(content)}
}}"""

    def _left_staff(self) -> Optional[str]:
        return self._staff("bass", self.left_lily())

    def _right_staff(self) -> Optional[str]:
        return self._staff("treble", self.right_lily())

    def _piano_staff(self):
        left = self._left_staff()
        right = self._right_staff()
        assert left or right
        if left and right:
            return f"""\\new PianoStaff<<
{indent(right)}
{indent(left)}
>>"""
        return left or right

    def lily(self, midi: bool = False):
        midi_str = """
  #\\midi{}
  \\layout{}""" if midi else ""
        lyrics_content = self.annotations_lily()
        lyrics_str = indent(f"""
\\new Lyrics {{
  \\lyricmode{{
{indent(lyrics_content, 4)}
  }}
}}""", 4) if lyrics_content else ""
        return f"""\\version "2.20.0"
\\score{{{midi_str}
  <<{lyrics_str}
{indent(self._piano_staff(), 4)}
  >>
}}"""


@dataclass(frozen=True)
class LiteralPianoLilyable(PianoLilyable):
    _first_key: str
    _left_lily: Optional[str] = None
    _right_lily: Optional[str] = None
    _annotation: Optional[str] = None

    @staticmethod
    def factory(key: Note, left_hand: Optional[Iterable[LocalLilyable]] = None,
                right_hand: Optional[Iterable[LocalLilyable]] = None) -> LiteralPianoLilyable:
        return LiteralPianoLilyable(key.lily_in_scale(),
                                    (" ".join(l.lily_in_scale() for l in left_hand) if (
                                            left_hand is not None) else None),
                                    (" ".join(
                                        r.lily_in_scale() for r in right_hand) if right_hand is not None else None))

    def first_key(self) -> str:
        return self._first_key

    def left_lily(self) -> Optional[str]:
        return self._left_lily

    def right_lily(self) -> Optional[str]:
        return self._right_lily

    def annotations_lily(self) -> Optional[str]:
        return self._annotation


def _for_list_of_notes(fingering: List[LocalLilyable]) -> str:
    """Generate the lilypond code to put in a staff, according to the fingering given in argument.

    chooseOctave is the function which, given its argument, decide which ottava is applied (if any)
    """
    return " ".join(note.lily_in_scale() for note in fingering)


def lilypond_code_for_one_hand(key: str, notes_or_chords: List[LocalLilyable], for_right_hand: bool,
                               midi: bool) -> str:
    """A lilypond score, with a single staff.

    The key is the given one.

    The note are decorated with the fingering given in argument.

    The bass/treble key depends on the hand
    """
    fingering = _for_list_of_notes(notes_or_chords)
    right_fingering = fingering if for_right_hand else None
    left_fingering = None if for_right_hand else fingering
    return LiteralPianoLilyable(key, left_fingering, right_fingering).lily(midi)


def lilypond_code_for_two_hands(key: str, left_fingering: List[LocalLilyable], right_fingering: List[LocalLilyable],
                                midi: bool) -> str:
    """A lilypond score for piano.

    The note are decorated with the fingering given in arguments.
    """
    return LiteralPianoLilyable(key, _for_list_of_notes(left_fingering), _for_list_of_notes(right_fingering)).lily(
        midi)


class TestPianoLilyable(unittest.TestCase):
    maxDiff = None
    value = LiteralPianoLilyable("aes", "cis", "gis'", "IV")
    both_hand_annotated_expected = r"""\version "2.20.0"
\score{
#\midi{}
\layout{}
<<
\new Lyrics {
  \lyricmode{
    IV
  }
}
\new PianoStaff<<
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef treble
    \key aes \major
    gis'
  }
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \omit Staff.BarLine
    \omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef bass
    \key aes \major
    cis
  }
>>
>>
}"""

    expected_right_hand = r"""\version "2.20.0"
\score{
<<
\new Staff{
  \override Staff.TimeSignature.stencil = ##f
  \omit Staff.BarLine
  \omit PianoStaff.SpanBar
  \set Staff.printKeyCancellation = ##f
  \clef treble
  \key aes \major
  gis'
}
>>
}"""

    def test_both_hand(self):
        generated = LiteralPianoLilyable("aes", "cis", "gis'", None).lily_in_scale()
        expected = r"""\version "2.20.0"
\score{
<<
\new PianoStaff<<
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \omit Staff.BarLine
    \omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef treble
    \key aes \major
    gis'
  }
  \new Staff{
    \override Staff.TimeSignature.stencil = ##f
    \omit Staff.BarLine
    \omit PianoStaff.SpanBar
    \set Staff.printKeyCancellation = ##f
    \clef bass
    \key aes \major
    cis
  }
>>
>>
}"""
        self.assertEquals(expected, generated)

    def test_right_hand(self):
        generated = LiteralPianoLilyable("aes", None, "gis'", None).lily()
        self.assertEquals(self.expected_right_hand, generated)
        test_file_path = f"{test_folder}/piano_lily_right"
        compile_(generated, test_file_path, True, force_recompile=True)()

    def test_both_hand_annotation(self):
        generated = LiteralPianoLilyable("aes", "cis", "gis'", "IV").lily(True)
        self.assertEquals(self.both_hand_annotated_expected, generated)
        test_file_path = f"{test_folder}/piano_lily_both"
        compile_(generated, test_file_path, True, force_recompile=True)()

    def test_eq_diff_class(self):
        class MockPianoLilyable(PianoLilyable):

            def first_key(self) -> str:
                return "aes"

            def right_lily(self) -> Optional[str]:
                """The lily code for the right hand scale, without the aes key"""
                return "gis'"

            def left_lily(self) -> Optional[str]:
                """The lily code for the left hand scale, without the aes key"""
                return "cis"

            def annotations_lily(self) -> Optional[str]:
                """The lily code for the annotation"""
                return "IV"

        self.assertEquals(self.value.first_key(), "aes")
        self.assertEquals(self.value.right_lily(), "gis'")
        self.assertEquals(self.value.left_lily(), "cis")
        self.assertEquals(self.value.annotations_lily(), "IV")
        self.assertEquals(self.value, MockPianoLilyable())

    def test_eq(self):
        self.assertEquals(self.value, LiteralPianoLilyable("aes", "cis", "gis'", "IV"))
