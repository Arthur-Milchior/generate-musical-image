from enum import Enum
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from utils import util
from solfege.value.key.key import Key, sets_of_enharmonic_keys
from typing import Optional, Dict, List, assert_never
from solfege.pattern.scale.scale_pattern import ScalePattern, scale_patterns_I_practice, scale_patterns, minor_melodic
from operator import itemgetter
from lily.lily import compile_
from dataclasses import dataclass
from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note
from consts import generate_root_folder


folder_path = f"{generate_root_folder}/solfege/scales"
util.ensure_folder(folder_path)


class Direction(Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    TOTAL = "total"
    REVERSE = "reverse"

chords = [ chord.to_arpeggio_pattern()  for chord in  ChordPattern.class_to_patterns[ChordPattern]]


@dataclass(frozen=True)
class Instrument:
    """Represents the information needed to generate scales"""
    name: str
    lowest_instrument_note: Note
    highest_instrument_note: Note
    transposition: Interval = Interval.make(0, 0)
    show_fingering: bool = True
    image_extension: str = "png"

    def difficulty(self, note) -> Optional[int]:
        return 0 if self.lowest_instrument_note <= note <= self.highest_instrument_note else None
    
    def __str__(self):
        return self.name

class ChromaticInstrumentWithDifficultNote(Instrument):
    """Chromatic instrument from lowest to highest
    
    difficulty_notes: map from chromatic note to the difficulty of playing it.
    """
    def __init__(self, name: str, lowest: Note, highest: Note, difficulty_notes: Dict[str, int], transposition: Optional[Interval]= None):
        super().__init__(name, lowest, highest)
        self.difficulty_notes = dict()
        for note, value in difficulty_notes.items():
            note = Note(note).get_chromatic().in_base_octave()
            self.difficulty_notes[note] = max(value, self.difficulty_notes.get(note, 0))

    def difficulty(self, note: Note):
        return self.difficulty_notes.get(note.get_chromatic().in_base_octave(), super().difficulty(note))

    """
    transposition: Interval = Interval.make(0, 0)
    note_difficulties: Optional[Dict[str, int]] = None
    simple_notes: Optional[List[str]]"""


ocarina_harmorny_double = ChromaticInstrumentWithDifficultNote("ocarina_pendant", Note.from_name("C4"), Note.from_name("E5"),
                             {"C4#":1, "E♭4":1, })
ocarina_pendant = ChromaticInstrumentWithDifficultNote("ocarina_pendant", Note.from_name("C4"), Note.from_name("E5"),
                             {"C4#":1, "E♭4":1, })

ocarina_harmorny_triple = Instrument("ocarina_harmony_triple", Note.from_name("A4"), Note.from_name("E♭6"))
ocarina_transverse = Instrument("ocarina_transverse", Note.from_name("C4"), Note.from_name("C6"))
mv_ocarina = Instrument("mv_ocarina", Note.from_name("B3"), Note.from_name("E5"))
saxophone = Instrument("saxophone", Note.from_name("B♭3"), Note.from_name("A6"))
tin_whistle = ChromaticInstrumentWithDifficultNote("tin_whistle", Note.from_name("D4"), Note.from_name("D6"), 
                                                   {
                                                    "D4#":2,
                                                    "F4":2,
                                                    "G#4":2,
                                                    "B♭4":1,
                                                    "A#4":1,
                                                    "C5":1,
                                                   }, Interval.make(chromatic=2, diatonic=1),)
recorder = ChromaticInstrumentWithDifficultNote("recorder", Note.from_name("C4"), Note.from_name("D6"),
                                                   {
                                                       "C4#": 2,
                                                       "E4♭": 2,
                                                       "F4": 1,
                                                       "F#4": 1,
                                                       "G#4": 1,
                                                       "B4♭": 1,
                                                       "C5#": 2,
                                                       "D5": 1,
                                                   })
harmonica_diatonic = ChromaticInstrumentWithDifficultNote("harmonica_diatonic", Note.from_name("C3"), Note.from_name("C6"), {
    "D3♭": 1,
    "F#3": 1,
    "F3": 2,
    "B♭3": 1,
    "A3": 2,
    "A3♭": 3,
    "C#4": 1,
    "A♭4": 1,
    "E♭6": 2,
    "F#6": 2,
    "B6": 2,
    "B6♭": 3,
})
haromnica_chromatic = Instrument("harmonica_chromatic", Note.from_name("C3"), Note.from_name("C7#"))

instruments: List[Instrument] = [
#    ocarina_harmorny_double,
 #   ocarina_pendant,
  #  ocarina_harmorny_triple,
   # ocarina_transverse,
#    mv_ocarina,
 #   saxophone,
    tin_whistle,
    recorder,
    harmonica_diatonic,
    haromnica_chromatic
    ]

class Difficulties:
    def __init__(self):
        self.difficulties = dict()
        self.biggest = 0

    def add(self, d):
        self.biggest = max(d, self.biggest)
        self.difficulties[d] = self.difficulties.get(d, 0) + 1

    def __eq__(self, value):
        return self.difficulties == value.difficulties
    
    def __hash__(self):
        return hash(self.difficulties)
     
    def __lt__(self, other):
        if self.biggest > other.biggest:
            return False
        if self.biggest < other.biggest:
            return True
        for d in range(self.biggest, -1, -1):
            if self.difficulties.get(d, 0) > other.difficulties.get(d, 0):
                return False
            if self.difficulties.get(d, 0) < other.difficulties.get(d, 0):
                 return True
        return False
    
    def __str__(self):
        return str(self.difficulties)

@dataclass
class AnkiNote:
    instrument: Instrument
    scale_pattern: ScalePattern
    specific: str
    set_of_enharmonic_keys: List[Key]

    def csv_path(self):
        return f"{folder_path}/{self.instrument}.csv"

    def instrument_image(self):
        return f"""<img src="{self.instrument}.png"/>"""

    def interval(self):
        return self.instrument.transposition - self.scale_pattern.interval_for_signature

    def scale_name(self):
        return self.scale_pattern.names[0]
    
    def scale_notation(self):
        return self.scale_pattern.notation or ""

    def bass_note(self):
        bass_note = self.set_of_enharmonic_keys[0].note + self.interval()
        while bass_note < instrument.lowest_instrument_note:
            bass_note = bass_note.add_octave(1)
        while bass_note >= instrument.lowest_instrument_note.add_octave(1):
            bass_note = bass_note.add_octave(-1)
        return bass_note
    
    def scale_for_difficulty(self):
        return self.scale_pattern.from_note(
                        tonic=bass_note,
                        number_of_octaves=1,
                        )

    def difficulties(self):
        """None if not playable"""
        difficulties = Difficulties()
        for note in self.scale_for_difficulty().notes:
            difficulty = instrument.difficulty(note)
            if difficulty is None:
                return None
            difficulties = difficulties.add(difficulty)
        return difficulties
    
    def tonic_name(self):
        return self.bass_note().get_name_with_octave(
                    octave_notation=OctaveOutput.MIDDLE_IS_4,
                    alteration_output = AlterationOutput.SYMBOL,
                    note_output= NoteOutput.LETTER,
                    fixed_length = FixedLengthOutput.NO,
                )
    
    def key(self):
        "A value uniquely identifiying this anki note"
        return f"""\"{self.instrument} {self.scale_name().replace(",", "")} {self.tonic_name()} difficulty {self.difficulties()}\""""
    
    def anki_fields(self):
        bass_note = self.bass_note()
        fields = [
            self.key(),
            self.instrument_image(),
            "", #hide single octave
            "",#practice single direction
            "", #signature
            "", #position
            self.tonic_name(),
            self.scale_name(),
            self.scale_notation(),
            self.specific(),
            bass_note.image_html(),
            bass_note.add_octave(1).image_html(),
            bass_note.add_octave(2).image_html(),
            bass_note.add_octave(3).image_html(),
        ]
        for (start_octave, number_of_octaves) in [(0, 1), (1,1), (0,2), (2,1), (1,2), (0,3)]:
            for direction in [Direction.INCREASING, Direction.DECREASING, Direction.TOTAL, Direction.REVERSE]:
                anki_field = AnkiField(self, start_octave, number_of_octaves, direction)
                fields.append(anki_field.field())
                anki_field.generate_and_compile_lily()
        return fields
    
    def anki_csv(self):
        return ",".join(self.anki_fields())
        

@dataclass
class AnkiField:
    """Represents a field in anki"""
    anki_note: AnkiNote
    start_octave: int
    number_of_octaves: int
    direction: Direction

    def scale_lowest_note(self):
        return self.anki_note.bass_note().add_octave(self.start_octave)

    def scale(self):
        increasing = self.anki_note.scale_pattern.from_note(
            tonic=self.scale_lowest_note(),
            number_of_octaves=self.number_of_octaves,
            )
        decreasing = self.anki_note.scale_pattern.descending.from_note(
            tonic=self.scale_lowest_note(),
            number_of_octaves=self.number_of_octaves,
            ).reverse()
        if self.direction is Direction.INCREASING:
            return increasing
        elif self.direction is Direction.DECREASING:
            return decreasing
        elif self.direction is Direction.TOTAL:
            return increasing.concatenate(decreasing)
        elif self.direction is Direction.REVERSE:
            return decreasing.concatenate(increasing)
        assert_never(self.direction)

    def playable(self):
        return self.anki_note.bass_note() <= self.anki_note.instrument.highest_instrument_note
    
    def scale_note_name(self):
        return self.scale_lowest_note.get_name_with_octave(
                                octave_notation=OctaveOutput.MIDDLE_IS_4,
                                alteration_output = AlterationOutput.ASCII, 
                                note_output = NoteOutput.LETTER, 
                                fixed_length = FixedLengthOutput.NO)
    

    def svg_scale_file_name(self):
        """The file name without extension."""
        return f"""{self.anki_note.scale_name()}-{self.scale_note_name()}-{self.number_of_octaves}-{self.direction}"""
    
    def path(self):
        return f"{folder_path}/{self.svg_scale_file_name}"
    
    def lily(self):
        return self.scale.lily()
    
    def generate_and_compile_lily(self):
        compile_(self.lily(), file_prefix=self.path(), wav = False)
    
    def svg_scale_html(self):
        return f"""<img src="{self.svg_scale_file_name()}.svg"/>"""
    
    def fingerings_html(self):
        field_parts = []
        for note_in_scale in self.notes():
            chromatic_note: ChromaticNote = note_in_scale.get_chromatic()
            note_name = chromatic_note.get_name_with_octave(
                octave_notation=OctaveOutput.MIDDLE_IS_4,
                alteration_output = AlterationOutput.ASCII, 
                note_output = NoteOutput.LETTER, 
                fixed_length = FixedLengthOutput.NO
            )
            field_parts.append(f"""<img src="{self.anki_note.instrument}_{note_name}.{self.anki_note.instrument.image_extension}"/>""")
        return field_parts            


    def field(self):
        if not self.playable():
            return ""
        field_parts = [self.svg_scale_html()]
        if self.anki_note.instrument.show_fingering:
            field_parts.append("<br/>")
            field_parts += self.fingerings_html()
        return "".join(field_parts)
            

all_csv = []
for instrument in instruments:
    instrument_image = f"""<img src="{instrument}.png"/>"""
    csv_path = f"{folder_path}/{instrument}.csv"
    anki_notes: List[str] = []
    for patterns, specific in ((chords, "Arpeggio"), (scale_patterns, "Scale"), ):
        for scale_pattern in patterns:
            anki_notes_in_scale = []
            for set_of_enharmonic_keys in sets_of_enharmonic_keys:
                anki_note = AnkiNote(instrument, scale_pattern, specific, set_of_enharmonic_keys)
                anki_notes_in_scale.append((anki_note.difficulties(), anki_note.anki_csv()))

            anki_notes_in_scale.sort(key=itemgetter(0))
            for _, anki_note_csv in anki_notes_in_scale:
                anki_notes.append(anki_note_csv)
    csv = "\n".join(anki_notes)
    with open(csv_path, "w") as f:
        f.write(csv)

