
from dataclasses import dataclass
from typing import ClassVar, Generic, List, Type

from instruments.fretted_instrument.chord.abstract_equivalent_inversion_and_its_fretted_instrument_chords import AbstractIdenticalInversionAndItsFrettedInstrumentChords
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatternGetter, ChromaticIdenticalInversionPatterns
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatternsGetterType, IdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from utils.util import assert_typing



@dataclass(frozen=True, unsafe_hash=True)
class AbstractEquivalentInversionWithoutNoteAndItsFrettedInstrumentChords(AbstractIdenticalInversionAndItsFrettedInstrumentChords[IdenticalInversionPatternsGetterType], Generic[IdenticalInversionPatternsGetterType]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords
    absolute: ClassVar[bool] = False

    def names_from_inversion(self, inversion: InversionPattern) -> List[str]:
        return inversion.names()

    def lily_field(self, *args, **kwargs) -> str:
        # The anki field for the partition if any.
        return ""

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIdenticalInversionPatternAndItsTransposableChords(AbstractIdenticalInversionAndItsFrettedInstrumentChords[ChromaticIdenticalInversionPatterns]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords
    absolute: ClassVar[bool] = False

    identical_inversion_pattern_getter_type: ClassVar[Type[ChromaticIdenticalInversionPatternGetter]] = ChromaticIdenticalInversionPatterns

    # pragma mark - AbstractIdenticalInversionAndItsFrettedInstrumentChords

    def names_from_inversion(self, inversion: InversionPattern) -> List[str]:
        return inversion.names()

    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalListPattern) -> str:
        return ""