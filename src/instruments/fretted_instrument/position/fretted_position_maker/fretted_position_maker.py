
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from utils.data_class_with_default_argument import DataClassWithDefaultArgument


@dataclass(frozen=True)
class FrettedPositionMaker(DataClassWithDefaultArgument, ABC):
    """Base class for the strategies that draw one played `PositionOnFrettedInstrument` (a dot on a fretboard
    diagram, possibly with a color and/or a text label) as SVG. Subclasses vary in how they pick the dot's color
    (see `colored_position_maker/`) and whether they add letter/finger labels (see `maker_with_letters/`)."""

    def svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument):
        """The full SVG content for `pos` (currently just `svg_lines`; kept separate as the hook for an
        eventual per-style `<style>` block, see the commented-out code below)."""
        # class_to_style = self.style()
        # if style:
        #     yield "<style>"
        #     yield from style
        #     yield "</style>"
        yield from self.svg_lines(instrument, pos)

    @abstractmethod
    def svg_lines(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        """Yield the SVG line(s) drawing `pos` on `instrument`. Implemented by subclasses."""
        ...

    @abstractmethod
    def __str__(self) -> str:
        """A short identifier for this maker, used when naming generated files."""
        ...