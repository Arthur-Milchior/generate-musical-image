from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Iterable

from _lily.Lilyable.lilyable import Lilyable
from _lily.Lilyable.local_lilyable import LocalLilyable
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from solfege.value.note.abstract_note import NoteOutput
from utils.constants import test_folder
from utils.util import assert_typing, indent


class PianoLilyable(Lilyable, ABC):
    """A `Lilyable` specialized to piano: knows how to render itself as a left-hand staff (bass clef), a
    right-hand staff (treble clef), and optional annotation lyrics, then combines whichever of those are
    present into a full `\\score` via `lily()`."""

    @abstractmethod
    def first_key(self) -> str:
        """The key signature (as a LilyPond key name, e.g. `"aes"`) this piece starts in."""
        ...

    @abstractmethod
    def right_lily(self) -> Optional[str]:
        """The lily code for the right hand scale, without the first key"""
        ...

    @abstractmethod
    def left_lily(self) -> Optional[str]:
        """The lily code for the left hand scale, without the first key"""
        ...

    @abstractmethod
    def annotations_lily(self) -> Optional[str]:
        """The lily code for the annotation"""
        ...

    def __eq__(self, other: PianoLilyable):
        """Two `PianoLilyable`s are equal if they share the same first key, left/right-hand code, and
        annotations."""
        return self.first_key() == other.first_key() and self.left_lily() == other.left_lily() and self.right_lily() == other.right_lily() and self.annotations_lily() == other.annotations_lily()

    def _staff(self, clef: Clef, content: Optional[str]) -> Optional[str]:
        """A lilypond staff.

        The key is the given one.

        The note are decorated with the fingering given in argument.

        Bass for left hand and treble for right

        Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
        """
        assert_typing(clef, Clef)
        if content is None:
            return None
        return f"""\\new Staff{{
  \\override Staff.TimeSignature.stencil = ##f
  \\omit Staff.BarLine
  \\omit PianoStaff.SpanBar
  \\time 30/4
  \\set Staff.printKeyCancellation = ##f
  \\clef {clef}
  \\key {self.first_key()} \\major
{indent(content)}
}}"""

    def _left_staff(self) -> Optional[str]:
        """The bass-clef staff for the left hand, or `None` if `left_lily()` is `None`."""
        return self._staff("bass", self.left_lily())

    def _right_staff(self) -> Optional[str]:
        """The treble-clef staff for the right hand, or `None` if `right_lily()` is `None`."""
        return self._staff("treble", self.right_lily())

    def _piano_staff(self):
        """The combined staff group: a `\\new PianoStaff<<...>>` with both hands if both are present, or just
        the single present staff otherwise. Asserts at least one hand is present."""
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
        """The full `\\score{...}` block: the piano staff group, plus a `\\new Lyrics` block for the annotation
        if any, plus a `\\midi{}`/`\\layout{}` block if `midi` is true."""
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
    """A `PianoLilyable` whose key/left/right/annotation code is given explicitly (fixed strings), rather than
    computed from music-theory objects. Used as the concrete leaf that other code (e.g. `ListPianoLilyable`,
    `lilypond_code_for_one_hand`/`lilypond_code_for_two_hands`) builds and combines, and as a fake in tests."""
    _first_key: str
    """The fixed key signature name (LilyPond syntax, e.g. `"aes"`) returned by `first_key()`."""
    _left_lily: Optional[str] = None
    """The fixed left-hand LilyPond code returned by `left_lily()`, or `None` if there is no left hand."""
    _right_lily: Optional[str] = None
    """The fixed right-hand LilyPond code returned by `right_lily()`, or `None` if there is no right hand."""
    _annotation: Optional[str] = None
    """The fixed annotation lyrics returned by `annotations_lily()`, or `None` if there is no annotation."""

    @staticmethod
    def make(key: Note, left_hand: Optional[Iterable[LocalLilyable]] = None,
                right_hand: Optional[Iterable[LocalLilyable]] = None) -> LiteralPianoLilyable:
        """Build a `LiteralPianoLilyable` from a `key` note and, for each hand, an optional iterable of
        `LocalLilyable`s whose `syntax_for_lily()` are joined with spaces (`None` if the hand isn't given)."""
        return LiteralPianoLilyable(key.lily_key(),
                                    (" ".join(l.syntax_for_lily() for l in left_hand) if (
                                            left_hand is not None) else None),
                                    (" ".join(
                                        r.syntax_for_lily() for r in right_hand) if right_hand is not None else None))

    def first_key(self) -> str:
        """Return the fixed `_first_key`."""
        return self._first_key

    def left_lily(self) -> Optional[str]:
        """Return the fixed `_left_lily`."""
        return self._left_lily

    def right_lily(self) -> Optional[str]:
        """Return the fixed `_right_lily`."""
        return self._right_lily

    def annotations_lily(self) -> Optional[str]:
        """Return the fixed `_annotation`."""
        return self._annotation


def _for_list_of_notes(fingering: List[LocalLilyable]) -> str:
    """Generate the lilypond code to put in a staff, according to the fingering given in argument.

    chooseOctave is the function which, given its argument, decide which ottava is applied (if any)
    """
    return " ".join(note.syntax_for_lily() for note in fingering)


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


