from __future__ import annotations

from solfege.interval.diatonic import DiatonicInterval
from solfege.note.abstract import AbstractNote, AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.note.alteration import LILY, FILE_NAME, FULL_NAME, DEBUG, NAME_UP_TO_OCTAVE


class DiatonicNote(AbstractNote, DiatonicInterval):
    """A diatonic note"""
    # Saved as the interval from middle C
    IntervalClass = DiatonicInterval

    def get_name_up_to_octave(self, note_output: NoteOutput, fixed_length: FixedLengthOutput) -> str:
        if note_output == NoteOutput.LILY:
            return ["c", "d", "e", "f", "g", "a", "b"][self.get_number() % 7]
        elif note_output == NoteOutput.FRENCH:
            if fixed_length == FixedLengthOutput.NO:
                return ["do", "re", "mi", "fa", "sol", "la", "si"][self.get_number() % 7]
            else:
                return ["do ", "re ", "mi ", "fa ", "sol", "la ", "si "][self.get_number() % 7]
        elif note_output == NoteOutput.LETTER:
            return ["C", "D", "E", "F", "G", "A", "B"][self.get_number() % 7]
        elif note_output == NoteOutput.NUMBER:
            return ["1", "2", "3", "4", "5", "6", "7"][self.get_number() % 7]
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
