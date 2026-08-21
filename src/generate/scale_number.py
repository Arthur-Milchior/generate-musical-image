

from collections.abc import Generator
from dataclasses import dataclass
from typing import ClassVar

from solfege.pattern.scale.scale_pattern import ScalePattern
from utils.csv import CsvGenerator
from utils.util import ensure_folder, save_file
from consts import generate_root_folder


# Ensure scales are generated
from solfege.pattern.scale.arpeggio_pattern import *
from solfege.pattern.scale.scale_patterns import *
from solfege.pattern.chord.chord_patterns import *



@dataclass
class AnkiNote(CsvGenerator):
    scale: ScalePattern
    max_number_of_names: ClassVar[int] = 1

    def csv_content(self) -> Generator[str]:
        yield self.increasing_field()
        yield self.decreasing_field()
        for diatonicInterval in range(7):
            yield ", ".join(self.scale.get_interval_list().alterations_from_diatonic(diatonicInterval)) or "None"
        notations = [*self.scale.notations]
        while len(notations) < 4:
            notations.append("")
        yield from notations
        notations = [*self.scale.notations]
        while len(names) < 6:
            names.append("")
        yield from names
        AnkiNote.max_number_of_names = max(AnkiNote.max_number_of_names, len(self.scale.names))

    def _chromatic_list(self):
        return [interval.value 
                for interval in self.scale.get_chromatic_interval_list().relative_intervals()]
    
    def increasing_field(self):
        return ", ".join(str(value) for value in self._chromatic_list())
    
    def decreasing_field(self):
        return ", ".join(str(value) for value in reversed(self._chromatic_list()))

anki_notes = []
for scale_pattern in ScalePattern.all_patterns:
    anki_note = AnkiNote(scale_pattern)
    csv_content = anki_notes.append(anki_note.csv())

scale_folder = f"{generate_root_folder}/scale"

ensure_folder(scale_folder)

save_file(f"{scale_folder}/relative_scales.csv", "\n".join(anki_notes))

print(AnkiNote.max_number_of_names)