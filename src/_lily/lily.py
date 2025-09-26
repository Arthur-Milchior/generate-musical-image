import os
from typing import Callable, List
from sh import assertNotUnitTest, shell

from lily.lily_svg_utils import clean_svg, display_svg_file
from solfege.value.note.note import Note
from utils.util import indent, save_file

lilyHeader = """"""
lowLimit = {"left": -14, "right": -3}
highLimit = {"left": 3, "right": 14}
lilyProgram = "lilypond"

"""
Lily order is:
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef treble
"""

