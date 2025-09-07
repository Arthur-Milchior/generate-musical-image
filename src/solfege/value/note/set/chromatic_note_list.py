
from typing import ClassVar, Type

from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalType
from solfege.value.interval.set.interval_list import AbstractIntervalList, ChromaticIntervalList
from solfege.value.note.abstract_note import AbstractNote
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.set.abstract_note_list import AbstractNoteList


class ChromaticNoteList(AbstractNoteList[ChromaticNote, ChromaticInterval, ChromaticIntervalList]):
    note_type: ClassVar[Type[AbstractNote]] = ChromaticNote
    interval_list_type: ClassVar[Type[AbstractIntervalList]] = ChromaticIntervalList

    def __repr__(self):
        return f"""ChromaticNoteList.make([{", ".join(str(note.value) for note in self)}])"""