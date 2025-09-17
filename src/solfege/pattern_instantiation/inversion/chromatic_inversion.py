
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.inversion.abstract_inversion import AbstractInversion
from solfege.value.interval.interval import Interval
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.note import Note


class ChromaticInversionPattern(AbstractInversion[Note, Interval], AbstractChromaticInstantiation[InversionPattern]):
    def _get_inversion(self):
        """The chord with a note with this chromatic."""
        from solfege.pattern_instantiation.inversion.inversion import Inversion
        note = Note.from_chromatic(self.lowest_note)
        return Inversion.make(self.pattern, note)
    
    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        return self._get_inversion().names(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)
    
    def notation(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        return self._get_inversion().notation(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)