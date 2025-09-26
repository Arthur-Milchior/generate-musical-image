from dataclasses import dataclass

from lily.sheet.lily_sheet import LilySheet
from lily.staff.lily_staff import LilyStaff


@dataclass(frozen=True)
class LilySheetSingleStaff(LilySheet):
    staff: LilyStaff

    def _lily_code(self) -> str:
        return self.staff.staff_lily_code()
