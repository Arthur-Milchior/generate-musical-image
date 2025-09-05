
from consts import generate_root_folder
from utils.util import ensure_folder
from guitar.position.fret import HIGHEST_FRET, Fret
from guitar.position.guitar_position import GuitarPosition
from guitar.position.string import strings

folder_path = f"{generate_root_folder}/guitar/positions"

ensure_folder(folder_path)

for fret_value in range(0, HIGHEST_FRET.value + 1):
    for string in strings:
        pos = GuitarPosition(string, Fret(fret_value))
        save_file(f"{folder_path}/{pos.singleton_diagram_svg_name()}", pos.singleton_diagram_svg())