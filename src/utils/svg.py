from dataclasses import dataclass
import re
from typing import List

from utils.util import assert_typing, ensure_folder, save_file

"""Number of space in an indentation."""
INDENT_SIZE = 2

@dataclass(frozen=True)
class SvgLine:
    line: str

    def _line_without_comment(self):
        return re.sub(r"<!--[^>]*-->", "", self.line)

    def __post_init__(self):
        assert_typing(self.line, str)
        line = self._line_without_comment()
        assert self.line.strip() == self.line
        assert "<" not in line[1:]
        assert ">" not in line[:-1]

    def indent(self):
        line = self._line_without_comment()
        if line.startswith("</"):
            return -1
        if line.startswith("<"):
            if line.endswith("/>"):
                return 0
            return 1
        return 0

    def indented_line(self, indent):
        return (" "*INDENT_SIZE * indent) + self.line


class SvgGenerator:    
    def svg_name(self, *args, **kwargs) -> str:
        return f"{self._svg_name_base(*args, **kwargs)}.svg"
    
    def save_svg(self, folder_path: str, *args, **kwargs) -> str:
        """Save the svg in `folder_path`. Return the file name."""
        assert_typing(folder_path, str)
        ensure_folder(folder_path)
        svg_name = self.svg_name(*args, **kwargs)
        file_path = f"{folder_path}/{svg_name}"
        save_file(file_path, self.svg(*args, **kwargs))
        return svg_name


    def svg(self, *args, **kwargs)->str:
        svg_content = self.svg_content(*args, **kwargs)
        width = int(self.svg_width(*args, **kwargs))
        height = int(self.svg_height(*args, **kwargs))
        all_svg_lines = [
            f"""<svg version='1.1' width='{width}' height='{height}' xmlns='http://www.w3.org/2000/svg'>""",
            """<rect width='100%' height='100%' fill='white'/>""",
            *svg_content,
            "</svg>"
        ]
        total_indent = 0
        indented_content = []
        for line in all_svg_lines:
            svg_line = SvgLine(line)
            new_indent = svg_line.indent()
            # Dedent but don't indent yet.
            current_indent = total_indent if new_indent > 0 else total_indent + new_indent
            indented_line = svg_line.indented_line(current_indent)
            indented_content.append(indented_line)
            total_indent += new_indent
            
        return "\n".join(f'{content}' for content in indented_content)
    
    #Must be implemented by subclasses
    def _svg_content(self) -> List[str]:
        """The content of the svg. Not containig svg itself and the white background."""
        return NotImplemented
    
    def _svg_name_base(self) -> str:
        return NotImplemented
    
    def svg_height(self) -> int: 
        "Returns the height of svg. Must accept same argument as svg"
        return NotImplemented
    
    def svg_width(self, *args, **kwargs) -> int: 
        "Returns the width of svg. Must accept same argument as svg"
        return NotImplemented