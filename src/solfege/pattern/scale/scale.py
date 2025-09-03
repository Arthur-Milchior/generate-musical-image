from __future__ import annotations

from typing import List, Generic
from lily.Lilyable.lilyable import Lilyable
from typing import Optional, List, Iterable
from solfege.value.note.abstract_note import NoteType
from utils.util import indent
# from solfege.pattern.scale.scale_pattern import ScalePattern


class Scale(Generic[NoteType], Lilyable):
    notes: List[NoteType]
    #pattern: ScalePattern

    def __init__(self, notes: List[NoteType], pattern  #: ScalePattern
                 , key: Optional[NoteType] = None):
        self.notes = notes
        self.pattern = pattern
        self._key = key

    def all_blacks(self):
        return all(note.is_black_key_on_piano() for note in self.notes)

    def __eq__(self, other):
        return self.notes == other.notes

    def __repr__(self):
        return f"Scale(notes={self.notes}, key = {self._key})"

    def add_octave(self, nb_octave: int) -> Scale:
        return Scale([note.add_octave(nb_octave) for note in self.notes], self.pattern, key= self._key)

    def reverse(self) -> Scale:
        return Scale(list(reversed(self.notes)), self.pattern, key= self._key)

    def append_reversed(self) -> Scale:
        return self.concatenate(self.reverse())

    def concatenate(self, other: Scale, merge_note: bool = True) -> Scale:
        """Concatenation of two scales with the same pattern.
        If `merge_note`, the last note of `self` is expected to be the same as the first note of `other`"""
        # This assertion is false for melodic descending, as it's melodic natural
        #assert self.pattern == other.pattern
        assert self._key == other._key
        if merge_note:
            assert self.notes[-1] == other.notes[0]
            notes = self.notes + other.notes[1:]
        else:
            notes = self.notes + other.notes
        return Scale(notes, self.pattern, self._key)

    def key(self):
        if self._key:
            return self._key
        return self.first_key()

    def first_key(self):
        return self.notes[0]

    def lily(self, midi:bool = False) -> Optional[str]:
        """A lilypond staff.

        The key is the given one.

        The note are decorated with the fingering given in argument.

        Bass for left hand and treble for right

        Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
        """
        return f"""
\\version "2.24.3"
\\new Staff{{
  \\override Staff.TimeSignature.stencil = ##f
  \\omit Staff.BarLine
  \\omit PianoStaff.SpanBar
  \\time 30/4
  \\set Staff.printKeyCancellation = ##f
  \\clef treble
  \\key {self.key().lily_key()} \\major
{" ".join(note.lily_in_scale() for note in self.notes)}
}}"""
