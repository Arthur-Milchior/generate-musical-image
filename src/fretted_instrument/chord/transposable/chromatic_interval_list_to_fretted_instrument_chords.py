from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type

from fretted_instrument.chord.transposable.chromatic_interval_list_and_its_fretted_instrument_chords import ChromaticIntervalListAndItsFrettedInstrumentChords
from fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern.chord.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.pattern.chord.interval_list_to_inversion_pattern import ChromaticIntervalListToInversion, IntervalListToInversionPattern, get_chromatic_intervals_and_inversions
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.pattern.chromatic_interval_list_to_patterns import ChromaticIntervalListToPatterns
from solfege.value.interval.set.interval_list import ChromaticIntervalList
from utils.recordable import RecordKeeper
from utils.util import assert_typing


@dataclass(frozen=True)
class ChromaticIntervalListToFrettedInstrumentChords(RecordKeeper[ChromaticIntervalList, ChordOnFrettedInstrument, ChromaticIntervalListAndItsFrettedInstrumentChords]):
    instrument: FrettedInstrument
    _pattern_type: ClassVar[Type] = ChordOnFrettedInstrument
    _pattern_with_chromatic_interval_type: ClassVar[Type] = ChromaticIntervalListAndItsFrettedInstrumentChords
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIntervalList
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticIntervalListAndItsFrettedInstrumentChords

    def _new_container(self, chromatic_interval_list: ChromaticIntervalList) -> ChromaticIntervalListAndItsFrettedInstrumentChords:
        chromatic_intervals_and_inversions = get_chromatic_intervals_and_inversions(chromatic_interval_list)
        assert_typing(chromatic_intervals_and_inversions, ChromaticIntervalListAndItsInversions)
        return ChromaticIntervalListAndItsFrettedInstrumentChords.make(self.instrument, chromatic_intervals_and_inversions)
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument", type=FrettedInstrument)
        return super()._clean_arguments_for_constructor(args, kwargs)