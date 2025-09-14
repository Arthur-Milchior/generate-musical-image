
from typing import ClassVar, Type

from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalType
from solfege.value.interval.set.interval_list_pattern import AbstractIntervalListPattern, ChromaticIntervalListPattern
from solfege.value.note.abstract_note import AbstractNote
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from solfege.value.note.set.abstract_note_list import AbstractNoteList
from utils.frozenlist import FrozenList


class ChromaticNoteList(AbstractNoteList[ChromaticNote, ChromaticInterval, ChromaticIntervalListPattern]):
    note_type: ClassVar[Type[AbstractNote]] = ChromaticNote
    interval_list_type: ClassVar[Type[AbstractIntervalListPattern]] = ChromaticIntervalListPattern
    _frozen_list_type: ClassVar[Type[FrozenList[AbstractNote]]] = ChromaticNoteFrozenList

    def __repr__(self):
        return f"""ChromaticNoteList.make([{", ".join(str(note.value) for note in self)}])"""