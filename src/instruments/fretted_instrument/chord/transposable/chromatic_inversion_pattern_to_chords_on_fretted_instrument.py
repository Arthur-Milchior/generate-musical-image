
from dataclasses import dataclass
from typing import ClassVar, Type

from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.transposable.chromatic_identical_inversion_pattern_and_its_transposable_chords import ChromaticIdenticalInversionPatternAndItsTransposableChords
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatterns
from utils.recordable import RecordKeeper
from utils.util import assert_typing



@dataclass(frozen=True)
class ChromaticIdenticalInversionPatternToItsTransposableChords(RecordKeeper[ChromaticIdenticalInversionPatterns, ChordOnFrettedInstrument, ChromaticIdenticalInversionPatternAndItsTransposableChords]):
    instrument: FrettedInstrument

    #pragma mark - RecordKeeper
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIdenticalInversionPatterns
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticIdenticalInversionPatternAndItsTransposableChords

    def is_key_valid(self, key: ChromaticIdenticalInversionPatterns) -> bool:
        """Whether the key is a valid entry. assert if not."""
        assert_typing(key, ChromaticIdenticalInversionPatterns, exact=True)
        return True

    def _new_container(self, key: ChromaticIdenticalInversionPatterns) -> ChromaticIdenticalInversionPatternAndItsTransposableChords:
        return ChromaticIdenticalInversionPatternAndItsTransposableChords(instrument=self.instrument, key=key)