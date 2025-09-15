from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from instruments.fretted_instrument.chord.transposable.inversion_pattern_and_its_chords_on_fretted_instrument import InversionPatternAndItsChordsOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.pattern.chord.chord_pattern import ChordPattern
from utils.recordable import RecordKeeper
from utils.util import assert_typing


class ChordPatternToChordsOnFrettedInstrument(RecordKeeper[ChordPattern, ChordOnFrettedInstrument, InversionPatternAndItsChordsOnFrettedInstrument]):
    instrument: FrettedInstrument

    #pragma mark - RecordKeeper

    def is_key_valid(self, key: ChordPattern) -> bool:
        """Whether the key is a valid entry. assert if not."""
        assert_typing(key, ChordPattern)
        return True

    def _new_container(self, key: ChordPattern) -> InversionPatternAndItsChordsOnFrettedInstrument:
        return InversionPatternAndItsChordsOnFrettedInstrument(key)