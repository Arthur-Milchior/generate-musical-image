
from abc import ABC, abstractmethod
from typing import Iterator


class SvgLines(ABC):
    """Protocol for "this object knows how to render itself as a sequence of raw SVG lines" — the content
    `SvgGenerator.svg()` wraps in an `<svg>` root."""

    @abstractmethod
    def svg_lines(self) -> Iterator[str]:
        """Yield this object's SVG content, one tag/text fragment per line (see `_SvgLine` for the shape each
        line is expected to have when auto-indented by `SvgGenerator.svg()`)."""