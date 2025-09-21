from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.consts import CIRCLE_RADIUS, CIRCLE_STROKE_WIDTH, FONT_SIZE, MARGIN, STROKE_WIDTH
from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.colored_position_from_note import Colors
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from utils.svg.svg_atom import svg_circle, svg_text
from utils.util import assert_iterable_typing, assert_typing



    

# @dataclass(frozen=True)
# class ConditionalFrettedPositionMaker(FrettedPositionMaker):
#     colors_for_selected_note: FrettedPositionMaker
#     selected_notes: ChromaticNoteList
#     colors_for_non_selected_notes: FrettedPositionMaker

#     # pragma mark - Colors

#     def __str__(self):
#         return f"{self.__class__.__name__}_with_tonic_{self.colors_for_selected_note.tonic}_restricted_to_intervals_[{"_".join(str(interval.value) for interval in self.colored_intervals)}])"
    

#     def _svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
#         fretted_position_maker = self.colors_for_selected_note if pos.get_chromatic().in_base_octave() in self.selected_notes else self.colors_for_non_selected_notes
#         return fretted_position_maker.svg_content(instrument, pos)

#     # def get_color_from_note(self, chromatic_note: ChromaticNote):
#     #     interval = chromatic_note - self.fretted_position_maker.tonic
#     #     if interval.in_base_octave() not in self.colored_intervals:
#     #         return "black"
#     #     return self.fretted_position_maker.get_color_from_interval(interval)
    
#     def __post_init__(self):
#         assert self.selected_notes.is_in_base_octave()
