
from dataclasses import dataclass
from typing import ClassVar, Optional, Type
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentType
from instruments.fretted_instrument.position.fretted_instrument_position_with_fingers import PositionOnFrettedInstrumentWithFingers, FrettedInstrumentPositionWithFingersFrozenList
from instruments.fretted_instrument.position.set.abstract_set_of_fretted_instrument_positions import COLOR_FIFTH, COLOR_UNINTERESTING, COLOR_QUALITY, COLOR_THIRD, COLOR_TONIC, AbstractSetOfFrettedPositions, Colors, ColorsWithTonic
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.frozenlist import FrozenList
from utils.util import assert_typing

@dataclass(frozen=True)
class ScaleColors(ColorsWithTonic):
    #pragma mark - Colors
    name: ClassVar[str] = "scale_colors"

    #pragma mark - ColorsWithTonic
    def get_color_from_interval(self, chromatic_interval: ChromaticInterval):
        color = [COLOR_TONIC, 
         COLOR_UNINTERESTING, COLOR_UNINTERESTING,
         COLOR_THIRD, COLOR_THIRD,
         COLOR_UNINTERESTING,
         COLOR_FIFTH, COLOR_FIFTH, COLOR_FIFTH,
         COLOR_UNINTERESTING, COLOR_QUALITY, COLOR_QUALITY][chromatic_interval.in_base_octave().value]
        assert_typing(color, str)
        return color
        
@dataclass(frozen=True, eq=False)
class SetOfFrettedInstrumentPositionsWithFingers(AbstractSetOfFrettedPositions[PositionOnFrettedInstrumentWithFingers]):
    type: ClassVar[Type[PositionOnFrettedInstrument]] = PositionOnFrettedInstrumentWithFingers
    _frozen_list_type: ClassVar[Type[FrozenList[PositionOnFrettedInstrumentType]]] = FrettedInstrumentPositionWithFingersFrozenList

    

class SetOfFrettedInstrumentPositionsWithFingersFrozenList(FrozenList[SetOfFrettedInstrumentPositionsWithFingers]):
    type = SetOfFrettedInstrumentPositionsWithFingers