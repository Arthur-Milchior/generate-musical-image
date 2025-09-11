from dataclasses import dataclass
from fretted_instrument.fretted_instrument.fretted_instruments import Guitar, fretted_instruments
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import ScaleColors, SetOfFrettedInstrumentPositionsWithFingers
from fretted_instrument.scale.generate_scale import generate_scale
from solfege.pattern.pattern import SolfegePattern
from utils.csv import CsvGenerator
from utils.util import *
from solfege.pattern.scale.scale_pattern import ScalePattern
from consts import generate_root_folder

# Ensure scales are generated
from solfege.pattern.scale.arpeggio_pattern import *
from solfege.pattern.scale.scale_patterns import *
from solfege.pattern.chord.chord_patterns import *


scale_transposable_folder = f"{generate_root_folder}/guitar/scale/transposable"
ensure_folder(scale_transposable_folder)


@dataclass(frozen=True)
class AnkiNote(CsvGenerator):
    """

    """
    scale_pattern: ScalePattern
    # note 3 and 4 are the same. One octave higher than note 1. This ensure that 
    # if we generate a scale starting on note 3 and 4 and it's the same pattern than a two-octave scale on note 1, the actual positions are the same. 
    string_1_pos = PositionOnFrettedInstrument.make(1, 12)
    string_2_pos = PositionOnFrettedInstrument.make(3, 12)
    string_3_pos = PositionOnFrettedInstrument.make(3, 14)
    string_4_pos = PositionOnFrettedInstrument.make(4, 9)

    def __post_init__(self):
        assert_typing(self.scale_pattern, ScalePattern)

    def csv_content(self) -> List[str]:
        l = []
        names = list(self.scale_pattern.names)
        first_name = names.pop(0)
        l.append(first_name)
        l.append(", ".join(names))

        two_octaves_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=2).best_for_each_finger()
        avoid = {two_octave_scale for two_octave_scale in two_octaves_scales if two_octave_scale is not None}

        first_string_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).best_for_each_finger()

        second_string_scales = generate_scale(Guitar, self.string_2_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).all_scales()
        # The only case where it's interesting to start on second string without repeating the first string is if we end on string 5
        best_second_string_scale_with_fifth_string: Optional[SetOfFrettedInstrumentPositionsWithFingers] = None
        for fingers, second_string_scale in second_string_scales:
            if 5 in [pos.string.value for pos in second_string_scale.positions]:
                assert 4 in fingers
                best_second_string_scale_with_fifth_string = second_string_scale
                break

        third_string_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).best_for_each_finger()

        fourth_string_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).best_for_each_finger()
        fourth_string_scale_first_finger, fourth_string_scale_middle_finger, fourth_string_scale_fourth_finger = fourth_string_scales
        assert fourth_string_scale_fourth_finger is None

        potential_scales: List[Optional[SetOfFrettedInstrumentPositionsWithFingers]] = [*two_octaves_scales, *first_string_scales, best_second_string_scale_with_fifth_string, *third_string_scales, fourth_string_scale_first_finger, fourth_string_scale_middle_finger] 
        for scale in potential_scales:
            if scale is None:
                l.append("")
                continue
            svg = scale.svg(Guitar, absolute=False)
            file_name = scale.scale_name(absolute=False)
            file_path = f"{scale_transposable_folder}/{file_name}"
            save_file(file_path, svg)
            l.append(img_tag(file_name))
        return l
    
    def generate_svg(self):
        for scales in self._scaless():
            for scale in scales:
                file_name = scale.scale_name(absolute=False)
                svg = scale.svg(absolute=False, colors = ScaleColors(self.string_1_pos.get_chromatic()))
                path =f"{scale_transposable_folder}/{file_name}"
                save_file(path, svg)

def generate_guitar():
    anki_notes = []
    for scale_pattern in ScalePattern.all_patterns:
        print(f"Generating {scale_pattern.first_of_the_names()}")
        anki_note = AnkiNote.make(scale_pattern)
        anki_note.generate_svg()
        anki_notes.append(anki_note.csv())

    save_file(f"{scale_transposable_folder}/anki.csv", "\n".join(anki_notes))

generate_guitar()