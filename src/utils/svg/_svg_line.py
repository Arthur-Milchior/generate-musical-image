
"""Number of space in an indentation."""
INDENT_SIZE = 2

from dataclasses import dataclass
import re

from utils.util import assert_typing


@dataclass(frozen=True)
class _SvgLine:
    """Allow to extract information from svg line."""

    line: str
    """The raw line content, expected to already be a single tag/text fragment with no leading/trailing
    whitespace and no more than one `<`/`>` pair outside of comments."""

    def _line_without_comment(self) -> str:
        """Return `line` with any `<!--...-->` XML comment stripped, for tag-shape checks that shouldn't be
        confused by comment text."""
        return re.sub(r"<!--[^>]*-->", "", self.line)

    def __post_init__(self) -> None:
        """Sanity-check `line`: no surrounding whitespace, and (ignoring a trailing comment) at most one tag
        delimiter pair."""
        assert_typing(self.line, str)
        line = self._line_without_comment()
        assert self.line.strip() == self.line
        assert "<" not in line[1:]
        assert ">" not in line[:-1]

    def indent(self) -> int:
        """Return the indent delta this line contributes: `-1` for a closing tag (`</...>`), `+1` for an opening
        tag that isn't self-closing, `0` for a self-closing tag (`.../>`) or plain text/other content."""
        line = self._line_without_comment()
        if line.startswith("</"):
            return -1
        if line.startswith("<"):
            if line.endswith("/>"):
                return 0
            return 1
        return 0

    def indented_line(self, indent: int) -> str:
        """Return `line` prefixed with `indent` levels of `INDENT_SIZE` spaces each."""
        return (" "*INDENT_SIZE * indent) + self.line