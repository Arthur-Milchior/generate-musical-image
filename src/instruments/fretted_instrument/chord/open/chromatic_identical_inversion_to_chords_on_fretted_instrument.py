from dataclasses import dataclass
from typing import ClassVar, Type
from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.open.chromatic_identical_inversion_pattern_with_note_and_its_transposable_chords import ChromaticIdenticalInversionAndItsOpenChords
from instruments.fretted_instrument.chord.transposable.identical_inversion_pattern_and_its_transposable_chords import IdenticalInversionPatternAndItsTransposableChords
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern_instantiation.inversion.chromatic_identical_inversions import ChromaticIdenticalInversions
from solfege.pattern_instantiation.inversion.identical_inversions import IdenticalInversion
from utils.recordable import RecordKeeper
from utils.util import assert_typing


@dataclass(frozen=True)
class ChromaticIdenticalInversionToItsOpenChords(RecordKeeper[ChromaticIdenticalInversions, ChordOnFrettedInstrument, ChromaticIdenticalInversionAndItsOpenChords]):
    instrument: FrettedInstrument

    #pragma mark - RecordKeeper
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticIdenticalInversions
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticIdenticalInversionAndItsOpenChords

    def is_key_valid(self, key: ChromaticIdenticalInversions) -> bool:
        """Whether the key is a valid entry. assert if not."""
        assert_typing(key, ChromaticIdenticalInversions, exact=True)
        return True

    def _new_container(self, key: ChromaticIdenticalInversions) -> ChromaticIdenticalInversionAndItsOpenChords:
        return ChromaticIdenticalInversionAndItsOpenChords(instrument=self.instrument, key=key)
