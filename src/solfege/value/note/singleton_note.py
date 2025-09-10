
from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Generic, Self, Union, overload

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.singleton_interval import AbstractSingletonInterval
from solfege.value.note.abstract_note import AbstractNote
from solfege.value.singleton import Singleton


@dataclass(frozen=True)
class AbstractSingletonNote(AbstractNote[IntervalType], Singleton, Generic[IntervalType]):
    def __add__(self, other: IntervalType) -> Self:
        if isinstance(other, self.IntervalClass):
            return dataclasses.replace(self, value = self.value + other.value)
        return NotImplemented

    def __sub__(self, other: Union[Self, IntervalType]) -> Union[Self, IntervalType]:
        new_value = self.value - other.value
        if isinstance(self, other.__class__):
            return self.IntervalClass(new_value)
        else:
            assert isinstance(other, self.IntervalClass) 
            return dataclasses.replace(self, value = new_value)
        
AbstractSingletonNote.IntervalClass = AbstractSingletonInterval