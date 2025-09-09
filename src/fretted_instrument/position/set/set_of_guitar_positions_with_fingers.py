
from dataclasses import dataclass
from typing import ClassVar, Type
from fretted_instrument.position.guitar_position import GuitarPosition, GuitarPositionType
from fretted_instrument.position.guitar_position_with_fingers import GuitarPositionWithFingers, GuitarPositionWithFingersFrozenList
from fretted_instrument.position.set.abstract_set_of_guitar_positions import COLOR_FIFTH, COLOR_UNINTERESTING, COLOR_QUALITY, COLOR_THIRD, COLOR_TONIC, AbstractSetOfGuitarPositions, ColorsWithTonic
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.frozenlist import FrozenList
from utils.util import assert_typing



class ScaleColors(ColorsWithTonic):
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
class SetOfGuitarPositionsWithFingers(AbstractSetOfGuitarPositions[GuitarPositionWithFingers]):
    type: ClassVar[Type[GuitarPosition]] = GuitarPositionWithFingers
    _frozen_list_type: ClassVar[Type[FrozenList[GuitarPositionType]]] = GuitarPositionWithFingersFrozenList

    def _scale_name(self, absolute: bool):
        return f"""guitar_scale_{"absolute" if absolute else "transposable"}_{"__".join(f"{pos.string.value}_{pos.fret.value}" for pos in self)}.svg"""

    def scale_name(self, absolute: bool):
        return self.execute_on_maybe_transposed(absolute, lambda poss: poss._scale_name(absolute))

    

class SetOfGuitarPositionsWithFingersFrozenList(FrozenList[SetOfGuitarPositionsWithFingers]):
    type = SetOfGuitarPositionsWithFingers