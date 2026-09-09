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
    """The finger (1 = thumb, ..., 5 = pinky) used to play this note."""

    @classmethod
    def make_instance_of_selfs_class(cls, _chromatic, _diatonic):
        """Build the plain `Note` (not a `PianoNote`) resulting from arithmetic on this note.

        Overrides `AbstractNote.make_instance_of_selfs_class` so that adding/subtracting an interval to/from a
        `PianoNote` yields a plain `Note`: the result no longer corresponds to a specific finger, so it would be
        meaningless to keep `self.finger` around."""
        return Note.make(_chromatic, _diatonic)

    def __post_init__(self):
        """Validate the note, then check that `finger` is a legal finger number (1 to 5)."""
        super().__post_init__()
        assert 1<=self.finger<=5

    @classmethod
    def make(cls,
             chromatic: Union[ChromaticNote, int],
             diatonic: Union[DiatonicNote, int],
             finger=int) -> Self:
        """Create a `PianoNote` from chromatic/diatonic values and a finger number.

        `chromatic`/`diatonic` may be raw ints or `ChromaticNote`/`DiatonicNote` instances, as accepted by
        `Note.make`."""
        note = Note.make(_chromatic=chromatic, _diatonic=diatonic)
        assert 1<=finger<=5
        return cls.from_note_and_finger(note=note, finger=finger)

    @staticmethod
    def from_note_and_finger(note: Note, finger: int):
        """Return the `PianoNote` obtained by attaching `finger` to an existing `note`."""
        return PianoNote(_chromatic=note.get_chromatic(), _diatonic=note.get_diatonic(), finger=finger)

    @staticmethod
    def from_name(name: str, finger: int):
        """Return the `PianoNote` for the note spelled `name` (e.g. "C#4"), played with `finger`."""
        return PianoNote.from_note_and_finger(Note.from_name(name), finger)

    def __eq__(self, other):
        """Equal to another `PianoNote` with the same pitch and finger, or to a plain `Note`/pitch with the same
        pitch (finger is then ignored)."""
        if isinstance(other, PianoNote):
            if self.finger != other.finger:
                return False
        return self.value == other.value and self.get_diatonic() == other.get_diatonic()

    def __hash__(self):
        """Hash combining the underlying note's hash with the finger."""
        return hash((super().__hash__(), self.finger))

    def __str__(self):
        """Human-readable form: the note's own string representation, suffixed with `-<finger>`."""
        return f"{super().__str__()}-{self.finger}"

    def lily_comment(self):
        """LilyPond comment text (just the finger number) attached to this note when rendering."""
        return str(self.finger)

    def syntax_for_lily(self):
        """LilyPond syntax for this note, suffixed with `-<finger>` so LilyPond prints the fingering annotation.

        Re-raises `TooBigAlterationException` from the parent with this note attached for context."""
        try:
            return f"{super().syntax_for_lily()}-{self.finger}"
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

    def __repr__(self):
        """`eval`-able representation, reconstructing this `PianoNote` via `PianoNote.make`."""
        return f"""PianoNote.make(_chromatic={self.value}, _diatonic={self.get_diatonic().value}, finger={self.finger})"""

    def valid_next_fingers(self, next_note: Note, for_right_hand: bool):
        """Return the fingers that may legally play `next_note` right after this note.

        Dispatches to `valid_next_fingers_for_same_note` if `next_note` is the same pitch, otherwise to
        `valid_next_fingers_in_thumb_direction`/`valid_next_fingers_in_pinky_direction` depending on whether
        `next_note` lies toward the thumb or the pinky side of the hand (which depends on both the melodic
        direction and `for_right_hand`)."""
        if self == next_note:
            return self.valid_next_fingers_for_same_note()
        toward_thumb_side = (self > next_note) == for_right_hand
        if toward_thumb_side:
            return self.valid_next_fingers_in_thumb_direction(self.adjacent(next_note))
        else:
            return self.valid_next_fingers_in_pinky_direction(self.adjacent(next_note))

    def valid_next_fingers_for_same_note(self) -> List[int]:
        """Return the fingers that may replay the same pitch right after `self.finger` (finger substitution)."""
        return [[1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5]][self.finger - 1]

    def valid_next_fingers_in_pinky_direction(self, adjacent: bool) -> List[int]:
        """Return the fingers that may play the next note toward the pinky side of the hand.

        If `adjacent` is true, only the immediately next finger (plus the thumb, which can always cross under)
        is allowed; otherwise any finger further toward the pinky is also allowed (crossing under further, with
        a TODO to further restrict based on the actual interval size)."""
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
        """Return the fingers that may play the next note toward the thumb side of the hand.

        The thumb (1) can pass under to reach fingers 2-4; finger 2 can only be followed by the thumb passing
        under it. If `adjacent` is true, only the immediately previous finger is allowed; otherwise any finger
        further toward the thumb is also allowed (the thumb crossing under further)."""
        if self.finger == 1:
            return [2, 3, 4]
        if self.finger == 2:
            return [1]
        if adjacent:
            return [self.finger - 1]
        return list(range(1, self.finger))


