
from dataclasses import dataclass
from typing import Dict, List
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.fretted_position_maker.maker_with_letters.fretted_position_maker_with_letters import FrettedPositionMakerWithLetter
from solfege.pattern.solfege_pattern import SolfegePattern
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_typing


@dataclass(frozen=True)
class FrettedPositionMakerForInterval(FrettedPositionMakerWithLetter):
    tonic: ChromaticNote
    pattern: SolfegePattern

    #pragma mark - FrettedPositionMakerForInterval
    def text(self, instrument: FrettedInstrument, pos: PositionOnFrettedInstrument):
        chromatic_note = pos.get_chromatic()
        chromatic_interval = chromatic_note - self.tonic
        interval_value_in_base_octave = chromatic_interval.in_base_octave().value
        for interval_in_pattern in self.pattern.absolute_intervals():
            assert interval_in_pattern.is_in_base_octave(accepting_octave=False)
            chromatic_interval_in_pattern = interval_in_pattern.get_chromatic()
            assert chromatic_interval_in_pattern.is_in_base_octave(accepting_octave=False)
            if chromatic_interval_in_pattern.value == interval_value_in_base_octave:
                return interval_in_pattern.get_role().text_for_guitar_image()
        assert False
#        return ["1", "2m", "2M", "3m", "3M", "4", "T", "5", "6m", "6M", "7m", "7M"][chromatic_interval.in_base_octave().value]
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "tonic")
        return args, kwargs
    
    def __post_init__(self):
        assert_typing(self.tonic, ChromaticNote)
        assert self.tonic.is_in_base_octave(accepting_octave=False)
        super().__post_init__()