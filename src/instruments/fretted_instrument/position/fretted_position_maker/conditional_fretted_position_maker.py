
from dataclasses import dataclass
from typing import Generator, List

from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.fretted_position_maker import FrettedPositionMaker
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_iterable_typing, assert_typing


@dataclass(frozen=True)
class ConditionalFrettedPositionMaker(FrettedPositionMaker):
    """A `FrettedPositionMaker` that delegates to one of two other makers depending on whether a position's
    interval above `tonic` (folded into the base octave) is in `selected_intervals` — e.g. to draw compound
    chord extensions in a different style from the rest of the notes (see
    `AbstractSetOfFrettedPositions`/chord generation for the caller that builds this)."""
    maker_for_selected_interval: FrettedPositionMaker
    """The maker used for positions whose interval above `tonic` is in `selected_intervals`."""
    selected_intervals: List[int]
    """The base-octave (0 to 11) interval values that get `maker_for_selected_interval` instead of the default."""
    maker_for_non_selected_intervals: FrettedPositionMaker
    """The maker used for every position not selected by `selected_intervals` (and for unplayed positions)."""
    tonic: ChromaticNote
    """The reference note that intervals are computed relative to."""

    def __post_init__(self) -> None:
        """Validate the types of `maker_for_non_selected_intervals`, `selected_intervals`, and `tonic`."""
        assert_typing(self.maker_for_non_selected_intervals, FrettedPositionMaker)
        assert_iterable_typing(self.selected_intervals, int)
        assert_typing(self.maker_for_non_selected_intervals, FrettedPositionMaker)
        assert_typing(self.tonic, ChromaticNote)

    # def style(self):
    #     yield from self.colors_for_non_selected_intervals.style()
    #     yield from self.colors_for_non_selected_intervals.style()

    def svg_lines(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> Generator[str]:
        """Delegate drawing `pos` to `maker_for_selected_interval` if `pos`'s interval above `tonic` (folded
        into the base octave) is in `selected_intervals`, otherwise to `maker_for_non_selected_intervals`
        (always the latter if `pos` isn't played)."""
        if pos.fret.is_played():
            interval = pos.get_chromatic() - self.tonic if pos.fret.is_played() else None
            fretted_position_maker = self.maker_for_selected_interval if interval.in_base_octave().value in self.selected_intervals else self.maker_for_non_selected_intervals
        else:
            fretted_position_maker = self.maker_for_non_selected_intervals
        yield from fretted_position_maker.svg_content(instrument, pos)

    def __str__(self) -> str:
        """A composite identifier encoding both delegate makers, the tonic, and the selected intervals, used
        when naming generated files."""
        return f"""{str(self.maker_for_selected_interval)}_tonic_{self.tonic.value}_{"-".join(str(interval) for interval in self.selected_intervals)}_{str(self.maker_for_non_selected_intervals)}"""