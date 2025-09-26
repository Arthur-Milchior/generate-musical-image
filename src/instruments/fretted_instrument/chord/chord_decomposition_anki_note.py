from dataclasses import dataclass, field
from tkinter.font import names
from typing import Generator, List, Tuple

from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.black_only import BlackOnly
from instruments.fretted_instrument.position.fretted_position_maker.conditional_fretted_position_maker import ConditionalFrettedPositionMaker
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_for_interval import FrettedPositionMakerForInterval
from lily.sheet.lily_chord_sheet import LilyChordSheet
from lily.staff.lily_chord_staff import LilyChordStaff
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import MinimalChordDecompositionInput
from solfege.value.interval.chromatic_interval import ChromaticInterval
from _lily import lily
from solfege.value.note.note import Note
from solfege.value.note.set.note_list import NoteList
from utils.csv import CsvGenerator
from solfege.value.key.keys import key_of_C
from utils.easyness import ClassWithEasyness
from utils.util import assert_typing, ensure_folder, img_tag

@dataclass(frozen=True)
class ChordDecompositionAnkiNote(ClassWithEasyness[Tuple[Tuple[int, int], int]], CsvGenerator):
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
            return self.chord, ChromaticInterval.make(0)
        return self.chord.transpose_to_fret_one()
    
    def decomposition_lily_field(self, path:str):
        lowest_note = Note.from_chromatic(self.chord.get_most_grave_note().get_chromatic())
        inversion_patterns = self.identical_inversions.get_inversion_patterns()
        inversion_pattern = inversion_patterns[0]
        note_to_use: NoteList = inversion_pattern.interval_list.from_note(lowest_note)

        chromatic_note_list = self.chord.chromatic_notes()
        note_list = note_to_use.change_octave_to_be_enharmonic(chromatic_note_list)

        clef = self.instrument.clef()
        sheet = LilyChordSheet.make(staff = LilyChordStaff.make(notes = note_list.notes, clef=clef, first_key = key_of_C))

        return img_tag(sheet.maybe_generate())
    
    def is_open(self):
        return self.chord.is_open()
    
    def fretted_position_maker(self, all_marked:bool):
        style = "fill: red;font: italic 12px serif;" if all_marked else None
        color = "red" if all_marked else None
        return FrettedPositionMakerForInterval.make(
            tonic=self.tonic().in_base_octave(),
            pattern=self.identical_inversions.get_inversion_patterns()[0].base,
            style=style,
            circle_color=color
            )
    
    def tonic(self):
        lowest_note = self.chord.get_most_grave_note().get_chromatic()
        return lowest_note - self.identical_inversions.get_tonic_minus_lowest_note().get_chromatic()
    
    def single_role_field(self, folder_path: str, interval_values: List[int]):
        transposed, transposition = self.transposed()
        intervals = [ChromaticInterval.make(iv) for iv in interval_values]
        notes = [self.tonic() + interval for interval in intervals]
        notes_in_base_octave = [note.in_base_octave() for note in notes]
        restricted_chord = transposed.restrict_to_note_up_to_octave(notes_in_base_octave)
        if restricted_chord is None:
            return ""
        is_open = self.is_open()
        all_colors = self.fretted_position_maker(all_marked=False)
        #interval_values = ChromaticIntervalListPattern.make_absolute(interval_values)
        fretted_position_maker = ConditionalFrettedPositionMaker(all_colors, interval_values, BlackOnly(), self.tonic())
        minimal_number_of_frets = self.last_shown_fret()
        svg_file_name = transposed.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=fretted_position_maker, absolute=is_open, minimal_number_of_frets=minimal_number_of_frets)
        return img_tag(svg_file_name)

    def first_string(self):
        for string_number, fret in enumerate(self.chord.get_frets(self.instrument)):
            if fret.is_played():
                return string_number + 1
        assert False

    def last_string(self):
        last_string = None
        for string_number, fret in enumerate(self.chord.get_frets(self.instrument)):
            if fret.is_played():
                last_string = string_number + 1
        assert last_string
        return last_string
    
    def last_shown_fret(self):
        return self.chord.last_shown_fret()

    #pragma mark - CsvGenerator

    def csv_content(self, folder_path: str, lily_folder_path: str) -> Generator[str]:
        transposed, transposition = self.transposed()
        notations = self.identical_inversions.notations()

        yield notations[0] # notation
        yield ", ".join(notations[1:]) # other notations
        yield img_tag(transposed.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=BlackOnly(), absolute=self.is_open())) # Chord
        yield img_tag(transposed.save_svg(folder_path, instrument=self.instrument, fretted_position_maker=self.fretted_position_maker(all_marked=True), absolute=self.is_open())) # Colored chord
        yield self.decomposition_lily_field(f"{lily_folder_path}") # partition
        yield "x" if self.is_open else ""
        yield str(self.first_string())
        yield str(self.last_string())
        yield from [self.single_role_field(folder_path, interval_values) for interval_values in [[0], [1, 2], [3, 4], [5], [6, 7, 8], [9, 10, 11]]]
        yield self.instrument.get_name()

    #pragma mark - ClassWithEasyness

    def easy_key(self) -> Tuple[Tuple[int, int], int]:
        return (self.identical_inversions.easy_key(), self.chord.easy_key())