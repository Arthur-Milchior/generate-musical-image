from __future__ import annotations
from dataclasses import dataclass

from solfege.value.interval.diatonic_interval import DiatonicIntervalFrozenList
from solfege.value.note.abstract_note import FixedLengthOutput, NoteOutput
from solfege.value.note.alteration import LILY, FILE_NAME, FULL_NAME, DEBUG, NAME_UP_TO_OCTAVE
from typing import assert_never
from solfege.value.note.abstract_note import FixedLengthOutput, NoteOutput
from solfege.value.diatonic import Diatonic
from solfege.value.note.singleton_note import AbstractSingletonNote
from utils.frozenlist import FrozenList
from utils.util import assert_equal_length

french_fixed_length_space = ["do ", "re ", "mi ", "fa ", "sol", "la ", "si "]
assert_equal_length(french_fixed_length_space)

@dataclass(frozen=True, eq=False)
class DiatonicNote(AbstractSingletonNote, Diatonic):
    """A diatonic note. Implemented as interval from C4"""

    def get_name_up_to_octave(self, note_output: NoteOutput, fixed_length: FixedLengthOutput) -> str:
        if note_output == NoteOutput.LILY:
            return ["c", "d", "e", "f", "g", "a", "b"][self.value % 7]
        elif note_output == NoteOutput.FRENCH:
            if fixed_length == FixedLengthOutput.NO:
                return ["do", "re", "mi", "fa", "sol", "la", "si"][self.value % 7]
            else:
                return french_fixed_length_space[self.value % 7]
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


class DiatonicNoteFrozenList(FrozenList[DiatonicNote]):
    type = DiatonicNote

DiatonicIntervalFrozenList.note_frozen_list_type = DiatonicNoteFrozenList