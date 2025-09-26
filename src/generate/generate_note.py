from typing import Iterable
from lily.sheet.lily_sheet_single_note import sheet_single_note
from solfege.value.note import note_alteration
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from _lily.lily import compile_
from utils import util
from consts import generate_root_folder

"""
Generate every note.
Scales 3 to 8 in treble.
Scales 0 to 4 in bass

"""

scale = [
    Note.from_name(f"{diatonic_letter}4{alteration_symbol}")
    for diatonic_letter in "ABCDEFG"
    for alteration_symbol in note_alteration.symbols
]
treble_notes = [note.add_octave(o) for note in scale for o in range(-2, 5)]
bass_notes = [note.add_octave(o) for note in scale for o in range(-4, 2)]



folder_path = f"{generate_root_folder}/lily"
util.ensure_folder(folder_path)


def generate(clef:Clef, notes: Iterable[Note]):
    for note in notes:
        sheet = sheet_single_note(note, clef)
        sheet.maybe_generate()


generate(Clef.TREBLE, treble_notes)
generate(Clef.BASS, bass_notes)
