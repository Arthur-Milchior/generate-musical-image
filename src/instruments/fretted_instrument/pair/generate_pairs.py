
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.pair.generate_fretted_instrument_interval import FrettedInstrumentIntervalAnkiNote, pairs_of_frets_values
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.string.string import String
from utils.util import ensure_folder, save_file


def anki_note_(instrument: FrettedInstrument, low_string: String, high_string: String, low_fret: Fret, high_fret: Fret):
    assert low_string < high_string
    return FrettedInstrumentIntervalAnkiNote(instrument,
        PositionOnFrettedInstrument(low_string, low_fret,),
        PositionOnFrettedInstrument(high_string, high_fret,),
        )

def generate_instrument(instrument: FrettedInstrument, folder_path:str):
    anki_notes = []
    number_of_strings = instrument.number_of_strings()
    for low_string, high_string in instrument.pair_of_string_with_distinct_intervals():
        assert low_string < high_string
        for (low_fret, high_fret) in pairs_of_frets_values(instrument.max_distance_between_two_closed_frets()):
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