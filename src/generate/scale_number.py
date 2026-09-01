

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
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval_alteration import IntervalAlteration



@dataclass
class AnkiNote(CsvGenerator):
    scale: ScalePattern
    max_number_of_names: ClassVar[int] = 1

    def csv_content(self) -> Generator[str]:
        yield self.increasing_relative_field()
        yield self.decreasing_relative_field()
        yield self.increasing_absolute_field()
        yield self.decreasing_absolute_field()
        for diatonicInterval in range(7):
            yield ", ".join(alteration.Name() for alteration in self.scale.get_interval_list().alterations_from_diatonic(DiatonicInterval.make(diatonicInterval))) or ""
        yield self.scale.notation or ""
        yield ""
        yield ""
        yield ""
        names = [*self.scale.names]
        while len(names) < 6:
            names.append("")
        yield from names
        yield "x" if self.scale._is_chord_pattern else ""
        AnkiNote.max_number_of_names = max(AnkiNote.max_number_of_names, len(self.scale.names))

    def _chromatic_relative_list(self):
        return [interval.value 
                for interval in self.scale.get_chromatic_interval_list().relative_intervals()]

    def _chromatic_absolute_list(self):
        # Removing the first and last element which are 0 and 12.
        return [interval.value 
                for interval in self.scale.get_chromatic_interval_list().absolute_intervals()][1:-1]
    
    def _absolute_list(self):
        # Removing the first and last element which are 0 and 12.
        return self.scale.get_interval_list().absolute_intervals()[1:-1]
    
    def increasing_relative_field(self):
        return ", ".join(str(value) for value in self._chromatic_relative_list())
    
    def decreasing_relative_field(self):
        return ", ".join(str(value) for value in reversed(self._chromatic_relative_list()))

    def increasing_absolute_field(self):
        return ", ".join(interval.notation() for interval in self._absolute_list())
    
    def decreasing_absolute_field(self):
        return ", ".join((Interval.unison().add_octave(1) -interval).notation() for interval in reversed(self._absolute_list()))

anki_notes = []
for scale_pattern in ScalePattern.all_patterns:
    anki_note = AnkiNote(scale_pattern)
    csv_content = anki_notes.append(anki_note.csv())

scale_folder = f"{generate_root_folder}/scale"

ensure_folder(scale_folder)

save_file(f"{scale_folder}/relative_scales.csv", "\n".join(anki_notes))

print(AnkiNote.max_number_of_names)