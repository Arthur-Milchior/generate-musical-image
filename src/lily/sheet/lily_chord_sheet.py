
from dataclasses import dataclass
from typing import Dict, List
from lily.sheet.lily_sheet import LilySheet
from lily.sheet.lily_sheet_single_staff import LilySheetSingleStaff
from lily.staff.lily_chord_staff import LilyChordStaff
from solfege.value.note.note import Note, NoteFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput


@dataclass(frozen=True)
class LilyChordSheet(LilySheetSingleStaff):
    staff: LilyChordStaff

    #pragma mark - LilySheet

    def file_prefix(self) -> str:
        va = self.staff.get_ottava()
        if va is 0:
            va_part = ""
        else:
            va_part = f"_ottava_{va}"
        def name(note: Note):
            return note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.ASCII, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.UNDERSCORE_DOUBLE)
        return f"""{str(self.staff.clef)}_chord_{"_".join(name(note) for note in self.staff.notes)}{va_part}"""


    # # Pragma mark - DataClassWithDefaultArgument
    # @classmethod
    # def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
    #     args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notes", NoteFrozenList)
    #     kwargs["staff"] = LilyChordStaff(kwargs["notes"])
    #     args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
    #     return args, kwargs