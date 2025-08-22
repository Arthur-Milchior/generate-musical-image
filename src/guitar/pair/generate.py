"""
generates pair on note on distinct string. Show 6 frets in the images.
Generate an anki note, with this image, and the distance between both strings, assuming one of the fret is 0
"""
from dataclasses import dataclass
from pickletools import string1
import guitar.util
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from guitar.position.fret import Fret
from guitar.position.string import String, strings
from solfege.interval.chromatic import ChromaticInterval, IntervalNameCreasing
from utils.util import *
from consts import generate_root_folder

"""
Generate an image for each pair of notes between fret 0 and LAST_FRET on distinct string.
Also a card for each note. Used for the card type "guitar interval"
"""


folder_path = f"{generate_root_folder}/guitar/pair"

LAST_FRET = 6

ensure_folder(folder_path)

@dataclass(frozen=True)
class AnkiNote:
    pos1: GuitarPosition
    pos2: GuitarPosition

    def __post_init__(self):
        assert_typing(self.pos1, GuitarPosition)
        assert_typing(self.pos2, GuitarPosition)
        assert self.pos1.fret.value < 2 or self.pos2.fret.value < 2
        assert self.pos1.string < self.pos2.string

    def key(self):
        return f"{self.pos1.string.value}{self.pos1.fret.value}-{self.pos2.string.value}{self.pos2.fret.value}"
    
    def svg_name(self):
        return f"guitar_{self.key()}.svg"
    
    def interval(self):
        return self.pos2 - self.pos1
    
    def pos_difference(self):
        v = self.pos2.fret.value - self.pos1.fret.value
        if v == 0:
            return "=0"
        if v < 0:
           return str(v)
        else:
            return f"+{v}"
        
    def difference_name(self):
        return self.interval().get_interval_name(side = IntervalNameCreasing.DECREASING_ONLY)
    
    def anki_fields(self):
        return [
            self.key(),
            str(self.pos1.string.value),
            str(self.pos2.string.value),
            f"""<img src="{self.svg_name()}"/>""",
            self.pos_difference(),
            str(self.interval().value),
            self.difference_name(),
        ]
    
    def anki_csv(self):
        return ",".join(self.anki_fields())
    
    def svg(self):
        return SetOfGuitarPositions(frozenset({self.pos1, self.pos2})).svg()

def pairs_of_frets_values(last_fret: int):
    return (
    [(low_fret, high_fret) for low_fret in range(0, 2) for high_fret in range (0, last_fret + 1)] +
    [(low_fret, high_fret) for low_fret in range(2, last_fret+1) for high_fret in range (0, 2)]
)

def pair_of_frets(last_fret: int):
    return [(Fret(low_fret), Fret(high_fret)) for (low_fret, high_fret) in pairs_of_frets_values(last_fret)]

def anki_note_(low_string: int, high_string: int, low_fret: Fret, high_fret: Fret):
    return AnkiNote(
        GuitarPosition(strings[low_string-1], low_fret,),
        GuitarPosition(strings[high_string-1], high_fret,),
        )

anki_notes = []
for low_string in range(1, 6):
    for high_string in range(low_string + 1, 7):
        for (low_fret, high_fret) in pair_of_frets(LAST_FRET):
            anki_note = anki_note_(low_string, high_string, low_fret, high_fret)
            with open(f"{folder_path}/{anki_note.svg_name()}", "w") as f:
                f.write(anki_note.svg())
            anki_notes.append(anki_note.anki_csv())

with open(f"{folder_path}/anki.csv", "w") as f:
    f.write("\n".join(anki_notes))