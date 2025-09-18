from dataclasses import dataclass
from typing import ClassVar, Type
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.transposable.identical_inversion_pattern_and_its_transposable_chords import IdenticalInversionPatternAndItsTransposableChords
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from utils.recordable import RecordKeeper
from utils.util import assert_typing


@dataclass(frozen=True)
class IdenticalInversionPatternToItsTransposableChords(RecordKeeper[IdenticalInversionPatterns, ChordOnFrettedInstrument, IdenticalInversionPatternAndItsTransposableChords]):
    instrument: FrettedInstrument

    #pragma mark - RecordKeeper
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = IdenticalInversionPatterns
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = IdenticalInversionPatternAndItsTransposableChords

    def is_key_valid(self, key: IdenticalInversionPatterns) -> bool:
        """Whether the key is a valid entry. assert if not."""
        assert_typing(key, IdenticalInversionPatterns, exact=True)
        return True

    def _new_container(self, key: IdenticalInversionPatterns) -> IdenticalInversionPatternAndItsTransposableChords:
        return IdenticalInversionPatternAndItsTransposableChords(instrument=self.instrument, key=key)
