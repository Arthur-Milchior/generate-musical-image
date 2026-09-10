from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import Iterator, List

from utils.svg._svg_line import _SvgLine
from utils.svg.svg_lines import SvgLines
from utils.svg.svg_saver import SvgSaver
from utils.util import assert_iterable_typing, assert_typing, ensure_folder, save_file

class SvgGenerator(SvgSaver, SvgLines):
    """Implements `SvgSaver.svg()` by wrapping `SvgLines.svg_lines()`'s content in an `<svg>` root (with a white
    background rect) and auto-indenting every line according to its tag nesting, via `_SvgLine`."""

    #pragma mark - SvgSaver

    def svg(self, **kwargs)->str:
        """Assemble the full SVG document: `<svg>` header sized from `svg_width`/`svg_height`, a white background
        rect, then `svg_lines(**kwargs)`, each line re-indented based on whether it opens/closes/is a leaf tag
        (tracked via `_SvgLine.indent()`, dedenting closing tags before they're rendered)."""
        svg_content = list(self.svg_lines(**kwargs))
        assert_iterable_typing(svg_content, str)
        width = int(self.svg_width(**kwargs))
        height = int(self.svg_height(**kwargs))
        all_svg_lines = [
            f"""<svg version='1.1' width='{width}' height='{height}' xmlns='http://www.w3.org/2000/svg'>""",
            """<rect width='100%' height='100%' fill='white'/>""",
            *svg_content,
            "</svg>"
        ]
        total_indent = 0
        indented_content = []
        for line in all_svg_lines:
            svg_line = _SvgLine(line)
            new_indent = svg_line.indent()
            # Dedent but don't indent yet.
            current_indent = total_indent if new_indent > 0 else total_indent + new_indent
            indented_line = svg_line.indented_line(current_indent)
            indented_content.append(indented_line)
            total_indent += new_indent
            
        return "\n".join(f'{content}' for content in indented_content)
    
    #Must be implemented by subclasses
    @abstractmethod
    def svg_lines(self) -> List[str]:
        """The content of the svg. Not containig svg itself and the white background."""
        ...

    @abstractmethod
    def _svg_name_base(self, **kwargs) -> str:
        """The base of the output file name, without extension (see `SvgSaver.svg_name`)."""
        ...

    @abstractmethod
    def svg_height(self) -> int:
        "Returns the height of svg. Must accept same argument as svg"
        ...

    @abstractmethod
    def svg_width(self, **kwargs) -> int:
        "Returns the width of svg. Must accept same argument as svg"
        ...
