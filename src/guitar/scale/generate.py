from dataclasses import dataclass
from guitar.position.guitar_position import GuitarPosition
from guitar.scale.generate_scale import generate_scale
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
    scale: SolfegePattern

    def csv_content(self) -> List[str]:
        l = []
        return l


max_scale = None
for scale_pattern in ScalePattern.all_patterns:
    anki_scales = generate_scale(GuitarPosition.make(2, 12), scale_pattern, 2)
    if max_scale is None or (len(anki_scales)>len (max_scale)):
        max_scale = anki_scales

print(f"{len(max_scale)=}")
print(f"{max_scale=}")