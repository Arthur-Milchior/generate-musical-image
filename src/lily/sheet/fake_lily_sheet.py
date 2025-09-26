from dataclasses import dataclass
from lily.sheet.lily_sheet import LilySheet


@dataclass(frozen=True)
class FakeLilySheet(LilySheet):
    prefix: str
    staff_code: str

    def file_prefix(self) -> str: 
        return self.prefix

    def lily_staff_code(self) -> str:
        return self.staff_code