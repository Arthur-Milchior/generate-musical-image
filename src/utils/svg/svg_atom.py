"""Smallest, single-tag SVG building blocks (a `<circle>`, a `<text>`), used by higher-level SVG generators
across the codebase instead of hand-writing SVG markup."""

from typing import Iterator, Optional

def svg_circle(x: int, y:int, radius: int, fill:str, stroke_color: str, stroke_width:int) -> str:
    """Return one `<circle>` element centered at `(x, y)` with the given `radius`, fill and stroke."""
    return f"""<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke_color}" stroke-width="{stroke_width}"/>"""

def svg_text(text: str, x:int, y:int, style: Optional[str] = None, cls: Optional[str] = None, font_size:int = 50, comment: str="") -> Iterator[str]:
    """Yield the lines of a `<text>` element (opening tag, then `text` immediately followed by an optional raw
    XML `comment`, then the closing tag) centered on `(x, y)`. `style`/`cls` add an inline `style`/`class`
    attribute when given; `cls` must not contain `"`."""
    if cls is not None:
        assert '"' not in cls
    yield f"""<text x="{x}" y="{y}" font-size="{font_size}" {f'style="{style}" ' if style is not None else " "}text-anchor="middle"{f'class="{cls}" ' if cls is not None else  " "}alignment-baseline="middle">""" 
    yield f"""{text}{comment}"""
    yield """</text>"""