
from dataclasses import dataclass, field
from typing import ClassVar, List, Type
from instruments.fretted_instrument.chord.abstract_equivalent_inversion_and_its_fretted_instrument_chords import AbstractIdenticalInversionAndItsFrettedInstrumentChords
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatternsGetter, IdenticalInversionPatterns
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from utils.recordable import RecordedContainer
from utils.util import img_tag


@dataclass(frozen=True, unsafe_hash=True)
class IdenticalInversionPatternAndItsTransposableChords(AbstractIdenticalInversionAndItsFrettedInstrumentChords[IdenticalInversionPatterns]):
    #pragma mark - AbstractEquivalentInversionAndItsFrettedInstrumentChords

    identical_inversion_pattern_getter_type:ClassVar[Type[IdenticalInversionPatternsGetter]] = IdenticalInversionPatterns

    def names_from_inversion(self, inversion: InversionPattern) -> List[str]:
        return inversion.names()

    def lily_field(self, fretted_instrument_chord : PositionOnFrettedInstrument, interval_list: IntervalListPattern) -> str:
        return ""
    