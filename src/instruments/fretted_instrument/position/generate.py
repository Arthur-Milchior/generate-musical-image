
from consts import generate_root_folder
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.black_only import BlackOnly
from utils.util import ensure_folder, save_file
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import fretted_instruments
"""Generate a file for each position."""



for instrument in fretted_instruments:
    folder_path = f"{instrument.generated_folder_name()}/positions"
    ensure_folder(folder_path)
    for fret_value in range(0, instrument.last_fret().value + 1):
        for string in instrument.strings():
            pos = PositionOnFrettedInstrument(string, Fret.make(fret_value, True))
            file_name = f"{folder_path}/{pos.singleton_diagram_svg_name(instrument)}"
            svg = pos.singleton_diagram_svg(instrument, fretted_position_maker=BlackOnly())
            save_file(file_name, svg)