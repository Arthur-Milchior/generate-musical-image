"""
generates pair on note on distinct string. Show 6 frets in the images.
Generate an anki note, with this image, and the distance between both strings, assuming one of the fret is 0
"""
import guitar.util
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set_of_positions import SetOfGuitarPositions
from utils.util import *

leafFolder = "pair/"
imageFolder = guitar.util.imageFolder + leafFolder
ankiFolder = guitar.util.ankiFolder + leafFolder
max_fret_distante = 4

first_fret = 0
last_fret = 6

ensure_folder(imageFolder)
ensure_folder(ankiFolder)
anki = ""
anki0 = ""

def generate_for_strings_and_pos(lower_string, higher_string, pos_of_lower_string, pos_of_higher_string):
    global anki, anki0
    assert 1<=lower_string<higher_string<=6
    pos1 = GuitarPosition(lower_string, pos_of_lower_string)
    pos2 = GuitarPosition(higher_string, pos_of_higher_string)
    chromatic1 = pos1.get_chromatic()
    chromatic2 = pos2.get_chromatic()
    sop = SetOfGuitarPositions(set([pos1, pos2]))
    interval = chromatic2 - chromatic1
    dif = interval.get_number()
    difString = f"+{int(dif)}" if dif > 0 else str(dif)
    fileName = f"{int(lower_string)}{int(pos_of_lower_string)}-{int(higher_string)}{int(pos_of_higher_string)}.svg"
    with open(f"{imageFolder}{fileName}", "w") as f:
        f.write(sop.svg(nbFretMin=6))
    if (pos_of_lower_string <= 1 or pos_of_higher_string <= 1):
        name = interval.get_interval_name()
        if pos_of_lower_string and pos_of_higher_string:
            anki += f"""strings {int(lower_string)} and {int(higher_string)},{fileName},{name},{difString}\n"""
        else:
            string_name = str(lower_string) if pos_of_lower_string else f"{int(lower_string)} open"
            string_name_ = str(higher_string) if pos_of_higher_string else f'{int(higher_string)} open'
            anki0 += f"""strings {string_name} and {string_name_},{fileName},{name},{difString}\n"""


for lower_string in range(1, 6):
    for higher_string in range(lower_string + 1, 7):
        for pos_of_lower_string in range(first_fret, last_fret + 1):
            for pos_of_higher_string in range(first_fret, last_fret + 1):
                generate_for_strings_and_pos(lower_string, higher_string, pos_of_lower_string, pos_of_higher_string)
with open(ankiFolder + "/anki.csv", "w") as f:
    f.write(anki)
    f.write(anki0)