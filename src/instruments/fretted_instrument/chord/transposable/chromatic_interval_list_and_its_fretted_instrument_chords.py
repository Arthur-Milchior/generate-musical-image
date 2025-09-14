
# from dataclasses import dataclass
# from typing import ClassVar
# from instruments.fretted_instrument.chord.chromatic_list_and_its_fretted_instrument_chords import ChromaticListAndItsFrettedInstrumentChords
# from solfege.pattern.chord.inversion_pattern import InversionPattern
# from solfege.value.interval.chromatic_interval import ChromaticInterval
# from utils.util import img_tag


# @dataclass(frozen=True, unsafe_hash=True)
# class ChromaticIntervalListAndItsFrettedInstrumentChords(ChromaticListAndItsFrettedInstrumentChords[ChromaticInterval]):
#     """
#     Csv is:
#     name, other name, open ("), for chord (1, 2, 3, 4, 5, 6, 7, remaining): (the chord black, chord colored, partition)
#     """
#     open: ClassVar[bool] = False
#     absolute: ClassVar[bool] = False

#     def name(self, inversion: InversionPattern):
#         return inversion.name()
    
#     def lily_field(self, *arg, **kwargs) -> str:
#         return ""