from dataclasses import dataclass

from lily.staff.lily_staff import LilyStaff
from solfege.value.note.note import NoteFrozenList


@dataclass(frozen=True)
class LilyScaleStaff(LilyStaff):
    """A staff rendering a scale (or arpeggio) as a sequence of individual, successive notes, unlike
    `LilyChordStaff` which stacks them into one simultaneous chord."""
    notes: NoteFrozenList
    """The notes of the scale/arpeggio, rendered one after another in order."""

    def staff_content(self) -> str:
        """The LilyPond code for the notes, space-separated, each rendered by `Note.syntax_for_lily()`."""
        return " ".join(note.syntax_for_lily() for note in self.notes)