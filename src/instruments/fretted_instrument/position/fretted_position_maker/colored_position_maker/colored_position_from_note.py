
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generator

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.positions_consts import CIRCLE_RADIUS, STROKE_WIDTH
from instruments.fretted_instrument.position.fretted_position_maker.fretted_position_maker import FrettedPositionMaker
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.value.note.chromatic_note import ChromaticNote
from utils.svg.svg_atom import svg_circle


@dataclass(frozen=True)
class Colors(FrettedPositionMaker):

    def svg_lines(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        stroke_color = self.get_color_from_note(pos.get_chromatic())
        fill_color = "white" if pos.fret.is_open() else (stroke_color)
        if pos.fret.is_not_played():
            yield from pos.string.svg_for_x(pos.fret.absolute)
            return
        x = pos.string.x()
        y = pos.fret.y_dots()
        yield f"""{svg_circle(int(x), int(y), int(CIRCLE_RADIUS), fill_color, stroke_color, STROKE_WIDTH)}<!-- String N° {pos.string.value}, position {pos.fret.value}-->"""


    # Must be implemented by subclasses
    @abstractmethod
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:...