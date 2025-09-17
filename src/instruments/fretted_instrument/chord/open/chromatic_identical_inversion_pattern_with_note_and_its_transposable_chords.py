
from dataclasses import dataclass
from typing import ClassVar, Type

from instruments.fretted_instrument.chord.abstract_equivalent_inversion_and_its_fretted_instrument_chords import AbstractIdenticalInversionAndItsFrettedInstrumentChords
from instruments.fretted_instrument.chord.chord_decomposition_anki_note import ChordDecompositionAnkiNote
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from lily import lily
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatternGetter
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.inversion.abstract_Identical_inversions import AbstractIdenticalInversionType
from solfege.pattern_instantiation.inversion.chromatic_identical_inversions import ChromaticIdenticalInversions
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from solfege.value.note.set.note_list import NoteList
from utils.util import assert_typing, ensure_folder, img_tag



@dataclass(frozen=True, unsafe_hash=True)
class AbstractIdenticalInversionInstantiationAndItsFrettedInstrumentChords(AbstractIdenticalInversionAndItsFrettedInstrumentChords[AbstractIdenticalInversionType]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords
    absolute: ClassVar[bool] = True
    key: AbstractIdenticalInversionType

    def names_from_inversion(self, inversion: InversionPattern):
        lowest_note: ChromaticNote = self.key.lowest_note
        delta_due_to_inversion = inversion.tonic_minus_lowest_note.chromatic
        tonic: ChromaticNote = lowest_note - delta_due_to_inversion
        note_name = tonic.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        lowest_note_name = lowest_note.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        chord_pattern_notation = inversion.base.notation
        if chord_pattern_notation is None:
            chord_pattern_notation = inversion.base.first_of_the_names()
        chord_notation = f"{note_name}{chord_pattern_notation}"
        if inversion.inversion == 0:
            assert tonic == lowest_note
            return [chord_notation]
        else:
            return [f"""{chord_notation}/{lowest_note_name}"""]

    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalListPattern) -> str:
        lowest_chromatic_note: ChromaticNote = self.key.lowest_note
        lowest_note: Note = Note.from_chromatic(lowest_chromatic_note)
        note_list: NoteList = interval_list.from_note(lowest_note)
        file_prefix = note_list.lily_file_name()
        lily_folder_path = f"""{self.instrument.generated_folder_name()}/open"""
        ensure_folder(lily_folder_path)
        path_prefix = f"{lily_folder_path}/{file_prefix}"
        code = note_list.lily_file_with_only_chord()
        lily.compile_(code, path_prefix, wav=False)
        return img_tag(f"{file_prefix}.svg")

@dataclass(frozen=True, unsafe_hash=True, order=False)
class ChromaticIdenticalInversionAndItsOpenChords(AbstractIdenticalInversionInstantiationAndItsFrettedInstrumentChords[ChromaticIdenticalInversions]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords

    identical_inversion_pattern_getter_type: ClassVar[Type[ChromaticIdenticalInversionPatternGetter]] = ChromaticIdenticalInversions