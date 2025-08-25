
from dataclasses import dataclass
from typing import ClassVar, List
from solfege.note.diatonic_note import DiatonicNote
from solfege.note.with_tonic.singleton import AbstractSingletonNoteWithTonic


@dataclass(frozen=True, eq=False)
class DiatonicNoteWithTonic(AbstractSingletonNoteWithTonic, DiatonicNote):
    # Saved as the interval from middle C
    role: ClassVar[List[str]] = ["tonic", "supertonic", "mediant", "subdominant", "dominant", "submediant", "leading"]


