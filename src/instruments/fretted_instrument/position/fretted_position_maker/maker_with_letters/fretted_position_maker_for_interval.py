
from dataclasses import dataclass
from typing import Dict, List, Tuple
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_with_letters import FrettedPositionMakerWithLetter
from solfege.pattern.solfege_pattern import SolfegePattern
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import IntervalList
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_typing


@dataclass(frozen=True)
class FrettedPositionMakerForInterval(FrettedPositionMakerWithLetter):
    """A `FrettedPositionMakerWithLetter` that labels each position with its interval role (e.g. "3m", "5",
    "T") relative to `tonic`, as defined by `pattern` (the scale/chord being drawn)."""
    tonic: ChromaticNote
    """The reference note (scale/chord root) that interval labels are computed relative to."""
    pattern: SolfegePattern
    """The scale/chord pattern whose interval roles supply the text label for each degree."""

    #pragma mark - FrettedPositionMakerForInterval
    def text(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument) -> str:
        """The interval-role label (e.g. "3m", "5", "T") for `pos`'s note relative to `tonic`, looked up in
        `pattern`'s first interval list by matching base-octave interval value. Asserts if no matching interval
        is found in the pattern."""
        chromatic_note = pos.get_chromatic()
        chromatic_interval = chromatic_note - self.tonic
        value_of_interval_in_base_octave = chromatic_interval.in_base_octave().value
        intervals = self.pattern.get_interval_lists()
        full_interval = intervals[0]
        assert_typing(full_interval, IntervalList)
        for interval_in_pattern in full_interval.absolute_intervals():
            assert_typing(interval_in_pattern, Interval)
            assert interval_in_pattern.is_in_base_octave(accepting_octave=False)
            chromatic_interval_in_pattern = interval_in_pattern.get_chromatic()
            assert chromatic_interval_in_pattern.is_in_base_octave(accepting_octave=False)
            if chromatic_interval_in_pattern.value == value_of_interval_in_base_octave:
                return interval_in_pattern.get_role().text_for_guitar_image()
        assert False
#        return ["1", "2m", "2M", "3m", "3M", "4", "T", "5", "6m", "6M", "7m", "7M"][chromatic_interval.in_base_octave().value]
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Normalize constructor arguments: make positional `tonic` a keyword argument."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "tonic")
        return args, kwargs

    def __post_init__(self) -> None:
        """Validate that `tonic` is a `ChromaticNote` within the base octave."""
        assert_typing(self.tonic, ChromaticNote)
        assert self.tonic.is_in_base_octave(accepting_octave=False)
        super().__post_init__()