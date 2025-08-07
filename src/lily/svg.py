import os
import re
import unittest


def rect(svg, color):
    match = re.search(r"""viewBox="(?P<x>[^ ]*) (?P<y>[^ ]*) (?P<width>[^ ]*) (?P<height>[^"]*)">""", svg)
    x = match.group("x")
    y = match.group("y")
    width = match.group("width")
    height = match.group("height")
    return f"""<rect x="{x}" width="{width}" y="{y}" height="{height}" fill="{color}"/>"""


def display_svg_file(path: str):
    os.system(f"eog {path}&")


def add_background(svg: str, background_color: str):
    prefix, content = svg.split("""
</style>
""")
    return f"""{prefix}
</style>
{rect(svg, background_color)}
{content}"""


def clean_svg(input: str, output: str, background_color: str):
    """Remove xlink and add a white background"""
    with open(input) as f:
        svg = f.read()
    svg = add_background(svg, background_color)
    svg = remove_xlink(svg)
    with open(output, "w") as f:
        f.write(svg)


def remove_xlink(input: str):
    return re.sub(r' xlink:href="[^"]*"', "", input)
