from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.chord.abstract_chord import AbstractChord
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.chromatic_interval import ChromaticIntervalFrozenList
from solfege.value.interval.interval import Interval
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, NoteType
from solfege.value.note.chromatic_note import ChromaticNoteFrozenList
from solfege.value.note.note import Note


class ChromaticChord(AbstractChord[Note, Interval], AbstractChromaticInstantiation[ChordPattern]):

    def _get_chord(self):
        """The chord with a note with this chromatic."""
        from solfege.pattern_instantiation.chord.abstract_chord import Chord
        note = Note.from_chromatic(self.lowest_note)
        return Chord.make(self.pattern, note)

    def names(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        return self._get_chord().names(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)
    
    def notation(self, alteration_output: AlterationOutput=AlterationOutput.SYMBOL, note_output: NoteOutput=NoteOutput.LETTER, fixed_length: FixedLengthOutput=FixedLengthOutput.NO):
        return self._get_chord().notation(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)
    

