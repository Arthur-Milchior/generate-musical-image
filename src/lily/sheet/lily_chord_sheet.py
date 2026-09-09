from dataclasses import dataclass
from typing import Dict, List
from lily.sheet.lily_sheet import LilySheet
from lily.sheet.lily_sheet_single_staff import LilySheetSingleStaff
from lily.staff.lily_chord_staff import LilyChordStaff
from solfege.value.key.key import Key
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note, NoteFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.value.key.keys import key_of_C


@dataclass(frozen=True)
class LilyChordSheet(LilySheetSingleStaff):
    """A `LilySheetSingleStaff` whose staff is a `LilyChordStaff` (a chord, possibly a singleton "chord" of one
    note as used for single-note diagrams)."""
    staff: LilyChordStaff
    """The chord staff to render."""

    #pragma mark - LilySheet

    def file_prefix(self) -> str:
        """A file name built from the clef, each note's name (ASCII, fixed-width), and an `_ottava_N` suffix if
        the chord needed an octave shift."""
        va = self.staff.get_ottava()
        if va is 0:
            va_part = ""
        else:
            va_part = f"_ottava_{va}"
        def name(note: Note):
            """The note's ASCII, fixed-width name (e.g. `C____________4`), used as a filesystem-safe token."""
            return note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.ASCII, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.UNDERSCORE_DOUBLE)
        return f"""{str(self.staff.clef)}_chord_{"_".join(name(note) for note in self.staff.notes)}{va_part}"""


    # # Pragma mark - DataClassWithDefaultArgument
    # @classmethod
    # def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
    #     args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notes", NoteFrozenList)
    #     kwargs["staff"] = LilyChordStaff(kwargs["notes"])
    #     args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
    #     return args, kwargs

def lily_chord_sheet(notes: List, clef: Clef, key: Key=key_of_C) ->LilyChordSheet:
    """Build a `LilyChordSheet` from a plain list of `notes`, a `clef`, and a `key` (defaulting to C major)."""
    staff = LilyChordStaff.make(notes= notes, clef=clef, first_key = key)
    return LilyChordSheet.make(staff=staff)