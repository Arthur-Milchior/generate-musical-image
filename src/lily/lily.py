import os
from typing import Callable, List
from sh import assertNotUnitTest, shell

from lily.svg import clean_svg, display_svg_file
from solfege.value.note.note import Note
from utils.util import indent

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


def chord(notes: List[Note]) -> str:  # only used by guitar right now
    return f"""\\version "2.20.0"
\\score{{
  \\new Staff{{
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef treble <
{indent("".join(note.lily_in_scale() for note in notes), 6)}
    >
  }}
}}"""


def show_file(file_prefix: str, extension: str = "svg") -> Callable[[], object]:
    """Returns a function which shows the content of {file_prefix}.{extension}"""
    if extension == "svg":
        return lambda: display_svg_file(f"{file_prefix}.svg")
    else:
        assert extension == "pdf"
        command = f"evince {file_prefix}.pdf&"
        return lambda: shell(command)


def compile_(code: str, file_prefix: str, wav: bool, extension="svg", execute_lily: bool = True, force_recompile: bool = False) -> \
        Callable[[], object]:
    """Write `code` in `filename`. If `execute_lily`, compile it in a file with the given extension

    return a function that shows the generated file.
    `execute_lily` should be False only for tests, to save time.
    `file_prefix`: path, except for the .svg/.pdf
    wav: whether to convert midi to wav. Assumes the lilypond file will generate midi."""
    if os.path.isfile(file_prefix + ".ly"):
        if os.path.exists(f"{file_prefix}.svg"):
            with open(file_prefix + ".ly", "r") as file:
                old_code = file.read()
                if old_code == code:
#                    print("""%s.ly's old code is equal to current one""" % file_prefix)
                    execute_lily = False
    if force_recompile:
        execute_lily = True
    if execute_lily:
        with open(file_prefix + ".ly", "w") as file:
            file.write(code)
        preview_path = f"{file_prefix}.preview.{extension}"
        if extension == "svg":
            cmd = f"""{lilyProgram} -dpreview -dbackend=svg -o "{file_prefix}"  "{file_prefix}.ly" """
            shell(cmd)
            clean_svg(preview_path, preview_path, "white")
        else:
            assert extension == "pdf"
            cmd = f"""lilypond  -o "{file_prefix}" "{file_prefix}.ly" """
            shell(cmd)
        shell(f"""mv -f "{preview_path}" "{file_prefix}.{extension}" """)
    if wav:
        shell(f"""timidity "{file_prefix}.midi" --output-mode=w -o "{file_prefix}.wav" """)
    return show_file(file_prefix, extension)
    # shell("""convert -background "#FFFFFF" -flatten "%s.svg" "%s.png" """%(folder_fileName,folder_fileName))

