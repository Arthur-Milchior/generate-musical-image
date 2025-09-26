from dataclasses import dataclass
from typing import Dict, List
from lily.staff.lily_chord_staff import LilyChordStaff
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval import Interval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.clef import Clef
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note


@dataclass(frozen=True)
class LilySingleNoteStaff(LilyChordStaff):
    note: Note

    # Pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "note", Note.make_single_argument)
        kwargs["notes"] = [kwargs["note"]]
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        return args, kwargs
    
    def get_8_va(self):
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

    def get_8_vb(self):
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
    
    