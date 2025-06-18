from utils import util
from solfege.key import sets_of_enharmonic_keys
from typing import Optional
from solfege.scale.scale_pattern import scale_patterns_I_practice, scale_patterns, minor_melodic
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
    name: str
    lowest_instrument_note: Note
    highest_instrument_note: Note
    transposition: Interval = Interval(0, 0)


all_csv = []
for instrument in [
        Instrument("ocarina_pendant", Note("C4"), Note("E5")),
        Instrument("ocarina_harmony_triple", Note("A4"), Note("E♭6")),
        Instrument("ocarina_transverse", Note("C4"), Note("C6")),
        Instrument("mv_ocarina", Note("B3"), Note("E5")),
        Instrument("saxophone", Note("B♭3"), Note("A6")),
        Instrument("tin_whistle", Note("D4"), Note("D6")),
        Instrument("recorder", Note("C4"), Note("D6"), Interval(chromatic=2, diatonic=1)),
        Instrument("harmonica_diatonic", Note("C3"), Note("C6")),
        Instrument("harmonica_chromatic", Note("C3"), Note("C7#")),
    ]:
    instrument_image = f"""<img src="{instrument}.png"/>"""
    csv_path = f"{folder_path}/{instrument}.csv"
    notes = []
    for patterns, specific in ((chords, "Arpeggio"), (scale_patterns, "Scale"), ):
        for scale_pattern in patterns:
            scale_name = scale_pattern.names[0]
            for set_of_enharmonic_keys in sets_of_enharmonic_keys:
                bass_key = set_of_enharmonic_keys[0] + instrument.transposition - scale_pattern.interval_for_signature
                bass_note = bass_key.note
                while bass_note < instrument.lowest_instrument_note:
                    bass_note = bass_note.add_octave(1)
                while bass_note >= instrument.lowest_instrument_note.add_octave(1):
                    bass_note = bass_note.add_octave(-1)
                tonic_name = bass_note.get_symbol_name()
                note = []
                notes.append(note)
                note.append(f"{instrument} {scale_name.replace(",", "")} {bass_note.get_full_name()}") # key
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

    csv = "\n".join(",".join(note) for note in notes)
    all_csv += notes
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
