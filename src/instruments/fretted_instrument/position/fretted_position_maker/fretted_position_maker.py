
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from utils.data_class_with_default_argument import DataClassWithDefaultArgument


@dataclass(frozen=True)
class FrettedPositionMaker(DataClassWithDefaultArgument, ABC):
    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument):
        # class_to_style = self.style()
        # if style:
        #     yield "<style>"
        #     yield from style
        #     yield "</style>"
        yield from self.svg_lines(instrument, pos)

    @abstractmethod
    def svg_lines(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:...

    @abstractmethod
    def __str__(self) -> str: ...