
from dataclasses import dataclass
from typing import Self, Union
from solfege.value.interval.singleton_interval import AbstractSingletonInterval
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.singleton_note import AbstractSingletonNote
from solfege.value.note.with_tonic.abstract import AbstractNoteWithTonic
from solfege.value.abstract import Abstract
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class AbstractSingletonNoteWithTonic(AbstractNoteWithTonic, AbstractSingletonNote):
    """A note of the scale, as an interval from middle C."""

    @classmethod
    def make(cls,
             value: Union[AbstractSingletonNote, int],
             tonic: Union[AbstractNoteWithTonic, bool]) -> Self:
        if isinstance(value, AbstractSingletonNote):
            value = value.value 
        return cls(value=value, tonic=tonic)

    def _add(self, other: AbstractSingletonInterval) -> Self:
        assert_typing(other, AbstractSingletonInterval)
        sum = super()._add(other)
        tonic = self.get_tonic()
        return self.__class__(value = sum.value, tonic=tonic)
