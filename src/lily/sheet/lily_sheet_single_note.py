from typing import Optional
from lily.sheet.lily_chord_sheet import LilyChordSheet
from lily.staff.lily_single_note_staff import LilySingleNoteStaff
from solfege.value.key.key import Key
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from solfege.value.key.keys import key_of_C
from utils.util import assert_typing


def sheet_single_note(note: Note, clef: Clef, key: Optional[Key] = None):
    assert_typing(note, Note)
    assert_typing(clef, Clef)
    if key is None:
        key = key_of_C
    return LilyChordSheet.make(staff=LilySingleNoteStaff.make(note=note, clef=clef, first_key=key))