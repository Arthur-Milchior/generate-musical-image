
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
    """A set of plain `PositionOnFrettedInstrument` (no finger annotation) — the base concrete instantiation of
    `AbstractSetOfFrettedPositions`, used wherever fingering isn't tracked (e.g. drawing a single note or a
    chord shape without finger numbers)."""
    # Must be implemented by subclasses
    type: ClassVar[Type[PositionOnFrettedInstrument]] = PositionOnFrettedInstrument
    """The element type held in this set: plain `PositionOnFrettedInstrument`."""
    _frozen_list_type: ClassVar[Type[FrozenList[PositionOnFrettedInstrumentType]]] = PositionOnFrettedInstrumentFrozenList
    """The `FrozenList` subclass matching `type`."""


class SetOfPositionsOnFrettedInstrumentFrozenList(FrozenList[SetOfPositionOnFrettedInstrument]):
    """An immutable list of `SetOfPositionOnFrettedInstrument`."""
    type = SetOfPositionOnFrettedInstrument
    """The element type enforced by this `FrozenList`."""


def empty_set_of_position(instrument: FrettedInstrument, absolute: bool) -> SetOfPositionOnFrettedInstrument:
    """An empty `SetOfPositionOnFrettedInstrument` for `instrument`, with the given `absolute` flag."""
    assert_typing(instrument, FrettedInstrument)
    return SetOfPositionOnFrettedInstrument.make([], absolute=absolute)