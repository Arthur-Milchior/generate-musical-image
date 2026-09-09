from dataclasses import dataclass, field
from typing import Dict, Optional
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.positions_consts import FONT_SIZE
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.black_only import BlackOnly
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_for_note import FrettedPositionMakerForNote
from instruments.fretted_instrument.position.string.string import String
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList
from lily.sheet.lily_sheet_single_note import sheet_single_note
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.value.note.chromatic_note import ChromaticNote
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import SetOfPositionOnFrettedInstrument, SetOfPositionsOnFrettedInstrumentFrozenList
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.note_alteration import NoteAlteration
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note
from utils.csv import CsvGenerator
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.svg.svg_generator import SvgSaver
from utils.util import assert_typing, img_tag, save_file
from consts import generate_root_folder
from utils.util import ensure_folder



@dataclass(frozen=True)
class NoteOnFrettedInstrumentAnkiNote(DataClassWithDefaultArgument, CsvGenerator, SvgSaver):
    """Anki note (and diagram) for a single pitch on a fretted instrument, showing where it can be played on
    each string."""
    instrument: FrettedInstrument
    """The instrument this note is played on."""
    chromatic_note: ChromaticNote
    """The pitch represented by this note."""
    string_to_pos: Dict[String, PositionOnFrettedInstrument] = field(hash=False)
    """Maps each string on which `chromatic_note` can be played to the fretted position on that string."""

    def __post_init__(self):
        """Validate the base class invariants, that `chromatic_note` has the right type, and that it falls
        within the instrument's playable range."""
        super().__post_init__()
        assert_typing(self.chromatic_note, ChromaticNote)
        assert self.instrument.lowest_note() <= self.chromatic_note <= self.instrument.highest_note()

    @classmethod
    def make_note(cls, instrument, note):
        """Build the note by locating every position on `instrument` (any string, unrestricted fret range)
        that plays `note`."""
        positions = PositionOnFrettedInstrument.from_chromatic(instrument, note, True)
        string_to_pos = {
            pos.string: pos for pos in positions
        }
        return cls(instrument, note, string_to_pos)

    def folder_path(self):
        """Return the folder where this instrument's note diagrams/CSV are written, creating it if needed."""
        folder_path =  f"{self.instrument.generated_folder_name()}/note"
        ensure_folder(folder_path)
        return folder_path

    def positions(self):
        """All positions (across every string) that play this note, as a `PositionOnFrettedInstrumentFrozenList`."""
        return PositionOnFrettedInstrumentFrozenList(self.string_to_pos.values())

    def name_for_field(self):
        """Note name (letter + octave) used as the Anki field value."""
        return self.chromatic_note.get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output = AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)

    def strings(self):
        """The set of strings on which this note can be played."""
        return frozenset(pos.string for pos in self.positions())

    def field_for_string(self, string: Optional[String]):
        """Anki field content for `string`: an `<img>` tag for that string's diagram, or `""` if `string` is
        `None` or does not carry this note."""
        if string is None:
            return ""
        pos = self.string_to_pos.get(string)
        if pos is None:
            return ""
        return img_tag(pos.singleton_diagram_svg_name(self.instrument))

    def all_notes_field(self):
        """Anki field: `<img>` tag for the diagram showing this note on every string at once."""
        return img_tag(self.svg_name())

    def _note(self) -> Note:
        """This note's pitch as a `Note` (diatonic-aware pitch, rather than the plain `ChromaticNote`)."""
        return self.chromatic_note.get_note()

    def diatonic_note(self)->DiatonicNote:
        """The diatonic (letter-name) representation of this note."""
        return self._note().get_diatonic()

    def degree(self):
        """Scale degree number of this note within its octave, as text."""
        return self.diatonic_note().get_name_up_to_octave(note_output=NoteOutput.NUMBER, fixed_length=FixedLengthOutput.NO)

    def alteration(self) -> NoteAlteration:
        """This note's alteration (sharp/flat/natural)."""
        return self._note().get_alteration()

    def height(self):
        """This note's octave number, using the middle-C-is-4 convention."""
        return str(self._note().get_octave_name(octave_notation=OctaveOutput.MIDDLE_IS_4))

    def partition_field(self):
        """Anki field: `<img>` tag for the note rendered on a staff, generated (and cached) via LilyPond."""
        sheet = sheet_single_note(Note.from_chromatic(self.chromatic_note), self.instrument.clef())
        img_name = sheet.maybe_generate()
        return img_tag(img_name)

    #pragma mark - SvgSaver

    def svg(self):
        """Render the diagram showing this note highlighted on every string that plays it."""
        singleton = SetOfPositionOnFrettedInstrument(positions=self.positions(), absolute=True)
        maker = FrettedPositionMakerForNote.make(text_size=FONT_SIZE-2)
        return singleton.svg(instrument=instrument, fretted_position_maker=maker)

    def _svg_name_base(self):
        """Base file name for the diagram: instrument name plus an unambiguous note name."""
        return f"{self.instrument.get_name()}_{self.chromatic_note.non_ambiguous_string_for_file_name()}"

    #pragma mark - CsvGenerator

    def csv_content(self):
        """Ordered Anki fields: note name, staff image, all-strings image, instrument name, one image per
        string (padded to 6 slots), degree, alteration symbol, and octave."""
        strings = list(self.instrument.strings())
        while len(strings) < 6:
            strings.append(None)
        return [
            self.name_for_field(),
            self.partition_field(),
            self.all_notes_field(),
            self.instrument.get_name(),
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
        anki_note = NoteOnFrettedInstrumentAnkiNote.make_note(instrument, current_note)
        folder_path = anki_note.folder_path()
        path = f"{folder_path}/{anki_note.svg_name()}"
        save_file(path, anki_note.svg())
        anki_notes.append(anki_note.csv())
        current_note += ChromaticInterval.make(1)
    save_file(f"{folder_path}/anki.csv", "\n".join(anki_notes))

    for string in instrument.strings():

        two_selected_strings = SetOfPositionOnFrettedInstrument.make(
            positions = [], 
            absolute=True,)
        two_selected_strings.save_svg(folder_path=folder_path,
                                      keep_in_collection=True,
                                      instrument=instrument, 
                                      fretted_position_maker=BlackOnly(), 
            minimal_number_of_frets = Fret(instrument.max_distance_between_two_closed_frets() + 1, absolute=False), 
            colored_strings = [string]
            )

