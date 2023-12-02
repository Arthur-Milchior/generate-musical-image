"""
generates pair on note on distinct string. Show 6 frets in the images.
Generate an anki note, with this image, and the distance between both strings, assuming one of the fret is 0
"""
import guitar.util
from guitar.pos import Pos, SetOfPos
from solfege.interval.intervalmode import TEXT
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
    pos1 = Pos(string, pos)
    pos2 = Pos(string_, pos_)
    sop = SetOfPos(set([pos1, pos2]))
    dif = (pos2 - pos1).get_number()
    difString = f"+{dif:d}" if dif > 0 else str(dif)
    fileName = f"{string:d}{pos:d}-{string_:d}{pos_:d}.svg"
    with open(f"{imageFolder}{fileName}", "w") as f:
        sop.draw(f, nbFretMin=6)
    if (pos <= 1 or pos_ <= 1):
        name = (pos2 - pos1).get_interval_name(usage=TEXT)
        if pos and pos_:
            anki += f"""strings {string:d} and {string_:d},{fileName},{name},{difString}\n"""
        else:
            string_name = str(string) if pos else f"{string:d} open"
            string_name_ = str(string_) if pos_ else f'{string_:d} open'
            anki0 += f"""strings {string_name} and {string_name_},{fileName},{name},{difString}\n"""


for string in range(1, 6):
    for string_ in range(string + 1, 7):
        for pos in range(first_fret, last_fret + 1):
            for pos_ in range(first_fret, last_fret + 1):
                generate_for_strings_and_pos(string, string_, pos, pos_)
with open(ankiFolder + "/anki.csv", "w") as f:
    f.write(anki)
    f.write(anki0)