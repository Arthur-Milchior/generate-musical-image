
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Type
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList, PositionOnFrettedInstrumentType
from instruments.fretted_instrument.position.set.abstract_set_of_fretted_instrument_positions import AbstractSetOfFrettedPositions
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class SetOfPositionOnFrettedInstrument(AbstractSetOfFrettedPositions[PositionOnFrettedInstrument], ABC):
    # Must be implemented by subclasses
    type: ClassVar[Type[PositionOnFrettedInstrument]] = PositionOnFrettedInstrument
    _frozen_list_type: ClassVar[Type[FrozenList[PositionOnFrettedInstrumentType]]] = PositionOnFrettedInstrumentFrozenList

    def _svg_name_base(self, **kwargs) -> str:
        return NotImplemented
    
class SetOfPositionsOnFrettedInstrumentFrozenList(FrozenList[SetOfPositionOnFrettedInstrument]):
    type = SetOfPositionOnFrettedInstrument


def empty_set_of_position(instrument: FrettedInstrument):
    assert_typing(instrument, FrettedInstrument)
    return SetOfPositionOnFrettedInstrument.make([])