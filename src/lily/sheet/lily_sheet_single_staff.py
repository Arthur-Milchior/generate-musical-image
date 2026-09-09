from dataclasses import dataclass

from lily.sheet.lily_sheet import LilySheet
from lily.staff.lily_staff import LilyStaff


@dataclass(frozen=True)
class LilySheetSingleStaff(LilySheet):
    """A `LilySheet` made of exactly one staff."""
    staff: LilyStaff
    """The single staff to render."""

    def _lily_code(self) -> str:
        """The staff's own LilyPond code, unwrapped (this sheet has no other staves to combine it with)."""
        return self.staff.staff_lily_code()
