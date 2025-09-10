
from dataclasses import dataclass
from typing import ClassVar, Type
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument, PositionOnFrettedInstrumentFrozenList, PositionOnFrettedInstrumentType
from fretted_instrument.position.set.abstract_set_of_fretted_instrument_positions import AbstractSetOfFrettedPositions
from utils.frozenlist import FrozenList
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class SetOfPositionOnFrettedInstrument(AbstractSetOfFrettedPositions[PositionOnFrettedInstrument]):
    type: ClassVar[Type[PositionOnFrettedInstrument]] = PositionOnFrettedInstrument
    _frozen_list_type: ClassVar[Type[FrozenList[PositionOnFrettedInstrumentType]]] = PositionOnFrettedInstrumentFrozenList

class SetOfPositionsOnFrettedInstrumentFrozenList(FrozenList[SetOfPositionOnFrettedInstrument]):
    type = SetOfPositionOnFrettedInstrument


def empty_set_of_position(instrument: FrettedInstrument):
    assert_typing(instrument, FrettedInstrument)
    return SetOfPositionOnFrettedInstrument.make(instrument, [])