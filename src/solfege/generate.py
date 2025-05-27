from .note import Note
from lily.lily import compile_
from utils import util

scale = [Note(diatonic =d, alteration = a)
         for d in range(7)
         for a in range(-2,3)
         ]
right_notes = [note.add_octave(o) for note in scale for o in range(5)]
left_notes = [note.add_octave(o) for note in scale for o in range(-4,0)]

def single_note(clef, note):
    return f"""
\\version "2.20.0"
\\score{{
  \\new Staff{{
    \\clef {clef}
    \\override Staff.TimeSignature.stencil = ##f
    {note.lily_in_scale()}
    }}
}}"""


folder_path = "../../generated/note"
util.ensure_folder(folder_path)

def generate(clef, notes):
    for note in notes:
        lily_code = single_note(clef, note)
        filename = f"_{note.get_ascii_name(fixed_length=False)}"
        path = f"{folder_path}/{filename}"
        compile_(lily_code, path, execute_lily=True, wav=False)

generate("treble", right_notes)
generate("bass", left_notes)
