
from dataclasses import dataclass
from typing import Generator, List

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.fretted_position_maker import FrettedPositionMaker
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_iterable_typing, assert_typing


@dataclass(frozen=True)
class ConditionalFrettedPositionMaker(FrettedPositionMaker):
    maker_for_selected_interval: FrettedPositionMaker
    selected_intervals: List[int]
    maker_for_non_selected_intervals: FrettedPositionMaker
    tonic: ChromaticNote

    def __post_init__(self):
        assert_typing(self.maker_for_non_selected_intervals, FrettedPositionMaker)
        assert_iterable_typing(self.selected_intervals, int)
        assert_typing(self.maker_for_non_selected_intervals, FrettedPositionMaker)
        assert_typing(self.tonic, ChromaticNote)

    # def style(self):
    #     yield from self.colors_for_non_selected_intervals.style()
    #     yield from self.colors_for_non_selected_intervals.style()

    def _svg_content(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        if pos.fret.is_played():
            interval = pos.get_chromatic() - self.tonic if pos.fret.is_played() else None
            fretted_position_maker = self.maker_for_selected_interval if interval.in_base_octave().value in self.selected_intervals else self.maker_for_non_selected_intervals
        else:
            fretted_position_maker = self.maker_for_non_selected_intervals
        yield from fretted_position_maker.svg_content(instrument, pos)
    
    def __str__(self):
        return f"""{str(self.maker_for_selected_interval)}_tonic_{self.tonic.value}_{"-".join(str(interval) for interval in self.selected_intervals)}_{str(self.maker_for_non_selected_intervals)}"""