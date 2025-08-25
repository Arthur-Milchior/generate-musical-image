
from dataclasses import dataclass
from typing import Self, Union
from solfege.interval.singleton_interval import AbstractSingletonInterval
from solfege.note.chromatic_note import ChromaticNote
from solfege.note.diatonic_note import DiatonicNote
from solfege.note.singleton_note import AbstractSingletonNote
from solfege.note.with_tonic.abstract import AbstractNoteWithTonic
from solfege.value.abstract import Abstract


@dataclass(frozen=True, eq=False)
class AbstractSingletonNoteWithTonic(AbstractNoteWithTonic, AbstractSingletonNote):
    """A note of the scale, as an interval from middle C."""

    @classmethod
    def make(cls, value: Union[AbstractSingletonNote, int], tonic: Union[AbstractNoteWithTonic, bool]):
        if isinstance(value, AbstractSingletonNote):
            value = value.value 
        return cls(value=value, tonic=tonic)

    def __add__(self, other: AbstractSingletonInterval) -> Self:
        sum = super().__add__(other)
        tonic = self.get_tonic()
        return self.__class__(value = sum.value, tonic=tonic)
