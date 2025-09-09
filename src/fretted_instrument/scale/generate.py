from dataclasses import dataclass
from fretted_instrument.position.guitar_position import GuitarPosition
from fretted_instrument.position.set.set_of_guitar_positions_with_fingers import ScaleColors, SetOfGuitarPositionsWithFingers
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
    scale_pattern: ScalePattern
    scales_for_two_octave_from_string_one: List[SetOfGuitarPositionsWithFingers]
    scales_for_first_three_strings: List[SetOfGuitarPositionsWithFingers]
    scales_for_middle_three_strings: List[SetOfGuitarPositionsWithFingers]
    scales_for_last_three_strings: List[SetOfGuitarPositionsWithFingers]

    string_1_pos = GuitarPosition.make(1, 12)
    string_3_pos = GuitarPosition.make(3, 12)
    string_4_pos = GuitarPosition.make(4, 12)

    def _scaless(self):
        return (self.scales_for_two_octave_from_string_one, self.scales_for_first_three_strings, self.scales_for_middle_three_strings, self.scales_for_last_three_strings)

    def __post_init__(self):
        assert_typing(self.scale_pattern, ScalePattern)
        assert_iterable_typing(self.scales_for_two_octave_from_string_one, SetOfGuitarPositionsWithFingers)

    @classmethod
    def make(cls, scale_pattern: ScalePattern):
        anki_scale_two_octave = generate_scale(cls.string_1_pos, scale_pattern, 2).all_scales()
        poss = [cls.string_1_pos, cls.string_3_pos, cls.string_4_pos]
        single_octave_scale_list_list = []
        for pos in poss:
            single_octave_scale_list = generate_scale(pos, scale_pattern, 1).all_scales()
            single_octave_scale_list = [scale for scale in single_octave_scale_list if scale not in anki_scale_two_octave]
            single_octave_scale_list_list.append(single_octave_scale_list)
        return cls(scale_pattern, anki_scale_two_octave, *single_octave_scale_list_list)

    def csv_content(self) -> List[str]:
        l = []
        l.append(self.scale_pattern.first_of_the_names())
        for scales in self._scaless():
            number_of_scales = min(3, len(scales))
            number_of_empty_fields = 3 - number_of_scales
            for i in range(number_of_scales):
                scale = scales[i]
                first_position = scale.positions[0]
                first_fingers = first_position.fingers
                l.append(", ".join(str(finger) for finger in first_fingers))
                l.append(img_tag(scale.scale_name(absolute=False)))
            for i in range(number_of_empty_fields):
                l.append("")
                l.append("")
            remaining_scales = scales[3:]
            l.append(", ".join(img_tag(scale.scale_name(absolute=False)) for scale in remaining_scales))
        return l
    
    def generate_svg(self):
        for scales in self._scaless():
            for scale in scales:
                file_name = scale.scale_name(absolute=False)
                svg = scale.svg(absolute=False, colors = ScaleColors(self.string_1_pos.get_chromatic()))
                path =f"{scale_transposable_folder}/{file_name}"
                save_file(path, svg)

anki_notes = []
for scale_pattern in ScalePattern.all_patterns:
    anki_note = AnkiNote.make(scale_pattern)
    anki_note.generate_svg()
    anki_notes.append(anki_note.csv())

save_file(f"{scale_transposable_folder}/anki.csv", "\n".join(anki_notes))