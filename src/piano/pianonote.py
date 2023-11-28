import unittest

from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.note import Note


class PianoNote(Note):
    """Represents a note played on the keyboard."""
    finger: int
    ClassToTransposeTo = Note

    @staticmethod
    def from_note_and_finger(note: Note, finger: int):
        return PianoNote(chromatic=note.get_chromatic().value, diatonic=note.get_diatonic().value, finger=finger)


    @staticmethod
    def from_name(name: str, finger:int):
        PianoNote.from_note_and_finger(Note.from_name(name), finger)

    def __eq__(self, other):
        if isinstance(other, PianoNote):
            if self.finger != other.finger:
                return False
        return self.value == other.value and self.get_diatonic() == other.get_diatonic()

    def __hash__(self):
        return hash((super().__hash__(), self.finger))

    def __init__(self, chromatic: int, diatonic: int, finger: int):
        super().__init__(chromatic=chromatic, diatonic=diatonic)
        self.finger = finger

    def __str__(self):
        return f"{super().__str__()}-{self.finger}"

    def lily_comment(self):
        return str(self.finger)

    def lily(self):
        try:
            return f"{super().lily()}-{self.finger}"
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

    def __repr__(self):
        return f"""PianoNote(chromatic={self.get_number()}, diatonic={self.get_diatonic().value}, finger={self.finger})"""


class TestPianoNote(unittest.TestCase):
    def test_lily(self):
        self.assertEquals(PianoNote(chromatic=0, diatonic=0, finger=1).lily(), "c'-1")
