from dataclasses import dataclass
from typing import ClassVar, Type
from instruments.fretted_instrument.chord.chord_on_fretted_instrument import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.chromatic_inversion_instantiation_and_its_chords import ChromaticInversionInstantiationAndItsChords
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern_instantiation.inversion.chromatic_inversion_instantiation import ChromaticInversionInstantiation
from utils.recording.record_keeper import RecordKeeper
from utils.util import assert_typing


@dataclass(frozen=True)
class ChromaticInversionInstantiationToChords(RecordKeeper[ChromaticInversionInstantiation, ChordOnFrettedInstrument, ChromaticInversionInstantiationAndItsChords]):
    """A `RecordKeeper` mapping each `ChromaticInversionInstantiation` (a chord pattern/inversion anchored to a
    specific chromatic note) to a `ChromaticInversionInstantiationAndItsChords` collecting every way to finger
    that chord on `instrument`. Built and populated by `AnkiNotesPreparation.register_all_chords` in
    `generate_chords.py`."""

    instrument: FrettedInstrument
    """The instrument the chords are played on."""

    #pragma mark - RecordKeeper
    """Same as RecordedType"""
    _recorded_type: ClassVar[Type] = ChordOnFrettedInstrument
    """Same as KeyType"""
    _key_type: ClassVar[Type] = ChromaticInversionInstantiation
    """Same as RecordedContainerType"""
    _recorded_container_type: ClassVar[Type] = ChromaticInversionInstantiationAndItsChords
    """The container class instantiated to hold the chords recorded for each key."""

    def is_key_valid(self, key: ChromaticInversionInstantiation) -> bool:
        """Whether the key is a valid entry. assert if not."""
        assert_typing(key, ChromaticInversionInstantiation, exact=True)
        return True

    def _new_container(self, key: ChromaticInversionInstantiation) -> ChromaticInversionInstantiationAndItsChords:
        """Create the (initially empty) container that will collect chords registered under `key`."""
        return ChromaticInversionInstantiationAndItsChords(instrument=self.instrument, key=key)
