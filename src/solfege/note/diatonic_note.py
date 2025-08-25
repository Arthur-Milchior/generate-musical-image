from __future__ import annotations

from solfege.note.abstract_note import FixedLengthOutput, NoteOutput
from solfege.note.alteration import LILY, FILE_NAME, FULL_NAME, DEBUG, NAME_UP_TO_OCTAVE
from typing import assert_never
from solfege.note.abstract_note import FixedLengthOutput, NoteOutput
from solfege.value.diatonic import Diatonic
from solfege.note.singleton_note import AbstractSingletonNote


class DiatonicNote(AbstractSingletonNote, Diatonic):
    """A diatonic note. Implemented as interval from C4"""

    def get_name_up_to_octave(self, note_output: NoteOutput, fixed_length: FixedLengthOutput) -> str:
        if note_output == NoteOutput.LILY:
            return ["c", "d", "e", "f", "g", "a", "b"][self.value % 7]
        elif note_output == NoteOutput.FRENCH:
            if fixed_length == FixedLengthOutput.NO:
                return ["do", "re", "mi", "fa", "sol", "la", "si"][self.value % 7]
            else:
                return ["do ", "re ", "mi ", "fa ", "sol", "la ", "si "][self.value % 7]
        elif note_output == NoteOutput.LETTER:
            return ["C", "D", "E", "F", "G", "A", "B"][self.value % 7]
        elif note_output == NoteOutput.NUMBER:
            return ["1", "2", "3", "4", "5", "6", "7"][self.value % 7]
        assert_never(note_output)

    @staticmethod
    def from_name(name: str):
        """Get name assumed to be in notation with letter. Only consider the first letter, A, B,.., G"""
        assert 1 <= len(name) <= 2
        letter = name[0].lower()
        note = DiatonicNote({"c": 0, "d": 1, "e": 2, "f": 3, "g": 4, "a": 5, "b": 6}[letter])
        if len(name) == 2:
            octave = int(name[1])
            note = note.add_octave(octave - 4)
        return note

DiatonicNote.DiatonicClass = DiatonicNote
