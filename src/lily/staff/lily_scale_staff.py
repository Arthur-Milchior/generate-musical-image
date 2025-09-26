from dataclasses import dataclass

from lily.staff.lily_staff import LilyStaff
from solfege.value.note.note import NoteFrozenList


@dataclass(frozen=True)
class LilyScaleStaff(LilyStaff):
    notes: NoteFrozenList
    
    def staff_content(self) -> str:
        return " ".join(note.syntax_for_lily() for note in self.notes)