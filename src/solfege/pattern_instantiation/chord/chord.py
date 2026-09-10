
from dataclasses import dataclass
from typing import ClassVar, Generic, List, TypeVar

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern_instantiation.chord.abstract_chord import AbstractChord
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.chord.chromatic_chord import ChromaticChord
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import  AlterationOutput, FixedLengthOutput, NoteOutput, NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.util import assert_typing


class Chord(AbstractChord[Note, Interval], AbstractPairInstantiation[ChordPattern, int]):
    """A `ChordPattern` anchored on a concrete (diatonic+chromatic) `Note` root -- e.g. "C major triad"."""

    chromatic_instantiation_type: ClassVar = ChromaticChord
    """`get_chromatic_instantiation()` builds a `ChromaticChord` from this chord."""

    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO) -> List[str]:
        """This chord's full names: `lowest_note`'s spelled name followed by each of `pattern.names`, e.g.
        ["C Major triad"]. `alteration_output`/`note_output`/`fixed_length` control how the note is spelled."""
        names = []
        for name in self.pattern.names:
            note_name = self.lowest_note.get_name_up_to_octave(
                alteration_output=alteration_output,
                note_output=note_output, 
                fixed_length=fixed_length)
            names.append(f"{note_name} {name}")
        return names

    def notation(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO) -> str:
        """This chord's short notation: `lowest_note`'s spelled name followed by `pattern.notation`, e.g. "CM"."""
        note_notation = self.lowest_note.get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)
        return f"{note_notation}{self.pattern.notation}"
    
