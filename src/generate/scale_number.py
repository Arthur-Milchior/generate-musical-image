

from collections.abc import Generator
from dataclasses import dataclass
from typing import ClassVar

from solfege.pattern.scale.scale_pattern import ScalePattern
from utils.csv import CsvGenerator
from utils.util import ensure_folder, save_file
from consts import generate_root_folder

"""Generates the "scale number" reference CSV: one Anki row per scale/arpeggio pattern, giving its intervals
(relative and absolute, increasing and decreasing) and per-diatonic-degree alteration notation. See
`generate/README.md`.
"""

# Ensure scales are generated
from solfege.pattern.scale.arpeggio_pattern import *
from solfege.pattern.scale.scale_patterns import *
from solfege.pattern.chord.chord_patterns import *
from solfege.value.interval.diatonic_interval import DiatonicInterval
from solfege.value.interval.interval_alteration import IntervalAlteration



@dataclass
class AnkiNote(CsvGenerator):
    """One Anki row describing a single scale/arpeggio pattern's interval structure."""

    scale: ScalePattern
    """The pattern this row describes."""

    max_number_of_names: ClassVar[int] = 1
    """Running max, across every `AnkiNote` built so far, of how many names a single pattern has — updated as a
    side effect of `csv_content()`, and printed at the bottom of this module so the Anki note type can be sized
    to fit the widest case."""

    def csv_content(self) -> Generator[str]:
        """Yield this row's CSV fields, in order: increasing/decreasing relative and absolute interval lists,
        one alteration field per diatonic degree, the pattern's notation, three blank fields, up to 6 name
        fields (padded with blanks), and an `"x"` marker if the pattern is a chord. Also updates
        `max_number_of_names` as a side effect."""
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
        """The scale's chromatic intervals between consecutive notes, as plain ints."""
        return [interval.value
                for interval in self.scale.get_chromatic_interval_list().relative_intervals()]

    def _chromatic_absolute_list(self):
        """The scale's chromatic intervals from the tonic, as plain ints, excluding the unison (0) and octave
        (12) endpoints."""
        # Removing the first and last element which are 0 and 12.
        return [interval.value
                for interval in self.scale.get_chromatic_interval_list().absolute_intervals()][1:-1]

    def _absolute_list(self):
        """The scale's (diatonic) intervals from the tonic, excluding the unison and octave endpoints."""
        # Removing the first and last element which are 0 and 12.
        return self.scale.get_interval_list().absolute_intervals()[1:-1]

    def increasing_relative_field(self):
        """Comma-separated chromatic step sizes, tonic to octave."""
        return ", ".join(str(value) for value in self._chromatic_relative_list())

    def decreasing_relative_field(self):
        """Comma-separated chromatic step sizes, octave down to tonic."""
        return ", ".join(str(value) for value in reversed(self._chromatic_relative_list()))

    def increasing_absolute_field(self):
        """Comma-separated interval notations from the tonic, ascending."""
        return ", ".join(interval.notation() for interval in self._absolute_list())

    def decreasing_absolute_field(self):
        """Comma-separated interval notations from the octave, descending (each interval expressed as its
        distance down from the octave)."""
        return ", ".join((Interval.unison().add_octave(1) -interval).notation() for interval in reversed(self._absolute_list()))

anki_notes = []
for scale_pattern in ScalePattern.all_patterns:
    anki_note = AnkiNote(scale_pattern)
    csv_content = anki_notes.append(anki_note.csv())

scale_folder = f"{generate_root_folder}/scale"

ensure_folder(scale_folder)

save_file(f"{scale_folder}/relative_scales.csv", "\n".join(anki_notes))

print(AnkiNote.max_number_of_names)