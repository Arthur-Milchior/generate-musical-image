
from abc import abstractmethod
from typing import Iterator

from utils.svg.svg_lines import SvgLines


class SvgLine(SvgLines):
    """`SvgLines` specialization for generators that only ever produce a single line of SVG."""

    @abstractmethod
    def svg_line(self) -> str:
        """Return the single SVG line this object renders to."""

    #pragma mark - SvgLines
    def svg_lines(self) -> Iterator[str]:
        """Yield the single line from `svg_line()`."""
        yield self.svg_line()