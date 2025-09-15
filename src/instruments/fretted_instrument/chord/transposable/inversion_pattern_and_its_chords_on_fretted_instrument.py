
from dataclasses import dataclass, field
from typing import ClassVar, List
from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from utils.recordable import RecordedContainer
from utils.util import img_tag


@dataclass(frozen=True, unsafe_hash=True)
class InversionPatternAndItsChordsOnFrettedInstrument(AbstractEquivalentInversionAndItsFrettedInstrumentChords):
    pass