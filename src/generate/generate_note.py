from typing import Iterable
from solfege.value.note import alteration
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from lily.lily import compile_
from utils import util
from consts import generate_root_folder

"""
Generate every note.
Scales 3 to 8 in treble.
Scales 0 to 4 in bass

"""

scale = [Note.from_name(f"{diatonic_letter}4{alteration_symbol}")
         for diatonic_letter in "ABCDEFG"
         for alteration_symbol in alteration.symbols
         ]
right_notes = [note.add_octave(o) for note in scale for o in range(-1, 5)]
left_notes = [note.add_octave(o) for note in scale for o in range(-4,1)]

def single_note(clef: Clef, note: Note):
    return f"""
\\version "2.20.0"
\\score{{
  \\new Staff{{
    \\override Staff.TimeSignature.stencil = ##f
    \\omit Staff.BarLine
    \\omit PianoStaff.SpanBar
    \\time 30/4
    \\set Staff.printKeyCancellation = ##f
    \\clef {clef}
    {note.lily_in_scale()}
    }}
}}"""


folder_path = f"{generate_root_folder}/note"
util.ensure_folder(folder_path)

def generate(clef, notes: Iterable[Note]):
    for note in notes:
        lily_code = single_note(clef, note)
        filename = note.file_name(clef)
        path = f"{folder_path}/{filename}"
        compile_(lily_code, path, execute_lily=True, wav=False)

generate(Clef.TREBLE, right_notes)
generate(Clef.BASS, left_notes)

