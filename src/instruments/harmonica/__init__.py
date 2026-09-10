"""Generates the harmonica diagram SVGs under `<generate_root_folder>/harmonica/images/` (one per
hole/direction combination): for each of the 10 holes and each of blow/draw, draws the 10-hole harmonica
outline with that hole highlighted and an arrow showing air direction. Running this module (e.g. via
`python3 -m instruments.harmonica`, see `__main__.py`) regenerates all 20 files. Smaller/less developed than
the other instrument packages: it has no solfege/note-to-fingering model — the images are static per
hole/direction, not per note."""
from typing import TextIO

from consts import generate_root_folder
from utils.util import *

harmonica_images_folder = f"{generate_root_folder}/harmonica/images"
"""Output folder for the generated harmonica diagram SVGs, per the shared `<generate_root_folder>/<instrument>` convention."""

square = 30
"""Size (in SVG user units) of one grid cell; every coordinate in `drawHarmonica` is expressed as a multiple
of this to keep the whole diagram proportional."""


def drawHarmonica(f: TextIO, pos: int, draw: bool) -> None:
    """Write one complete harmonica SVG to file object `f`: the 10-hole outline with each hole numbered, hole
    `pos` (1-10) highlighted in red, and a red arrow through it pointing up if `draw` else down (draw vs. blow)."""
    f.write(
        """<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">""" % (square * 11, square * 3))
    # vertical
    for i in range(0, 11):
        f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="%s" />""" % (
        square * (i + 0.5), square * .5, square * (i + 0.5), square * (1.5), "black"))
    # numbers
    for i in range(1, 11):
        f.write("""<text x="%d" y="%d" fill="%s" font-size="30">%d</text>""" % (
        square * (i - .5), square * (1.3), "black" if i != pos else "red", i))
    # horizontal
    for i in range(1, 3):
        f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="black" />""" % (
        square * .5, square * (i - 0.5), square * 10.5, square * (i - .5)))
    f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2" stroke="red" />""" % (
    square * pos, square * 1.5, square * pos, square * 2.5))
    end_of_arrow = square * 2.5 if draw else square * 1.5
    f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2" stroke="red" />""" % (
    square * (pos + .25), square * 1.75, square * pos, end_of_arrow))
    f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2" stroke="red" />""" % (
    square * (pos - .25), square * 1.75, square * pos, end_of_arrow))

    f.write("</svg>")


for draw in [True, False]:
    for pos in range(1, 11):
        ensure_folder(harmonica_images_folder)
        with open("%s/%s%d.svg" % (harmonica_images_folder, "draw" if draw else "blow", pos), "w") as f:
            drawHarmonica(f, pos, draw)
