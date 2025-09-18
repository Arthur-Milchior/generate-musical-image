
from dataclasses import dataclass
from typing import ClassVar, List, Tuple

from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.pattern_instantiation.inversion.abstract_Identical_inversions import AbstractIdenticalInversion
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.inversion.chromatic_identical_inversions import ChromaticIdenticalInversions
from solfege.pattern_instantiation.inversion.inversion import Inversion
from solfege.value.interval.interval import Interval
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.note import Note
from utils.util import assert_typing


class IdenticalInversion(AbstractIdenticalInversion[Note, Interval], AbstractPairInstantiation[IdenticalInversionPatterns, Tuple[int, int]]):
    
    chromatic_instantiation_type: ClassVar = ChromaticIdenticalInversions

    def get_tonic(self):
        return self.inversions()[0].get_tonic()

    def inversions(self):
        identical_inversion_patterns = self.pattern
        inversions: List[Inversion] = []
        for inversion_pattern in identical_inversion_patterns.inversion_patterns:
            inversions.append(Inversion.make(inversion_pattern, self.lowest_note))
        return inversions

    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        names = []
        for inversion in self.inversions():
            names += inversion.names(alteration_output, note_output, fixed_length)
        return names

    def notations(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        notations = []
        for inversion in self.inversions():
            notations.append(inversion.notation(alteration_output, note_output, fixed_length))
        return notations
    
        
