import os
import unittest
from typing import Callable

from lily.svg import clean_svg, display_svg_file
from utils.util import indent

lilyHeader = """"""
lowLimit = {"left": -14, "right": -3}
highLimit = {"left": 3, "right": 14}
lilyProgram = "lilypond"


def chord(notes) -> str:  # only used by guitar right now
    return f"""\\version "2.20.0"
\\score{{
  \\new Staff{{
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef treble <
{indent("".join(note.lily() for note in notes), 6)}
    >
  }}
}}"""


def command(file_prefix: str, extension: str = "svg") -> Callable[[], object]:
    if extension == "svg":
        return lambda: display_svg_file(f"{file_prefix}.svg")
    else:
        assert extension == "pdf"
        command = f"evince {file_prefix}.pdf&"
        return lambda: os.system(command)


def compile_(code: str, file_prefix, wav: bool, extension="svg", execute_lily: bool = True, force_recompile: bool = False) -> \
        Callable[[], object]:
    """Write `code` in `filename`. If `execute_lily`, compile it in a file with the given extension

    return the command to see the generated file.
    `execute_lily` should be False only for tests, to save time.
    wav: whether to convert midi to wav. Assumes the lilypond file will generate midi."""
    if os.path.isfile(file_prefix + ".ly"):
        if os.path.exists(f"{file_prefix}.svg"):
            with open(file_prefix + ".ly", "r") as file:
                old_code = file.read()
                if old_code == code:
                    print("""%s.ly's old code is equal to current one""" % file_prefix)
                    execute_lily = False
    if force_recompile:
        execute_lily = True
    if not execute_lily:
        return command(file_prefix, extension)
    with open(file_prefix + ".ly", "w") as file:
        file.write(code)
    preview_path = f"{file_prefix}.preview.{extension}"
    if extension == "svg":
        cmd = f"""{lilyProgram} -dpreview -dbackend=svg -o "{file_prefix}"  "{file_prefix}.ly" """
        os.system(cmd)
        clean_svg(preview_path, preview_path, "white")
    else:
        assert extension == "pdf"
        cmd = f"""lilypond  -o "{file_prefix}" "{file_prefix}.ly" """
        os.system(cmd)
    os.system(f"""mv -f "{preview_path}" "{file_prefix}.{extension}" """)
    if wav:
        os.system(f"""timidity "{file_prefix}.midi" --output-mode=w -o "{file_prefix}.wav" """)
    return command(file_prefix, extension)
    # os.system("""convert -background "#FFFFFF" -flatten "%s.svg" "%s.png" """%(folder_fileName,folder_fileName))

