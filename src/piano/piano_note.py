import unittest
from typing import Optional, List

from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.note import Note


class PianoNote(Note):
    """Represents a note played on the keyboard."""
    finger: int
    ClassToTransposeTo = Note

    def __init__(self, name: Optional[str] = None, finger: Optional[int] = None, *args, **kwargs):
        # none used for default argument
        assert finger is not None
        super().__init__(name, *args, **kwargs)
        self.finger = finger

    @staticmethod
    def from_note_and_finger(note: Note, finger: int):
        return PianoNote(chromatic=note.get_chromatic().value, diatonic=note.get_diatonic().value, finger=finger)

    @staticmethod
    def from_name(name: str, finger: int):
        PianoNote.from_note_and_finger(Note(name), finger)

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
        return f"""PianoNote(chromatic={self.get_number()}, diatonic={self.get_diatonic().value}, finger={self.finger})"""

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


class TestPianoNote(unittest.TestCase):
    def test_lily(self):
        self.assertEquals(PianoNote(chromatic=0, diatonic=0, finger=1).lily_in_scale(), "c'-1")

    def test_next_finger(self):
        for adjacent in (True, False):
            for pinky_side in range(1, 6):
                for thumb_side in PianoNote("C", finger=pinky_side).valid_next_fingers_in_thumb_direction(adjacent):
                    self.assertTrue(
                        pinky_side in PianoNote("C", finger=thumb_side).valid_next_fingers_in_pinky_direction(adjacent))
            for thumb_side in range(1, 6):
                for pinky_side in PianoNote("C", finger=thumb_side).valid_next_fingers_in_pinky_direction(adjacent):
                    self.assertTrue(
                        thumb_side in PianoNote("C", finger=pinky_side).valid_next_fingers_in_thumb_direction(adjacent))

    def test_valid_next_fingers_for_same_note(self):
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers_for_same_note(), [1, 2])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers_for_same_note(), [1, 2, 3])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers_for_same_note(), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers_for_same_note(), [3, 4, 5])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers_for_same_note(), [4, 5])

    def test_valid_next_finger_pinky_side(self):
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers_in_pinky_direction(adjacent=True), [2])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers_in_pinky_direction(adjacent=True), [3, 1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers_in_pinky_direction(adjacent=True), [4, 1])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers_in_pinky_direction(adjacent=True), [5, 1])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers_in_pinky_direction(adjacent=True), [])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers_in_pinky_direction(adjacent=False), [2, 3, 4, 5])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers_in_pinky_direction(adjacent=False), [3, 1, 4, 5])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers_in_pinky_direction(adjacent=False), [4, 1, 5])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers_in_pinky_direction(adjacent=False), [5, 1])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers_in_pinky_direction(adjacent=False), [])

    def test_valid_next_finger_thumb_side(self):
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers_in_thumb_direction(adjacent=True), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers_in_thumb_direction(adjacent=True), [1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers_in_thumb_direction(adjacent=True), [2])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers_in_thumb_direction(adjacent=True), [3])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers_in_thumb_direction(adjacent=True), [4])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers_in_thumb_direction(adjacent=False), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers_in_thumb_direction(adjacent=False), [1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers_in_thumb_direction(adjacent=False), [1, 2])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers_in_thumb_direction(adjacent=False), [1, 2, 3])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers_in_thumb_direction(adjacent=False), [1, 2, 3, 4])

    def test_valid_next_fingers(self):
        # same note
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("C"), for_right_hand=True), [1, 2])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("C"), for_right_hand=True), [1, 2, 3])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("C"), for_right_hand=True), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("C"), for_right_hand=True), [3, 4, 5])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("C"), for_right_hand=True), [4, 5])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("C"), for_right_hand=False), [1, 2])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("C"), for_right_hand=False), [1, 2, 3])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("C"), for_right_hand=False), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("C"), for_right_hand=False), [3, 4, 5])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("C"), for_right_hand=False), [4, 5])

        # pinky side
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("B3"), for_right_hand=False), [2])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("B3"), for_right_hand=False), [3, 1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("B3"), for_right_hand=False), [4, 1])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("B3"), for_right_hand=False), [5, 1])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("B3"), for_right_hand=False), [])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("A3"), for_right_hand=False), [2, 3, 4, 5])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("A3"), for_right_hand=False), [3, 1, 4, 5])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("A3"), for_right_hand=False), [4, 1, 5])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("A3"), for_right_hand=False), [5, 1])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("A3"), for_right_hand=False), [])

        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("D"), for_right_hand=True), [2])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("D"), for_right_hand=True), [3, 1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("D"), for_right_hand=True), [4, 1])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("D"), for_right_hand=True), [5, 1])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("D"), for_right_hand=True), [])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("E"), for_right_hand=True), [2, 3, 4, 5])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("E"), for_right_hand=True), [3, 1, 4, 5])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("E"), for_right_hand=True), [4, 1, 5])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("E"), for_right_hand=True), [5, 1])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("E"), for_right_hand=True), [])

        # thumb side
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("D"), for_right_hand=False), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("D"), for_right_hand=False), [1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("D"), for_right_hand=False), [2])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("D"), for_right_hand=False), [3])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("D"), for_right_hand=False), [4])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("E"), for_right_hand=False), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("E"), for_right_hand=False), [1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("E"), for_right_hand=False), [1, 2])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("E"), for_right_hand=False), [1, 2, 3])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("E"), for_right_hand=False), [1, 2, 3, 4])

        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("B3"), for_right_hand=True), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("B3"), for_right_hand=True), [1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("B3"), for_right_hand=True), [2])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("B3"), for_right_hand=True), [3])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("B3"), for_right_hand=True), [4])
        self.assertEquals(PianoNote("C", finger=1).valid_next_fingers(Note("A3"), for_right_hand=True), [2, 3, 4])
        self.assertEquals(PianoNote("C", finger=2).valid_next_fingers(Note("A3"), for_right_hand=True), [1])
        self.assertEquals(PianoNote("C", finger=3).valid_next_fingers(Note("A3"), for_right_hand=True), [1, 2])
        self.assertEquals(PianoNote("C", finger=4).valid_next_fingers(Note("A3"), for_right_hand=True), [1, 2, 3])
        self.assertEquals(PianoNote("C", finger=5).valid_next_fingers(Note("A3"), for_right_hand=True), [1, 2, 3, 4])