
from typing import ClassVar, Type

from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalType
from solfege.value.interval.set.interval_list import AbstractIntervalListPattern, ChromaticIntervalListPattern
from solfege.value.note.abstract_note import AbstractNote
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from solfege.value.note.set.abstract_note_list import AbstractNoteList
from utils.frozenlist import FrozenList


class ChromaticNoteList(AbstractNoteList[ChromaticNote, ChromaticInterval, ChromaticIntervalListPattern]):
    """A list of `ChromaticNote`, with no diatonic information."""
    note_type: ClassVar[Type[AbstractNote]] = ChromaticNote
    """The concrete note class this list holds."""
    interval_list_type: ClassVar[Type[AbstractIntervalListPattern]] = ChromaticIntervalListPattern
    """The interval-list-pattern class produced by `interval_list_from_min_note`."""
    _frozen_list_type: ClassVar[Type[FrozenList[AbstractNote]]] = ChromaticNoteFrozenList
    """The `FrozenList` subclass used to store `notes`."""

    def __repr__(self) -> str:
        """Debug representation as a `ChromaticNoteList.make([...])` call."""
        return f"""ChromaticNoteList.make([{", ".join(str(note.value) for note in self)}])"""