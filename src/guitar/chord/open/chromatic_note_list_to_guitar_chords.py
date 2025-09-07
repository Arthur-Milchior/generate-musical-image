from dataclasses import dataclass
from typing import ClassVar, Type

from guitar.chord.guitar_chord import GuitarChord
from guitar.chord.open.chromatic_note_list_and_its_guitar_chords import ChromaticNoteListAndItsGuitarChords
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.interval_list_to_inversion_pattern import get_chromatic_intervals_and_inversions
from solfege.value.note.set.note_list import ChromaticNoteList
from utils.recordable import RecordKeeper
from utils.util import assert_typing


class ChromaticNoteListToGuitarChords(RecordKeeper[ChromaticNoteList, GuitarChord, ChromaticNoteListAndItsGuitarChords]):
    _pattern_type: ClassVar[Type] = GuitarChord
    _pattern_with_chromatic_note_type: ClassVar[Type] = ChromaticNoteListAndItsGuitarChords
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = GuitarChord
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticNoteList
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticNoteListAndItsGuitarChords

    def _new_container(self, chromatic_note_list: ChromaticNoteList) -> ChromaticNoteListAndItsGuitarChords:
        chromatic_interval_list = chromatic_note_list.interval_list_from_min_note()
        chromatic_interval_list_in_base_octave = chromatic_interval_list.in_base_octave()
        chromatic_interval_and_inversions = get_chromatic_intervals_and_inversions(chromatic_interval_list_in_base_octave)
        assert_typing(chromatic_interval_and_inversions, ChromaticIntervalListAndItsInversions)
        return ChromaticNoteListAndItsGuitarChords.make(lowest_note = min(chromatic_note_list), interval_and_its_inversions=chromatic_interval_and_inversions)