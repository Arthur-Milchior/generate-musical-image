from dataclasses import dataclass
from typing import List
import unittest

from utils.svg.svg_generator import SvgGenerator, _SvgLine
from utils.util import assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class FakeSvgGenerator(SvgGenerator):
    """Minimal `SvgGenerator` fixture: returns a fixed list of lines and fixed dimensions, for testing the base
    class's `svg()` assembly logic without any real drawing."""

    svgs: List[str]
    """The raw lines to return from `svg_lines()`."""

    _width: int
    """Fixed value returned by `svg_width()`."""

    _height: int
    """Fixed value returned by `svg_height()`."""

    def __post_init__(self) -> None:
        """Sanity-check the field types."""
        assert_iterable_typing(self.svgs, str)
        assert_typing(self._width, int)
        assert_typing(self._height, int)

    def svg_lines(self) -> List[str]:
        """Return the fixed `svgs` lines."""
        return self.svgs

    def svg_width(self) -> int:
        """Return the fixed `_width`."""
        return self._width

    def svg_height(self) -> int:
        """Return the fixed `_height`."""
        return self._height

    def _svg_name_base(self, **kwargs) -> str:
        """Fixed file-name base, `"fake_svg"`."""
        return "fake_svg"


line_2 = """<style text='style/css'>"""
line_4 = """stylish"""
line_6 = """</style>"""
line_7 = """<line test/><!-- foo -->"""
line_8 = """<line test 2/>"""

class TestSvgGenerator(unittest.TestCase):
    """Tests for `_SvgLine` indentation detection and `SvgGenerator.svg()` assembly."""

    def test_svg_line(self) -> None:
        """`_SvgLine` detects opening/closing-tag indentation and renders itself indented by a given amount."""
        svg_line_2 = _SvgLine(line_2)
        self.assertEqual(svg_line_2.indent(), 1)
        self.assertEqual(svg_line_2.indented_line(0) , """<style text='style/css'>""")
        self.assertEqual(svg_line_2.indented_line(1) , """  <style text='style/css'>""")
        svg_line_7 = _SvgLine(line_7)
        self.assertEqual(svg_line_7.indent(), 0)
        self.assertEqual(svg_line_7.indented_line(0) , """<line test/><!-- foo -->""")
        self.assertEqual(svg_line_7.indented_line(1) , """  <line test/><!-- foo -->""")

    def test_svg_file(self) -> None:
        """`svg()` wraps the generator's lines in an `<svg>` root with the right dimensions, indenting each
        line according to its nesting."""
        fake = FakeSvgGenerator(
            [
    line_2,
line_4,
line_6,
line_7,
line_8,
], 42, 50)
        actual = fake.svg()
        self.assertEqual(actual, """\
<svg version='1.1' width='42' height='50' xmlns='http://www.w3.org/2000/svg'>
  <rect width='100%' height='100%' fill='white'/>
  <style text='style/css'>
    stylish
  </style>
  <line test/><!-- foo -->
  <line test 2/>
</svg>"""
                         )