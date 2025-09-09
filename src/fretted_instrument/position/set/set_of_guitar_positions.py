
from dataclasses import dataclass
from typing import ClassVar, Type
from fretted_instrument.position.guitar_position import GuitarPosition, GuitarPositionFrozenList, GuitarPositionType
from fretted_instrument.position.set.abstract_set_of_guitar_positions import AbstractSetOfGuitarPositions
from utils.frozenlist import FrozenList


@dataclass(frozen=True, eq=False)
class SetOfGuitarPositions(AbstractSetOfGuitarPositions[GuitarPosition]):
    type: ClassVar[Type[GuitarPosition]] = GuitarPosition
    _frozen_list_type: ClassVar[Type[FrozenList[GuitarPositionType]]] = GuitarPositionFrozenList

class SetOfGuitarPositionsFrozenList(FrozenList[SetOfGuitarPositions]):
    type = SetOfGuitarPositions

empty_set_of_guitar_position = SetOfGuitarPositions.make([])