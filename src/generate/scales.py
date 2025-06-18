from utils import util
from solfege.key import sets_of_enharmonic_keys
from typing import Optional, Dict, List
from solfege.scale.scale_pattern import scale_patterns_I_practice, scale_patterns, minor_melodic
from operator import itemgetter
from lily.lily import compile_
from dataclasses import dataclass
from solfege.chord.chord_pattern import ChordPattern
from solfege.interval.interval import Interval
from solfege.note import Note


folder_path = "../generated/solfege/scales"
util.ensure_folder(folder_path)


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
    transposition: Interval = Interval(0, 0)

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
            note = Note(note).get_chromatic().get_in_base_octave()
            self.difficulty_notes[note] = max(value, self.difficulty_notes.get(note, 0))

    def difficulty(self, note: Note):
        return self.difficulty_notes.get(note.get_chromatic().get_in_base_octave, super().difficulty(note))

    """
    transposition: Interval = Interval(0, 0)
    note_difficulties: Optional[Dict[str, int]] = None
    simple_notes: Optional[List[str]]"""


ocarina_harmorny_double = ChromaticInstrumentWithDifficultNote("ocarina_pendant", Note("C4"), Note("E5"),
                             {"C4#":1, "E♭4":1, })
ocarina_pendant = ChromaticInstrumentWithDifficultNote("ocarina_pendant", Note("C4"), Note("E5"),
                             {"C4#":1, "E♭4":1, })

ocarina_harmorny_triple = Instrument("ocarina_harmony_triple", Note("A4"), Note("E♭6"))
ocarina_transverse = Instrument("ocarina_transverse", Note("C4"), Note("C6"))
mv_ocarina = Instrument("mv_ocarina", Note("B3"), Note("E5"))
saxophone = Instrument("saxophone", Note("B♭3"), Note("A6"))
tin_whistle = ChromaticInstrumentWithDifficultNote("tin_whistle", Note("D4"), Note("D6"), 
                                                   {
                                                    "D4#":2,
                                                    "F4":2,
                                                    "G#4":2,
                                                    "B♭4":1,
                                                    "A#4":1,
                                                    "C5":1,
                                                   }, Interval(chromatic=2, diatonic=1),)
recorder = ChromaticInstrumentWithDifficultNote("recorder", Note("C4"), Note("D6"),
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
harmonica_diatonic = ChromaticInstrumentWithDifficultNote("harmonica_diatonic", Note("C3"), Note("C6"), {
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
haromnica_chromatic = Instrument("harmonica_chromatic", Note("C3"), Note("C7#"))

instruments: List[Instrument] = [
    ocarina_harmorny_double,
    ocarina_pendant,
    ocarina_harmorny_triple,
    ocarina_transverse,
    mv_ocarina,
    saxophone,
    tin_whistle,
    recorder,
    harmonica_diatonic,
    haromnica_chromatic
    ]

all_csv = []
for instrument in instruments:
    instrument_image = f"""<img src="{instrument}.png"/>"""
    csv_path = f"{folder_path}/{instrument}.csv"
    anki_notes = []
    for patterns, specific in ((chords, "Arpeggio"), (scale_patterns, "Scale"), ):
        for scale_pattern in patterns:
            scale_name = scale_pattern.names[0]
            anki_notes_in_scale = []
            for set_of_enharmonic_keys in sets_of_enharmonic_keys:
                bass_note = set_of_enharmonic_keys[0].note + instrument.transposition - scale_pattern.interval_for_signature
                while bass_note < instrument.lowest_instrument_note:
                    bass_note = bass_note.add_octave(1)
                while bass_note >= instrument.lowest_instrument_note.add_octave(1):
                    bass_note = bass_note.add_octave(-1)
                scale = scale_pattern.generate(
                        fundamental=bass_note,
                        number_of_octaves=1,
                        )
                difficulties = [instrument.difficulty(note) for note in scale.notes]
                if None in difficulties: 
                    continue
                difficulty = max(difficulties)
                tonic_name = bass_note.get_symbol_name()
                note = []
                note.append(f"{instrument} {scale_name.replace(",", "")} {bass_note.get_full_name()} difficulty {difficulty}") # key
                note.append(instrument_image)
                note.append("") # Hide single octave
                note.append("") # Practice single direction
                note.append("") #signature
                note.append("") #position
                note.append(tonic_name)  #tonic
                note.append(scale_name) # mode
                note.append(specific) # specific
                note.append(bass_note.image_html())#0
                note.append(bass_note.add_octave(1).image_html()) # 1
                note.append(bass_note.add_octave(2).image_html()) # 2

                for (start_octave, number_of_octaves) in [(0, 1), (1,1), (0,2), (2,1), (1,2), (0,3)]:
                    scale_lowest_note = bass_note.add_octave(start_octave)
                    for direction in [
                        (INCREASING),
                        (DECREASING),
                        (TOTAL),
                        (REVERSE)
                    ]:
                        if bass_note.add_octave(start_octave+number_of_octaves) > instrument.highest_instrument_note:
                            note.append("")
                        else:
                            file_name = f"""{scale_name}-{scale_lowest_note.get_ascii_name(fixed_length=False)}-{number_of_octaves}-{direction}"""
                            note.append(f"""<img src="{file_name}.svg"/>""")
                note.append(bass_note.add_octave(2).image_html()) # 1
                anki_notes_in_scale.append((difficulty, note))

            anki_notes_in_scale.sort(key=itemgetter(0))
            anki_notes.extend(anki_note for _, anki_note in anki_notes_in_scale)
    csv = "\n".join(",".join(anki_note) for anki_note in anki_notes)
    all_csv += anki_notes
    print(f"{csv_path=}")
    with open(csv_path, "w") as f:
        f.write(csv)


all_csv_path = f"{folder_path}/all.csv"
csv = "\n".join(",".join(note) for note in all_csv)
with open(all_csv_path, "w") as f:
    f.write(csv)


for patterns, specific in ((chords, "Arpeggio"), (scale_patterns, "Scale"), ):
    for scale_pattern in patterns:
        scale_name = scale_pattern.names[0]
        for set_of_enharmonic_keys in sets_of_enharmonic_keys:
            bass_key = set_of_enharmonic_keys[0]
            bass_note = bass_key.note
            tonic_name = bass_note.get_symbol_name()

            for (start_octave, number_of_octaves) in [(0, 1), (1,1), (0,2)]:
                    scale_lowest_note = bass_note.add_octave(start_octave)
                    increasing = scale_pattern.generate(
                        fundamental=scale_lowest_note,
                        number_of_octaves=number_of_octaves
                        )
                    decreasing = scale_pattern.descending.generate(
                        fundamental=scale_lowest_note,
                        number_of_octaves=number_of_octaves
                        ).reverse()
                    total = increasing.concatenate(decreasing)
                    reverse = decreasing.concatenate(increasing)
                    for direction, scale in [
                        (INCREASING, increasing),
                        (DECREASING, decreasing),
                        (TOTAL, total),
                        (REVERSE, reverse)
                    ]:
                        file_name = f"""{scale_name}-{scale_lowest_note.get_ascii_name(fixed_length=False)}-{number_of_octaves}-{direction}"""
                        code = scale.lily()
                        path = f"{folder_path}/{file_name}"
                        compile_(
                            code,
                            file_prefix=path,
                            wav=False,
                            )
