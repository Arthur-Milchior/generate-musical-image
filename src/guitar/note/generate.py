from dataclasses import dataclass
from guitar.position.fret.fret import HIGHEST_FRET, OPEN_FRET
from guitar.position.string.string import String, strings
from guitar.position.guitar_position import GuitarPosition
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.value.note.chromatic_note import ChromaticNote
from guitar.position.set.set_of_guitar_positions import SetOfGuitarPositions
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.alteration import Alteration
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note
from utils.util import assert_typing
from consts import generate_root_folder
from utils.util import ensure_folder

folder_path = f"{generate_root_folder}/guitar/note"
ensure_folder(folder_path)

lowest_guitar_note = GuitarPosition(strings[0], OPEN_FRET).get_chromatic()
highest_guitar_note = GuitarPosition(strings[5], HIGHEST_FRET).get_chromatic()

@dataclass()
class AnkiNote:
    note: ChromaticNote

    def __post_init__(self):
        super().__post_init__()
        assert_typing(self.note, ChromaticNote)
        assert lowest_guitar_note <= self.note <= highest_guitar_note
        positions = GuitarPosition.from_chromatic(self.note)
        self.dic = {
            pos.string: pos for pos in positions
        }

    def positions(self):
        return self.dic.values()
    
    def name_for_field(self):
        return self.note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output = AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)

    def svg_name_for_all_positions(self):
        return f"guitar{self.note.file_name()}.svg"
    
    def strings(self):
        return frozenset(pos.string for pos in self.positions())
        
    def field_for_string(self, string: String):
        pos = self.dic.get(string)
        if pos is None:
            return ""
        return img_tag(pos.singleton_diagram_svg_name())
    
    def svg(self):
        return SetOfGuitarPositions(frozenset(self.positions())).svg(absolute=True)
    
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
    
    def anki_fields(self):
        return [
            self.name_for_field(),
            self.all_notes_field(),
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
    
    def anki_csv(self):
        return ",".join(self.anki_fields())
    
anki_notes = []
note = lowest_guitar_note
while note <= highest_guitar_note:
    anki_note = AnkiNote(note)
    save_file(f"{folder_path}/{anki_note.svg_name_for_all_positions()}", anki_note.svg())
    anki_notes.append(anki_note.anki_csv())
    note += ChromaticInterval(1)
save_file(f"{folder_path}/anki.csv", "\n".join(anki_notes))