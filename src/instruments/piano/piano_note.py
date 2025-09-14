from dataclasses import dataclass
from typing import Optional, List, Self, Union

from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note
from solfege.value.note.abstract_note import NoteOutput


@dataclass(frozen=True)
class PianoNote(Note):
    """Represents a note played on the keyboard."""
    finger: int

    @classmethod
    def make_instance_of_selfs_class(cls, chromatic, diatonic):
        return Note(chromatic, diatonic)

    def __post_init__(self):
        super().__post_init__()
        assert 1<=self.finger<=5

    @classmethod
    def make(cls,
             chromatic: Union[ChromaticNote, int],
             diatonic: Union[DiatonicNote, int],
             finger=int) -> Self:
        note = Note.make(chromatic=chromatic, diatonic=diatonic)
        assert 1<=finger<=5
        return cls.from_note_and_finger(note=note, finger=finger)

    @staticmethod
    def from_note_and_finger(note: Note, finger: int):
        return PianoNote(chromatic=note.get_chromatic(), diatonic=note.get_diatonic(), finger=finger)

    @staticmethod
    def from_name(name: str, finger: int):
        return PianoNote.from_note_and_finger(Note.from_name(name), finger)

    def __eq__(self, other):
        if isinstance(other, PianoNote):
            if self.finger != other.finger:
                return False
        return self.value == other.value and self.get_diatonic() == other.get_diatonic()

    def __hash__(self):
        return hash((super().__hash__(), self.finger))

    def __str__(self):
        return f"{super().__str__()}-{self.finger}"

    def lily_comment(self):
        return str(self.finger)

    def lily_in_scale(self):
        try:
            return f"{super().lily_in_scale()}-{self.finger}"
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

    def __repr__(self):
        return f"""PianoNote.make(chromatic={self.value}, diatonic={self.get_diatonic().value}, finger={self.finger})"""

    def valid_next_fingers(self, next_note: Note, for_right_hand: bool):
        if self == next_note:
            return self.valid_next_fingers_for_same_note()
        toward_thumb_side = (self > next_note) == for_right_hand
        if toward_thumb_side:
            return self.valid_next_fingers_in_thumb_direction(self.adjacent(next_note))
        else:
            return self.valid_next_fingers_in_pinky_direction(self.adjacent(next_note))

    def valid_next_fingers_for_same_note(self) -> List[int]:
        return [[1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5]][self.finger - 1]

    def valid_next_fingers_in_pinky_direction(self, adjacent: bool) -> List[int]:
        if self.finger == 5:
            return []
        l = [self.finger + 1]
        if self.finger > 1:
            l.append(1)
        if not adjacent:
            # TODO: Improve with the interval size
            for f in range(self.finger + 2, 6):
                l.append(f)
        return l

    def valid_next_fingers_in_thumb_direction(self, adjacent: bool) -> List[int]:
        if self.finger == 1:
            return [2, 3, 4]
        if self.finger == 2:
            return [1]
        if adjacent:
            return [self.finger - 1]
        return list(range(1, self.finger))


