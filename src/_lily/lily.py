"""Shared LilyPond layout constants, plus a few re-exported helpers (`indent`/`save_file`,
`clean_svg`/`display_svg_file`). Used to also define `compile_`/`chord`, the functions that actually wrote
`.ly` source and shelled out to `lilypond` — see `_lily/README.md` for where those went and which callers
still expect them here."""
import os
from typing import Callable, List
from sh import assertNotUnitTest, shell

from lily.lily_svg_utils import clean_svg, display_svg_file
from solfege.value.note.note import Note
from utils.util import indent, save_file

lilyHeader = """"""
"""Unused leftover: an empty string, from when this held boilerplate `.ly` header text."""
lowLimit = {"left": -14, "right": -3}
"""Lowest playable chromatic offset from middle C for each hand, keyed by `"left"`/`"right"`."""
highLimit = {"left": 3, "right": 14}
"""Highest playable chromatic offset from middle C for each hand, keyed by `"left"`/`"right"`."""
lilyProgram = "lilypond"
"""Name of the `lilypond` binary invoked (via `shell()`) to compile `.ly` source to SVG/PDF/etc."""

"""
Lily order is:
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef treble
"""

