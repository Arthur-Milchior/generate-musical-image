
# from dataclasses import dataclass
# from typing import ClassVar, Optional
# from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
# from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
# from lily import lily
# from solfege.pattern.inversion_pattern import InversionPattern
# from solfege.value.interval.chromatic_interval import ChromaticInterval
# from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
# from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
# from solfege.value.note.chromatic_note import ChromaticNote
# from solfege.value.note.set.note_list import NoteList
# from utils.util import assert_typing, ensure_folder, img_tag

# @dataclass(frozen=True, unsafe_hash=True)
# class InversionAndTonicAndItsFrettedInstrumentChords(ChromaticListAndItsFrettedInstrumentChords):
#     """Up to octave.
    
#     """
#     lowest_note: ChromaticNote
#     open: ClassVar[bool] = True
#     absolute: ClassVar[bool] = True

#     def __post_init__(self):
#         assert_typing(self.lowest_note, ChromaticNote)
#         super().__post_init__()

#     def name(self, inversion: InversionPattern):
#         tonic: ChromaticNote = self.lowest_note - inversion.position_of_lowest_interval_in_base_octave.chromatic
#         note_name = tonic.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
#         lowest_note_name = self.lowest_note.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
#         chord_pattern_notation = inversion.base.notation
#         if chord_pattern_notation is None:
#             chord_pattern_notation = f" inversion.base.first_of_the_names()"
#         chord_notation = f"{note_name}{chord_pattern_notation}"
#         if inversion.inversion == 0:
#             assert tonic == self.lowest_note
#             return chord_notation
#         else:
#             return f"""{chord_notation}/{lowest_note_name}"""
    
#     def notes(self, inversion: InversionPattern):
#         notes_in_base_octave: NoteList = inversion.interval_list.from_note(self.lowest_note)
#         return notes_in_base_octave.change_octave_to_be_enharmonic()

#     def append(self, fretted_instrument_chord: ChordOnFrettedInstrument):
#         super().append(fretted_instrument_chord)
#         fretted_instrument_chord_lowest_note = fretted_instrument_chord.get_most_grave_note()
#         assert fretted_instrument_chord_lowest_note.get_chromatic().in_base_octave() == self.lowest_note.in_base_octave(), f"""{fretted_instrument_chord_lowest_note} is not a octave away from {self.lowest_note}"""

#     def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalListPattern) -> str:
#         note_list = fretted_instrument_chord.notes_from_interval_list(interval_list=interval_list)
#         file_prefix = note_list.lily_file_name()
#         lily_folder_path = f"""{self.instrument.generated_folder_name()}/open"""
#         ensure_folder(lily_folder_path)
#         path_prefix = f"{lily_folder_path}/{file_prefix}"
#         code = note_list.lily_file_with_only_chord()
#         lily.compile_(code, path_prefix, wav=False)
#         return img_tag(f"{file_prefix}.svg")
