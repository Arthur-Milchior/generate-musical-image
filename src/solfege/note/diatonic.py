from __future__ import annotations

from solfege.interval.diatonic import DiatonicInterval
from solfege.note.abstract import AbstractNote
from solfege.note.alteration import LILY, FILE_NAME, FULL_NAME, DEBUG, NAME_UP_TO_OCTAVE


class DiatonicNote(AbstractNote, DiatonicInterval):
    """A diatonic note"""
    # Saved as the interval from middle C
    IntervalClass = DiatonicInterval

    def lily_in_scale(self):
        return ["c", "d", "e", "f", "g", "a", "b"][self.get_number() % 7]

    def get_name_up_to_octave(self):
        return ["C", "D", "E", "F", "G", "A", "B"][self.get_number() % 7]

    def get_octave_name_lily(self):
        """How to write the octave.

        Example: "'"
        """
        # must be separated from note name, because, in lilypond, the alteration is between the note name and the octave
        if self.get_octave() >= 0:
            return "'" * (self.get_octave()+1)
        return "," * (-self.get_octave()-1)

    def get_octave_name_ascii(self):
        """How to write the octave.

        Example: 4
        """
        # must be separated from note name, because, in lilypond, the alteration is between the note name and the octave
        return str(self.get_octave(scientific_notation=True))

    def get_name_with_octave(self):
        """Example C4"""
        return f"{self.get_name_up_to_octave()}{self.get_octave_name_ascii()}"


    @staticmethod
    def from_name(name: str):
        assert 1 <= len(name) <= 2
        letter = name[0].lower()
        note = DiatonicNote({"c": 0, "d": 1, "e": 2, "f": 3, "g": 4, "a": 5, "b": 6}[letter])
        if len(name) == 2:
            octave = int(name[1])
            note = note.add_octave(octave - 4)
        return note
