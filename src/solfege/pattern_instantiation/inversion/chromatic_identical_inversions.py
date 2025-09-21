
from dataclasses import dataclass
from typing import Generic, List, Tuple
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatterns, MinimalChordDecompositionInput
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.inversion.abstract_Identical_inversions import AbstractIdenticalInversion
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.interval import Interval
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from utils.util import T


@dataclass(frozen=True, eq=True)
class ChromaticIdenticalInversions(AbstractIdenticalInversion[Note, Interval], AbstractChromaticInstantiation[ChromaticIdenticalInversionPatterns, Tuple[int, int]], MinimalChordDecompositionInput):

    def get_tonic(self) -> ChromaticNote:
        return self._get_identical_inversion().get_tonic().get_chromatic()

    def _get_identical_inversion(self):
        """The identiacl_inversion with a note with this chromatic."""
        from solfege.pattern_instantiation.inversion.identical_inversions_instantiation import IdenticalInversion
        note = Note.from_chromatic(self.lowest_note)
        return IdenticalInversion.make(self.pattern, note)
    
    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        return self._get_identical_inversion().names(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

    #pragma mark - MinimalChordDecompositionInput

    def notations(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        return self._get_identical_inversion().notations(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)
        
    def get_tonic_minus_lowest_note(self) -> ChromaticInterval:
        return self.pattern.inversion_patterns[0].tonic_minus_lowest_note.get_chromatic()
    
    def get_inversion_patterns(self) -> List[InversionPattern]:
        return self.pattern.inversion_patterns

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> Tuple[int, int]:
        return self.pattern.easy_key()