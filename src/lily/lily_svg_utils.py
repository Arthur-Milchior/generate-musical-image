import os
import re
from sh import shell
from utils.util import save_file


def rect(svg: str, color: str) -> str:
    """Build a `<rect>` SVG element, filled with `color`, sized/positioned to exactly cover `svg`'s `viewBox`."""
    match = re.search(r"""viewBox="(?P<x>[^ ]*) (?P<y>[^ ]*) (?P<width>[^ ]*) (?P<height>[^"]*)">""", svg)
    x = match.group("x")
    y = match.group("y")
    width = match.group("width")
    height = match.group("height")
    return f"""<rect x="{x}" width="{width}" y="{y}" height="{height}" fill="{color}"/>"""


def display_svg_file(path: str) -> None:
    """Open `path` in VS Code (`code`), in the background, for quick visual inspection during development."""
    shell(f"""code "{path}"&""")


def add_background(svg: str, background_color: str) -> str:
    """Return `svg` with a `background_color`-filled `rect` (see `rect`) inserted right after its `</style>` tag, so it's drawn behind everything else."""
    prefix, content = svg.split("""
</style>
""")
    return f"""{prefix}
</style>
{rect(svg, background_color)}
{content}"""


def clean_svg(svg_input_path: str, svg_output_path: str, background_color: str) -> None:
    """Remove xlink and add a white background"""
    with open(svg_input_path) as f:
        svg = f.read()
    svg = add_background(svg, background_color)
    svg = remove_xlink(svg)
    save_file(svg_output_path, svg)


def remove_xlink(input: str) -> str:
    """Strip every `xlink:href="..."` attribute from `input` (an SVG document), removing LilyPond's font-glyph references."""
    return re.sub(r' xlink:href="[^"]*"', "", input)
