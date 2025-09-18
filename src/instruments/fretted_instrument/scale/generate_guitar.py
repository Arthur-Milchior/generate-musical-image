from dataclasses import dataclass
from typing import Generator
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar, fretted_instruments
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import ScaleColors, SetOfFrettedInstrumentPositionsWithFingers
from instruments.fretted_instrument.scale.generate_scale import generate_scale
from solfege.pattern.solfege_pattern import SolfegePattern
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
class ScaleOnGuitarAnkiNote(CsvGenerator):
    """

    """
    scale_pattern: ScalePattern
    # note 3 and 4 are the same. One octave higher than note 1. This ensure that 
    # if we generate a scale starting on note 3 and 4 and it's the same pattern than a two-octave scale on note 1, the actual positions are the same. 
    string_1_pos = PositionOnFrettedInstrument.make(Guitar.string(1), 12)
    string_2_pos = PositionOnFrettedInstrument.make(Guitar.string(2), 12)
    string_3_pos = PositionOnFrettedInstrument.make(Guitar.string(3), 14)
    string_4_pos = PositionOnFrettedInstrument.make(Guitar.string(4), 9)

    def __post_init__(self):
        assert_typing(self.scale_pattern, ScalePattern)
    
    def generate_svg(self, scale: SetOfFrettedInstrumentPositionsWithFingers):
        assert_typing(scale, SetOfFrettedInstrumentPositionsWithFingers)
        scale, transposition = scale.transpose_to_fret_one()
        first_note = scale.get_most_grave_note().get_chromatic()
        folder_path = f"{scale_transposable_folder}/{self.scale_pattern.first_of_the_names()}"
        ensure_folder(folder_path)
        return scale.save_svg(folder_path=folder_path, instrument=Guitar, absolute=False, colors = ScaleColors(first_note))

    #Pragma mark - CsvGenerator

    def csv_content(self) -> Generator[str]:
        names = list(self.scale_pattern.names)
        first_name = names.pop(0)
        yield first_name
        yield ", ".join(names)

        two_octaves_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=2).best_for_each_finger()
        avoid = {two_octave_scale for two_octave_scale in two_octaves_scales if two_octave_scale is not None}

        first_string_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).best_for_each_finger()

        def keep_chord_with_fifth_string(chord: SetOfFrettedInstrumentPositionsWithFingers):
            return 5 in [pos.string.value for pos in chord]

        second_string_scales = generate_scale(Guitar, self.string_2_pos, self.scale_pattern, number_of_octaves=1, filter=keep_chord_with_fifth_string, pattern_to_avoid_list=avoid).all_scales()
        # The only case where it's interesting to start on second string without repeating the first string is if we end on string 5
        best_second_string_scale_with_fifth_string = None
        if second_string_scales:
            fingers, best_second_string_scale_with_fifth_string = second_string_scales[0]
            # assert 4 in fingers: 
            # Actually, by going lower then higher we can still start with finger 1 and ends up on fret 5.
            # I doubt this lead to interesting to play scale, but let's generate it just to see. Many will probably end up being deleted.
                #continue

        third_string_scales = generate_scale(Guitar, self.string_3_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).best_for_each_finger()

        fourth_string_scales = generate_scale(Guitar, self.string_4_pos, self.scale_pattern, number_of_octaves=1,pattern_to_avoid_list=avoid).best_for_each_finger()
        # assert fourth_string_scale_fourth_finger is None
        # Pentatonic major starting on fourth fret four finger would work. Not the most natural finger selection. But the assertion would be false

        potential_scales: List[Optional[SetOfFrettedInstrumentPositionsWithFingers]] = [*two_octaves_scales, *first_string_scales, best_second_string_scale_with_fifth_string, *third_string_scales, *fourth_string_scales] 
        for scale in potential_scales:
            if scale is None:
                yield ""
                continue
            file_name = self.generate_svg(scale)
            yield img_tag(file_name)

def generate_guitar():
    anki_notes = []
    for scale_pattern in ScalePattern.all_patterns:
        print(f"Generating {scale_pattern.first_of_the_names()}")
        anki_note = ScaleOnGuitarAnkiNote(scale_pattern)
        anki_notes.append(anki_note.csv())

    save_file(f"{scale_transposable_folder}/anki.csv", "\n".join(anki_notes))

generate_guitar()