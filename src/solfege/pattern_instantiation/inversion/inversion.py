
from dataclasses import dataclass
from typing import ClassVar

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.chord.chord import Chord
from solfege.pattern_instantiation.inversion.abstract_inversion import AbstractInversion
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.inversion.chromatic_inversion import ChromaticInversionPattern
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.util import assert_typing


@dataclass(frozen=True)
class Inversion(
    AbstractInversion[Note, Interval],
    AbstractPairInstantiation[InversionPattern]):
    
    chromatic_instantiation_type: ClassVar = ChromaticInversionPattern

    def get_tonic(self) -> Note:
        return (self.lowest_note - self.pattern.tonic_minus_lowest_note).in_base_octave()

    def _get_chord(self):
        inversion = self.pattern
        return Chord.make(pattern=inversion.base, lowest_note =self.get_tonic())

    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        inversion = self.pattern
        chord = self._get_chord()
        chord_names = chord.names()
        lowest_note_name = self.lowest_note.get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

        if inversion.inversion == 0:
            return chord_names
        else:
            return [f"{chord_name} over {lowest_note_name}" for chord_name in chord_names]
        
    def notation(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        inversion = self.pattern
        chord = self._get_chord()
        chord_notation = chord.notation()
        lowest_note_name = self.lowest_note.get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

        if inversion.inversion == 0:
            return chord_notation
        else:
            return f"{chord_notation}/{lowest_note_name}"