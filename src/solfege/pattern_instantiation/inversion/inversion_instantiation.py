
from dataclasses import dataclass
from typing import ClassVar, List, Tuple

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.chord.chord import Chord
from solfege.pattern_instantiation.inversion.abstract_inversion import AbstractInversionInstantiation
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.inversion.chromatic_inversion_instantiation import ChromaticInversionInstantiation
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.util import assert_typing


@dataclass(frozen=True)
class InversionInstantiation(
    AbstractInversionInstantiation[Note, Interval],
    AbstractPairInstantiation[InversionPattern, Tuple[int, int]]):
    """An `InversionPattern` anchored on a concrete (diatonic+chromatic) `Note` bass -- e.g. "C major triad,
    first inversion (E in the bass)"."""

    chromatic_instantiation_type: ClassVar = ChromaticInversionInstantiation
    """`get_chromatic_instantiation()` builds a `ChromaticInversionInstantiation` from this inversion."""

    def get_tonic(self) -> Note:
        """The tonic of the underlying chord (not this inversion's bass note), recovered from `lowest_note`
        via the pattern's `tonic_minus_lowest_note`."""
        return (self.lowest_note - self.pattern.tonic_minus_lowest_note)

    def _get_chord(self) -> Chord:
        """The root-position `Chord` this is an inversion of, anchored on its tonic (in the base octave)."""
        inversion = self.pattern
        return Chord.make(pattern=inversion.base, lowest_note =self.get_tonic().in_base_octave())

    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO) -> List[str]:
        """This inversion's names: the underlying chord's names as-is for root position (inversion 0), or
        each suffixed with "over <bass note>" (e.g. "C Major triad over E") for any other inversion."""
        inversion = self.pattern
        chord = self._get_chord()
        chord_names = chord.names()
        lowest_note_name = self.lowest_note.get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

        if inversion.inversion == 0:
            return chord_names
        else:
            return [f"{chord_name} over {lowest_note_name}" for chord_name in chord_names]

    def notation(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO) -> str:
        """This inversion's short notation: the underlying chord's notation as-is for root position
        (inversion 0), or "<chord notation>/<bass note>" (e.g. "CM/E") for any other inversion."""
        inversion = self.pattern
        chord = self._get_chord()
        chord_notation = chord.notation()
        lowest_note_name = self.lowest_note.get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

        if inversion.inversion == 0:
            return chord_notation
        else:
            return f"{chord_notation}/{lowest_note_name}"