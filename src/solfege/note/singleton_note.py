
from dataclasses import dataclass
from typing import ClassVar, Self

from solfege.note.abstract_note import AbstractNote
from solfege.value.singleton import Singleton


@dataclass(frozen=True)
class AbstractSingletonNote(AbstractNote, Singleton):
    def _sub_note(self, other: Self):
        return self.IntervalClass(self.value - other.value)
