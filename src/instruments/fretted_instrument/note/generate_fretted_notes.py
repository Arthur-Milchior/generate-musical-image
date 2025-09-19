from dataclasses import dataclass, field
from typing import Dict, Optional
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.string.string import String
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.value.note.chromatic_note import ChromaticNote
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, SetOfPositionsOnFrettedInstrumentFrozenList
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.alteration import Alteration
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_typing, img_tag, save_file
from consts import generate_root_folder
from utils.util import ensure_folder



@dataclass(frozen=True)
class AnkiNote(DataClassWithDefaultArgument, CsvGenerator):
    instrument: FrettedInstrument
    note: ChromaticNote
    string_to_pos: Dict[String, PositionOnFrettedInstrument] = field(hash=False)

    def __post_init__(self):
        super().__post_init__()
        assert_typing(self.note, ChromaticNote)
        assert self.instrument.lowest_note() <= self.note <= self.instrument.highest_note()

    @classmethod
    def make_note(cls, instrument, note):
        positions = PositionOnFrettedInstrument.from_chromatic(instrument, note, True)
        string_to_pos = {
            pos.string: pos for pos in positions
        }
        return cls(instrument, note, string_to_pos) 

    def folder_path(self):
        folder_path =  f"{generate_root_folder}/{self.instrument.name}/note"
        ensure_folder(folder_path)
        return folder_path

    def positions(self):
        return PositionOnFrettedInstrumentFrozenList(self.string_to_pos.values())
    
    def name_for_field(self):
        return self.note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output = AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)

    def svg_name_for_all_positions(self):
        return f"{self.instrument.name}_{self.note.file_name()}.svg"
    
    def strings(self):
        return frozenset(pos.string for pos in self.positions())
        
    def field_for_string(self, string: Optional[String]):
        if string is None:
            return ""
        pos = self.string_to_pos.get(string)
        if pos is None:
            return ""
        return img_tag(pos.singleton_diagram_svg_name(self.instrument))
    
    def svg(self):
        return SetOfPositionOnFrettedInstrument(self.positions()).svg(instrument=instrument, absolute=True)
    
    def all_notes_field(self):
        return img_tag(self.svg_name_for_all_positions())
    
    def _note(self) -> Note:
        return self.note.get_note()
    
    def diatonic_note(self)->DiatonicNote:
        return self._note().get_diatonic()
    
    def degree(self):
        return self.diatonic_note().get_name_up_to_octave(note_output=NoteOutput.NUMBER, fixed_length=FixedLengthOutput.NO)
    
    def alteration(self) -> Alteration:
        return self._note().get_alteration()
    
    def height(self):
        return str(self._note().get_octave_name(octave_notation=OctaveOutput.MIDDLE_IS_4))
    
    def partition_field(self):
        return img_tag(Note.from_chromatic(self.note).image_file_name(self.instrument.clef))

    #pragma mark - CsvGenerator
    
    def csv_content(self):
        strings = list(self.instrument.strings())
        while len(strings) < 6:
            strings.append(None)
        return [
            self.name_for_field(),
            self.partition_field(),
            self.all_notes_field(),
            self.instrument.name,
            self.field_for_string(strings[0]),
            self.field_for_string(strings[1]),
            self.field_for_string(strings[2]),
            self.field_for_string(strings[3]),
            self.field_for_string(strings[4]),
            self.field_for_string(strings[5]),
            self.degree(),
            self.alteration().get_name(alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO),
            self.height(),
        ]
    
for instrument in fretted_instruments:
    anki_notes = []
    current_note = instrument.lowest_note()
    while current_note <= instrument.highest_note():
        anki_note = AnkiNote.make_note(instrument, current_note)
        folder_path = anki_note.folder_path()
        save_file(f"{folder_path}/{anki_note.svg_name_for_all_positions()}", anki_note.svg())
        anki_notes.append(anki_note.csv())
        current_note += ChromaticInterval(1)
    save_file(f"{folder_path}/anki.csv", "\n".join(anki_notes))