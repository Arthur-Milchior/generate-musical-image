from dataclasses import dataclass
from typing import ClassVar, Generator
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_for_interval import FrettedPositionMakerForInterval
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import SetOfFrettedInstrumentPositionsWithFingers
from instruments.fretted_instrument.scale.anki_scale import generate_scale
from solfege.pattern.solfege_pattern import SolfegePattern
from utils.csv import CsvGenerator
from utils.util import *
from solfege.pattern.scale.scale_pattern import ScalePattern
from consts import generate_root_folder

# Ensure scales are generated
from solfege.pattern.scale.arpeggio_pattern import *
from solfege.pattern.scale.scale_patterns import *
from solfege.pattern.chord.chord_patterns import *


scale_transposable_folder = f"{Guitar.generated_folder_name()}/scale/transposable"
ensure_folder(scale_transposable_folder)


@dataclass(frozen=True)
class ScaleOnGuitarAnkiNote(CsvGenerator):
    """Anki note for one scale/arpeggio pattern on guitar: gathers the best fingerings starting from each of
    four reference positions (covering strings 1 to 4, and both one- and two-octave forms) and renders a
    diagram for each."""
    scale_pattern: ScalePattern
    """The scale/arpeggio pattern this note is generated for."""
    # note 3 and 4 are the same. One octave higher than note 1. This ensure that
    # if we generate a scale starting on note 3 and 4 and it's the same pattern than a two-octave scale on note 1, the actual positions are the same.
    string_1_pos: ClassVar[PositionOnFrettedInstrument] = PositionOnFrettedInstrument.make(Guitar.string(1), Fret.make(12, absolute=False))
    """Fixed reference position (string 1, 12th fret) used as the transposition anchor for the string-1 fingering."""
    string_2_pos: ClassVar[PositionOnFrettedInstrument] = PositionOnFrettedInstrument.make(Guitar.string(2), Fret.make(12, absolute=False))
    """Fixed reference position (string 2, 12th fret) used as the transposition anchor for the string-2 fingering."""
    string_3_pos: ClassVar[PositionOnFrettedInstrument] = PositionOnFrettedInstrument.make(Guitar.string(3), Fret.make(14, absolute=False))
    """Fixed reference position (string 3, 14th fret) used as the transposition anchor for the string-3 fingering."""
    string_4_pos: ClassVar[PositionOnFrettedInstrument] = PositionOnFrettedInstrument.make(Guitar.string(4), Fret.make(9, absolute=False))
    """Fixed reference position (string 4, 9th fret) used as the transposition anchor for the string-4 fingering."""

    def __post_init__(self) -> None:
        """Validate that `scale_pattern` has the right type."""
        assert_typing(self.scale_pattern, ScalePattern)

    def generate_svg(self, scale: SetOfFrettedInstrumentPositionsWithFingers) -> str:
        """Transpose `scale` to start at fret one, resolve its fingering, render it, and return the saved
        SVG's file name."""
        assert_typing(scale, SetOfFrettedInstrumentPositionsWithFingers)
        scale, transposition = scale.transpose_to_fret_one()
        first_note = scale.get_most_grave_note().get_chromatic()
        folder_path = f"{scale_transposable_folder}/{self.scale_pattern.first_of_the_names()}"
        ensure_folder(folder_path)
        maker = FrettedPositionMakerForInterval.make(tonic=first_note.in_base_octave(), pattern=self.scale_pattern)
        scale = scale.resolve_fingers(Guitar)
        return scale.save_svg(folder_path=folder_path, instrument=Guitar, absolute=False, fretted_position_maker = maker)

    #Pragma mark - CsvGenerator

    def csv_content(self) -> Generator[str]:
        """Yield the Anki fields: primary name, remaining names, then one diagram image (or an empty field)
        for each candidate fingering: the best-per-finger two-octave scales from string 1, the best-per-finger
        one-octave scales from string 1, the best one-octave scale from string 2 that also touches string 5,
        and the best-per-finger one-octave scales from strings 3 and 4."""
        names = list(self.scale_pattern.names)
        first_name = names.pop(0)
        yield first_name
        yield ", ".join(names)

        two_octaves_scales = generate_scale(Guitar, self.string_1_pos, self.scale_pattern, number_of_octaves=2).best_for_each_finger()
        avoid = {two_octave_scale for two_octave_scale in two_octaves_scales if two_octave_scale is not None}

        first_string_scales = generate_scale(
            Guitar, 
            self.string_1_pos,
            self.scale_pattern, 
            number_of_octaves=1,
            #pattern_to_avoid_list=avoid # uncomment if you want to avoid having one scale being a subset of two scales
            ).best_for_each_finger()

        def keep_scale_with_fifth_string(scale: SetOfFrettedInstrumentPositionsWithFingers) -> bool:
            """Filter predicate: keep only scales that include a position on string 5."""
            return 5 in [pos.string.value for pos in scale]

        second_string_scales = generate_scale(Guitar, self.string_2_pos, self.scale_pattern, number_of_octaves=1, filter=keep_scale_with_fifth_string, pattern_to_avoid_list=avoid).all_scales()
        # The only case where it's interesting to start on second string without repeating the first string is if we end on string 5
        best_second_string_scale_with_fifth_string = None
        if second_string_scales:
            fingers, best_second_string_scale_with_fifth_string = second_string_scales[0]
            # assert 4 in fingers: 
            # Actually, by going lower then higher we can still start with finger 1 and ends up on fret 5.
            # I doubt this lead to interesting to play scale, but let's generate it just to see. Many will probably end up being deleted.
                #continue

        third_string_scales = generate_scale(
            Guitar, 
            self.string_3_pos, 
            self.scale_pattern, 
            number_of_octaves=1,
            #pattern_to_avoid_list=avoid
            ).best_for_each_finger()

        fourth_string_scales = generate_scale(
            Guitar, 
            self.string_4_pos, 
            self.scale_pattern, 
            number_of_octaves=1,
            #pattern_to_avoid_list=avoid
            ).best_for_each_finger()
        # assert fourth_string_scale_fourth_finger is None
        # Pentatonic major starting on fourth fret four finger would work. Not the most natural finger selection. But the assertion would be false

        potential_scales: List[Optional[SetOfFrettedInstrumentPositionsWithFingers]] = [
            *two_octaves_scales, 
            *first_string_scales, 
            best_second_string_scale_with_fifth_string, 
            *third_string_scales, 
            *fourth_string_scales] 
        for scale in potential_scales:
            if scale is None:
                yield ""
                continue
            file_name = self.generate_svg(scale)
            yield img_tag(file_name)

def generate_guitar() -> None:
    """Generate the Anki notes (and diagrams) for every registered scale/arpeggio pattern on guitar, and
    save them as a CSV."""
    anki_notes = []
    for scale_pattern in ScalePattern.all_patterns:
        print(f"Generating {scale_pattern.first_of_the_names()}")
        anki_note = ScaleOnGuitarAnkiNote(scale_pattern)
        anki_notes.append(anki_note.csv())

    save_file(f"{scale_transposable_folder}/guitar_scales.csv", "\n".join(anki_notes))

generate_guitar()