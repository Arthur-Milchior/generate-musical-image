
from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Generic, Self, Union, overload

from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.singleton_interval import AbstractSingletonInterval
from solfege.value.note.abstract_note import AbstractNote
from solfege.value.singleton import Singleton


@dataclass(frozen=True)
class AbstractSingletonNote(AbstractNote[IntervalType], Singleton, Generic[IntervalType]):
    """Base for notes represented by a single number (chromatic-only or diatonic-only), as
    opposed to `Note`'s chromatic+diatonic pair."""

    #Pragma mark - AbstractNote

    def __add__(self, other: IntervalType) -> Self:
        """Add an interval of `self.IntervalClass` to this note's value, returning a note of the
        same class."""
        if isinstance(other, self.IntervalClass):
            return dataclasses.replace(self, value = self.value + other.value)
        return NotImplemented

    #Pragma mark - Abstract

    def __sub__(self, other: Union[Self, IntervalType]) -> Union[Self, IntervalType]:
        """Subtract another note of the same class (yielding an interval) or an interval
        (yielding a shifted note of the same class)."""
        new_value = self.value - other.value
        if isinstance(self, other.__class__):
            return self.IntervalClass.make(new_value)
        else:
            assert isinstance(other, self.IntervalClass)
            return dataclasses.replace(self, value = new_value)

AbstractSingletonNote.IntervalClass = AbstractSingletonInterval