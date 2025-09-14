from dataclasses import dataclass
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Bass
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import ScaleColors, SetOfFrettedInstrumentPositionsWithFingers
from instruments.fretted_instrument.scale.generate_scale import generate_scale
from solfege.pattern.pattern import SolfegePattern
from utils.csv import CsvGenerator
from utils.util import *
from solfege.pattern.scale.scale_pattern import ScalePattern
from consts import generate_root_folder

# Ensure scales are generated
from solfege.pattern.scale.arpeggio_pattern import *
from solfege.pattern.scale.scale_patterns import *
from solfege.pattern.chord.chord_patterns import *


scale_transposable_folder = f"{generate_root_folder}/bass/scale/transposable"
ensure_folder(scale_transposable_folder)


@dataclass(frozen=True)
class ScaleOnBassAnkiNote(CsvGenerator):
    """

    """
    scale_pattern: ScalePattern
    # note 3 and 4 are the same. One octave higher than note 1. This ensure that 
    # if we generate a scale starting on note 3 and 4 and it's the same pattern than a two-octave scale on note 1, the actual positions are the same. 
    start_pos = PositionOnFrettedInstrument.make(Bass.string(1), 12)

    def __post_init__(self):
        assert_typing(self.scale_pattern, ScalePattern)

    def csv_content(self) -> List[str]:
        l = []
        names = list(self.scale_pattern.names)
        first_name = names.pop(0)
        l.append(first_name)
        l.append(", ".join(names))

        scales = generate_scale(Bass, self.start_pos, self.scale_pattern, number_of_octaves=1).all_scales()
        scale_tags = []
        for fingers, scale in scales:
            file_name = self.generate_svg(scale)
            scale_tags.append(img_tag(file_name))
        l+=scale_tags[:min(3, len(scale_tags))]
        if len(scale_tags) >3: 
            l.append(", ".join(scale_tags[3:]))
        else:
            l.append("")
        return l
    
    def generate_svg(self, scale: SetOfFrettedInstrumentPositionsWithFingers):
        assert_typing(scale, SetOfFrettedInstrumentPositionsWithFingers)
        scale, tranpsosition = scale.transpose_to_fret_one()
        file_name = scale.svg_file_name(Bass, absolute=False)
        svg = scale.svg(Bass, absolute=False, colors = ScaleColors(self.start_pos.get_chromatic()))
        folder_path = f"{scale_transposable_folder}/{self.scale_pattern.first_of_the_names()}"
        path =f"{folder_path}/{file_name}"
        ensure_folder(folder_path)
        save_file(path, svg)
        return file_name

def generate_bass():
    anki_notes = []
    for scale_pattern in ScalePattern.all_patterns:
        print(f"Generating {scale_pattern.first_of_the_names()}")
        anki_note = ScaleOnBassAnkiNote(scale_pattern)
        anki_notes.append(anki_note.csv())

    save_file(f"{scale_transposable_folder}/anki.csv", "\n".join(anki_notes))

generate_bass()