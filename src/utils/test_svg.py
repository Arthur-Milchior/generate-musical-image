from dataclasses import dataclass
from typing import List
import unittest

from utils.svg import SvgGenerator, SvgLine
from utils.util import assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class FakeSvgGenerator(SvgGenerator):
    svgs: List[str]
    _width: int
    _height: int

    def __post_init__(self):
        assert_iterable_typing(self.svgs, str)
        assert_typing(self._width, int)
        assert_typing(self._height, int)

    def svg_content(self):
        return self.svgs

    def svg_width(self):
        return self._width
    
    def svg_height(self):
        return self._height


line_2 = """<style text='style/css'>"""
line_4 = """stylish"""
line_6 = """</style>"""
line_7 = """<line test/><!-- foo -->"""
line_8 = """<line test 2/>"""

class TestSvgGenerator(unittest.TestCase):
    def test_svg_line(self):
        svg_line_2 = SvgLine(line_2)
        self.assertEqual(svg_line_2.indent(), 1)
        self.assertEqual(svg_line_2.indented_line(0) , """<style text='style/css'>""")
        self.assertEqual(svg_line_2.indented_line(1) , """  <style text='style/css'>""")
        svg_line_7 = SvgLine(line_7)
        self.assertEqual(svg_line_7.indent(), 0)
        self.assertEqual(svg_line_7.indented_line(0) , """<line test/><!-- foo -->""")
        self.assertEqual(svg_line_7.indented_line(1) , """  <line test/><!-- foo -->""")

    def test_svg_file(self):
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