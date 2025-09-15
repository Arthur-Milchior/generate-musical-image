
from dataclasses import dataclass
from typing import ClassVar, Generic, List, Type

from instruments.fretted_instrument.chord.abstract_equivalent_inversion_and_its_fretted_instrument_chords import AbstractEquivalentInversionAndItsFrettedInstrumentChords
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import ChromaticIdenticalInversionPatternGetter, ChromaticIdenticalInversionPatterns
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatternsGetterType, IdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from utils.util import assert_typing



@dataclass(frozen=True, unsafe_hash=True)
class AbstractEquivalentInversionWithoutNoteAndItsFrettedInstrumentChords(AbstractEquivalentInversionAndItsFrettedInstrumentChords[IdenticalInversionPatternsGetterType], Generic[IdenticalInversionPatternsGetterType]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords
    absolute: ClassVar[bool] = False

    def name(self, inversion: InversionPattern) -> List[str]:
        return inversion.name()

    def lily_field(self, *args, **kwargs) -> str:
        # The anki field for the partition if any.
        return ""

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIdenticalInversionPatternAndItsTransposableChords(AbstractEquivalentInversionAndItsFrettedInstrumentChords[ChromaticIdenticalInversionPatterns]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords
    absolute: ClassVar[bool] = False

    identical_inversion_pattern_getter_type: ClassVar[Type[ChromaticIdenticalInversionPatternGetter]] = ChromaticIdenticalInversionPatterns
    
