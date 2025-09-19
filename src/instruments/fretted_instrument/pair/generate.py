
from instruments.fretted_instrument.fretted_instrument import fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.pair.generate_fretted_instrument_interval import FrettedInstrumentIntervalAnkiNote, pairs_of_frets_values
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from utils.util import ensure_folder, save_file


def pair_of_frets(instrument: FrettedInstrument):
    last_fret = instrument.last_fret()
    return [(Fret(low_fret, True), Fret(high_fret, True)) for (low_fret, high_fret) in pairs_of_frets_values(last_fret)]

def anki_note_(instrument: FrettedInstrument, low_string: int, high_string: int, low_fret: Fret, high_fret: Fret):
    return FrettedInstrumentIntervalAnkiNote(instrument,
        PositionOnFrettedInstrument(instrument.string(low_string), low_fret,),
        PositionOnFrettedInstrument(instrument.string(high_string), high_fret,),
        )

def generate_instrument(instrument: FrettedInstrument, folder_path:str):
    anki_notes = []
    number_of_strings = instrument.number_of_strings()
    for low_string in range(1, number_of_strings):
        for high_string in range(low_string + 1, number_of_strings + 1):
            for (low_fret, high_fret) in pair_of_frets(instrument):
                anki_note = anki_note_(instrument, low_string, high_string, low_fret, high_fret)
                save_file(f"{folder_path}/{anki_note.svg_name()}", anki_note.svg())
                anki_notes.append(anki_note.csv())
    return anki_notes

def generate():
    for instrument in fretted_instruments:
        folder_path = f"{instrument.generated_folder_name()}/pair"
        ensure_folder(folder_path)
        save_file(f"{folder_path}/anki.csv", "\n".join(generate_instrument(instrument, folder_path)))

generate()