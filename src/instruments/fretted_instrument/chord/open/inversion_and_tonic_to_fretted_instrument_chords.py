from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type

from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.open.inversion_and_tonic_and_its_fretted_instrument_chords import InversionAndTonicAndItsFrettedInstrumentChords
from instruments.fretted_instrument.chord.open.inversion_and_tonic import InversionAndTonic
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from utils.recordable import RecordKeeper
from utils.util import assert_typing




@dataclass(frozen=True)
class InversionAndTonicToFrettedInstrumentChord(RecordKeeper[InversionAndTonic, ChordOnFrettedInstrument, InversionAndTonicAndItsFrettedInstrumentChords]):
    instrument: FrettedInstrument
    _pattern_type: ClassVar[Type] = ChordOnFrettedInstrument
    _pattern_with_chromatic_note_type: ClassVar[Type] = InversionAndTonicAndItsFrettedInstrumentChords
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = InversionAndTonic
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = InversionAndTonicAndItsFrettedInstrumentChords

    def _new_container(self, chromatic_note_list: InversionAndTonic) -> InversionAndTonicAndItsFrettedInstrumentChords:
        chromatic_interval_list = chromatic_note_list.interval_list_from_min_note()
        chromatic_interval_list_in_base_octave = chromatic_interval_list.in_base_octave()
        chromatic_interval_and_inversions = InversionPattern.get_record_keeper().get_from_chromatic_interval_list(chromatic_interval_list_in_base_octave)
        assert_typing(chromatic_interval_and_inversions, ChromaticIntervalListAndItsInversions)
        return InversionAndTonicAndItsFrettedInstrumentChords.make(instrument=self.instrument, lowest_note = min(chromatic_note_list), interval_and_its_inversions=chromatic_interval_and_inversions)

    def is_key_valid(self, key: InversionAndTonic):
        return key.tonic.in_base_octave() == key.tonic

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument", type=FrettedInstrument)
        return super()._clean_arguments_for_constructor(args, kwargs)