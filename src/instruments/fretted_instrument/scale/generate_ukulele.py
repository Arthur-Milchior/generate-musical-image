from dataclasses import dataclass
from typing import Generator
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Ukulele
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.colors import PositionWithIntervalLetters
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import SetOfFrettedInstrumentPositionsWithFingers
from instruments.fretted_instrument.position.string.string_deltas import StringDelta
from instruments.fretted_instrument.scale.generate_scale import generate_scale
from utils.csv import CsvGenerator
from utils.util import *
from solfege.pattern.scale.scale_pattern import ScalePattern
from consts import generate_root_folder

# Ensure scales are generated
from solfege.pattern.scale.arpeggio_pattern import *
from solfege.pattern.scale.scale_patterns import *
from solfege.pattern.chord.chord_patterns import *


scale_transposable_folder = f"{generate_root_folder}/ukulele/scale/transposable"
ensure_folder(scale_transposable_folder)


@dataclass(frozen=True)
class ScaleOnUkuleleAnkiNote(CsvGenerator):
    """

    """
    scale_pattern: ScalePattern
    # note 3 and 4 are the same. One octave higher than note 1. This ensure that 
    # if we generate a scale starting on note 3 and 4 and it's the same pattern than a two-octave scale on note 1, the actual positions are the same. 
    start_pos = PositionOnFrettedInstrument.make(Ukulele.string(2), Fret(5, absolute=False))

    def __post_init__(self):
        assert_typing(self.scale_pattern, ScalePattern)
    
    def generate_svg(self, scale: SetOfFrettedInstrumentPositionsWithFingers):
        assert_typing(scale, SetOfFrettedInstrumentPositionsWithFingers)
        folder_path = f"{scale_transposable_folder}/{self.scale_pattern.first_of_the_names()}"
        scale, transposition = scale.transpose_to_fret_one()
        first_note = scale.get_most_grave_note().get_chromatic()
        file_name = scale.save_svg(folder_path, instrument=Ukulele, absolute=False, colors=PositionWithIntervalLetters(first_note))
        return file_name

    #Pragma mark - CsvGenerator

    def csv_content(self) -> Generator[str]:
        names = list(self.scale_pattern.names)
        first_name = names.pop(0)
        yield first_name
        yield ", ".join(names)

        scales = generate_scale(Ukulele, self.start_pos, self.scale_pattern, number_of_octaves=1, string_delta=StringDelta.SAME_STRING_OR_GREATER(Ukulele)).all_scales()
        scale_tags = []
        for fingers, scale in scales:
            file_name = self.generate_svg(scale)
            scale_tags.append(img_tag(file_name))
        yield from scale_tags[:min(3, len(scale_tags))]
        if len(scale_tags) >3: 
            yield ", ".join(scale_tags[3:])
        else:
            yield ""

def generate_ukulele():
    anki_notes = []
    for scale_pattern in ScalePattern.all_patterns:
        print(f"Generating {scale_pattern.first_of_the_names()}")
        anki_note = ScaleOnUkuleleAnkiNote(scale_pattern)
        anki_notes.append(anki_note.csv())

    save_file(f"{scale_transposable_folder}/anki.csv", "\n".join(anki_notes))

generate_ukulele()