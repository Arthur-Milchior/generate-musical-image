from dataclasses import dataclass
from typing import Dict, List, Tuple
from lily.staff.lily_chord_staff import LilyChordStaff
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval import Interval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.clef import Clef
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note


@dataclass(frozen=True)
class LilySingleNoteStaff(LilyChordStaff):
    """A `LilyChordStaff` specialized to a single note, computing the correct `\\ottava` shift for notes that fall
    above/below the staff's normal ambitus for the current clef."""
    note: Note
    """The single note to render. Kept alongside (and always kept in sync with) the inherited `notes` list, which
    `_clean_arguments_for_constructor` sets to `[note]`."""

    # Pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Coerce `note` via `Note.make_single_argument`, then force `notes` to the singleton list `[note]` so the
        inherited `LilyChordStaff` rendering has exactly one note to draw."""
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "note", Note.make_single_argument)
        kwargs["notes"] = [kwargs["note"]]
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        return args, kwargs

    def get_8_va(self) -> int:
        """Number of octaves of `\\ottava` shift needed above the staff: 0 if `note` is within the normal ambitus
        for the clef (up to F6 for treble, F4 for bass), else how many octaves above that threshold it sits
        (rounded up)."""
        F4 =DiatonicNote.make(3)
        F6 = F4.add_octave(2)
        if self.clef is Clef.BASS:
            first_note_in_ottavia = F4
        else:
            assert self.clef is Clef.TREBLE
            first_note_in_ottavia = F6
        if self.note.get_diatonic() < first_note_in_ottavia:
            return 0
        return (self.note.get_diatonic() - first_note_in_ottavia).octave()+1

    def get_8_vb(self) -> int:
        """Number of octaves of `\\ottava` shift needed below the staff: 0 if `note` is within the normal ambitus
        for the clef (down to E3 for treble, C2 for bass), else how many octaves below that threshold it sits
        (rounded up)."""
        E4 =DiatonicNote.make(2)
        E3 = E4.add_octave(-1)
        C4 = DiatonicNote.make(0)
        C2 = C4.add_octave(-2)
        if self.clef is Clef.BASS:
            last_note_without_ottavia = C2
        else:
            assert self.clef is Clef.TREBLE
            last_note_without_ottavia = E3
        if self.note.get_diatonic() >= last_note_without_ottavia:
            return 0
        return -(self.note.get_diatonic() - last_note_without_ottavia ).octave()
    
    