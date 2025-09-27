
from dataclasses import dataclass
from typing import ClassVar, Type

from instruments.fretted_instrument.chord.abstract_equivalent_inversion_and_its_fretted_instrument_chords import AbstractIdenticalInversionAndItsFrettedInstrumentChords
from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from _lily import lily
from lily.sheet.lily_chord_sheet import lily_chord_sheet
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.inversion.inversion_instantiation import InversionInstantiation
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note
from solfege.value.note.set.note_list import NoteList
from utils.util import assert_typing, ensure_folder, img_tag



@dataclass(frozen=True, unsafe_hash=True, order=False)
class ChromaticInversionInstantiationAndItsOpenChords(AbstractIdenticalInversionAndItsFrettedInstrumentChords[InversionInstantiation]):
    """
    Contains a chromatic inversion and all chords that produce it.
    """
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords
    absolute: ClassVar[bool] = True
    key: InversionInstantiation
    identical_inversion_pattern_getter_type: ClassVar = InversionInstantiation

    def names(self):
        inversion = self.get_inversion_pattern()
        chromatic_lowest_note: ChromaticNote = self.key.lowest_note
        lowest_note = inversion.get_interval_list().best_enharmonic_starting_note(chromatic_lowest_note)
        tonic = inversion.get_tonic(lowest_note)
        note_name = tonic.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        lowest_note_name = chromatic_lowest_note.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        chord_pattern_notation = inversion.base.notation
        if chord_pattern_notation is None:
            chord_pattern_notation = inversion.base.first_of_the_names()
        chord_notation = f"{note_name}{chord_pattern_notation}"
        if inversion.inversion == 0:
            assert tonic.get_chromatic() == chromatic_lowest_note
            return [chord_notation]
        else:
            return [f"""{chord_notation}/{lowest_note_name}"""]