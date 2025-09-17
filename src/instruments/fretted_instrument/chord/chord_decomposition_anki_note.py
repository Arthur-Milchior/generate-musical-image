from dataclasses import dataclass, field
from tkinter.font import names
from typing import Generator, List

from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordColors, ChordOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import ScaleColors
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import MinimalChordDecompositionInput
from solfege.pattern_instantiation.inversion.inversion import Inversion
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from lily import lily
from solfege.value.note.note import Note
from solfege.value.note.set.note_list import NoteList
from utils.csv import CsvGenerator
from utils.easyness import ClassWithEasyness
from utils.frozenlist import StrFrozenList
from utils.util import assert_iterable_typing, assert_typing, ensure_folder, img_tag

@dataclass(frozen=True)
class ChordDecompositionAnkiNote(ClassWithEasyness, CsvGenerator):
    instrument: FrettedInstrument
    identical_inversions: MinimalChordDecompositionInput
    chord: ChordOnFrettedInstrument

    def __post_init__(self):
        assert_typing(self.instrument, FrettedInstrument)
        assert_typing(self.identical_inversions, MinimalChordDecompositionInput)
        assert_typing(self.chord, ChordOnFrettedInstrument)

    def is_open(self):
        return self.chord.is_open()

    def transposed(self):
        """The chord as it should be presented as svg, and the transposition compared to `chord`."""
        if self.is_open():
            return self.chord, ChromaticInterval(0)
        return self.chord.transpose_to_fret_one()
    
    def lily_field(self, path:str):
        lowest_note = Note.from_chromatic(self.chord.get_most_grave_note().get_chromatic())
        inversion_patterns = self.identical_inversions.get_inversion_patterns()
        inversion_pattern = inversion_patterns[0]
        note_list: NoteList = inversion_pattern.interval_list.from_note(lowest_note)
        ensure_folder(path)
        file_prefix = note_list.lily_file_name()
        path_prefix = f"{path}/{file_prefix}"
        code = note_list.lily_file_with_only_chord()
        lily.compile_(code, path_prefix, wav=False)
        return img_tag(f"{file_prefix}.svg")
    
    def open(self):
        self.chord.is_open()
    
    def colors(self):
        return ChordColors(self.tonic())
    
    def tonic(self):
        lowest_note = self.chord.get_most_grave_note().get_chromatic()
        return lowest_note - self.identical_inversions.get_tonic_minus_lowest_note().get_chromatic()
    
    def single_role_field(self, folder_path: str, interval_values: List[int]):
        transposed, transposition = self.transposed()
        intervals = [ChromaticInterval(iv) for iv in interval_values]
        notes = [self.tonic() + interval for interval in intervals]
        notes_in_base_octave = [note.in_base_octave() for note in notes]
        restricted_chord = transposed.restrict_to_note_up_to_octave(notes_in_base_octave)
        if restricted_chord is None:
            return ""
        return img_tag(restricted_chord.save_svg(folder_path, self.instrument, colors=self.colors(), absolute=self.open()))

    def first_string(self):
        for string_number, fret in enumerate(self.chord.get_frets(self.instrument)):
            if fret.is_played():
                return string_number + 1
        assert False

    def first_string(self):
        last_string = None
        for string_number, fret in enumerate(self.chord.get_frets(self.instrument)):
            if fret.is_played():
                last_string = string_number + 1
        assert last_string
        return last_string

    #pragma mark - CsvGenerator

    def csv_content(self, folder_path: str) -> Generator[str]:
        transposed, transposition = self.transposed()
        notations = self.identical_inversions.notations()

        yield notations[0] # notation
        yield ", ".join(notations[1:]) # other notations
        yield img_tag(transposed.save_svg(folder_path, self.instrument, colors=None, absolute=self.open())) # Chord
        yield img_tag(transposed.save_svg(folder_path, self.instrument, colors=self.colors(), absolute=self.open())) # Colored chord
        yield img_tag(self.lily_field(f"{folder_path}/lily")) # partition
        yield str(self.first_string())
        yield str(self.last_string())
        yield from [self.single_role_field(interval_values) for interval_values in [[0], [1, 2], [3, 4], [5], [6, 7, 8], [9, 10, 11]]]

    #pragma mark - ClassWithEasyness

    def easy_key(self):
        return (self.identical_inversions.easy_key(), self.chord.easy_key())