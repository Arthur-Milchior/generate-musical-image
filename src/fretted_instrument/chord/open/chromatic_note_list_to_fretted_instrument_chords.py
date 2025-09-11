from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type

from fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from fretted_instrument.chord.open.chromatic_note_list_and_its_fretted_instrument_chords import ChromaticNoteListAndItsFrettedInstrumentChords
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.interval_list_to_inversion_pattern import get_chromatic_intervals_and_inversions
from solfege.value.note.set.note_list import ChromaticNoteList
from utils.recordable import RecordKeeper
from utils.util import assert_typing


@dataclass(frozen=True)
class ChromaticNoteListToFrettedInstrumentChords(RecordKeeper[ChromaticNoteList, ChordOnFrettedInstrument, ChromaticNoteListAndItsFrettedInstrumentChords]):
    instrument: FrettedInstrument
    _pattern_type: ClassVar[Type] = ChordOnFrettedInstrument
    _pattern_with_chromatic_note_type: ClassVar[Type] = ChromaticNoteListAndItsFrettedInstrumentChords
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticNoteList
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticNoteListAndItsFrettedInstrumentChords

    def _new_container(self, chromatic_note_list: ChromaticNoteList) -> ChromaticNoteListAndItsFrettedInstrumentChords:
        chromatic_interval_list = chromatic_note_list.interval_list_from_min_note()
        chromatic_interval_list_in_base_octave = chromatic_interval_list.in_base_octave()
        chromatic_interval_and_inversions = get_chromatic_intervals_and_inversions(chromatic_interval_list_in_base_octave)
        assert_typing(chromatic_interval_and_inversions, ChromaticIntervalListAndItsInversions)
        return ChromaticNoteListAndItsFrettedInstrumentChords.make(instrument=self.instrument, lowest_note = min(chromatic_note_list), interval_and_its_inversions=chromatic_interval_and_inversions)
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        return super()._clean_arguments_for_constructor(args, kwargs)