
from dataclasses import dataclass
from typing import Dict, List
from lily.sheet.lily_sheet import LilySheet
from lily.sheet.lily_sheet_single_staff import LilySheetSingleStaff
from lily.staff.lily_chord_staff import LilyChordStaff
from lily.staff.lily_scale_staff import LilyScaleStaff
from solfege.value.note.note import Note, NoteFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput


@dataclass(frozen=True)
class LilyScaleSheet(LilySheetSingleStaff):
    """A `LilySheetSingleStaff` whose staff is a `LilyScaleStaff` (a melodic sequence of notes, e.g. a scale or
    arpeggio)."""
    staff: LilyScaleStaff
    """The scale staff to render."""

    #pragma mark - LilySheet

    def file_prefix(self) -> str:
        """A file name built from `"scale_"` followed by each note's name (ASCII, fixed-width), underscore
        joined."""
        def name(note: Note):
            """The note's ASCII, fixed-width name (e.g. `C____________4`), used as a filesystem-safe token."""
            return note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.ASCII, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.UNDERSCORE_DOUBLE)
        return f"""scale_{"_".join(name(note) for note in self.staff.notes)}"""


    # # Pragma mark - DataClassWithDefaultArgument
    # @classmethod
    # def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
    #     args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "notes", NoteFrozenList)
    #     kwargs["staff"] = LilyChordStaff(kwargs["notes"])
    #     args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
    #     return args, kwargs