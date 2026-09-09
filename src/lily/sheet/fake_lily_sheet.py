from dataclasses import dataclass
from lily.sheet.lily_sheet import LilySheet


@dataclass(frozen=True)
class FakeLilySheet(LilySheet):
    """Test double for `LilySheet` with fixed `file_prefix`/content, useful for exercising `LilySheet`'s
    file-writing/compiling machinery without a real staff."""
    prefix: str
    """The fixed value returned by `file_prefix()`."""
    staff_code: str
    """The fixed LilyPond content string returned by `lily_staff_code()`."""

    def file_prefix(self) -> str:
        """Return the fixed `prefix` given at construction."""
        return self.prefix

    def lily_staff_code(self) -> str:
        """Return the fixed `staff_code` given at construction."""
        return self.staff_code