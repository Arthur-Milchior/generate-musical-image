
from dataclasses import dataclass
from typing import Dict, List, Optional

from fretted_instrument.position.string.string import String, bass_A2, guitar_A3, guitar_B4, bass_D3, guitar_D4, bass_E2, guitar_E3, guitar_E5, bass_G3, guitar_G4, StringFrozenList, ukulele_A4, ukulele_C4, ukulele_E4, ukulele_G4
from solfege.value.note.chromatic_note import ChromaticNoteFrozenList
from solfege.value.note.clef import Clef
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_optional_typing, assert_typing


@dataclass(frozen=True)
class FrettedInstrument(DataClassWithDefaultArgument):
    name: str
    number_of_frets: int
    open_string_chromatic_note: ChromaticNoteFrozenList
    clef: Clef

    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_open_strings(open_strings):
            return ChromaticNoteFrozenList.make(open_strings)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "name")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_frets")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "open_string_chromatic_note", clean_open_strings)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "clef")
        return args, kwargs
    
    def __post_init__(self):
        assert_typing(self.name, str)
        assert_typing(self.number_of_frets, int)
        assert_typing(self.name, ChromaticNoteFrozenList)
        assert_typing(self.clef, Clef)
        super().__post_init__()

    def string(self, index):
        return String(index, self.open_string_chromatic_note[index+1], self)
    
    def strings(self):
        return StringFrozenList(self.string(index) for index in range(1, len(self.open_string_chromatic_note)+1))
    
    def number_of_frets(self):
        return len(self.open_string_chromatic_note)



Ukulele = FrettedInstrument.make(
    name= "Ukulele",
    number_of_frets=12, 
    strings= ["G4", "C4", "E4", "A4"],
    clef=Clef.TREBLE,
    )
Guitar = FrettedInstrument(
    name="Guitar",
    number_of_frets=24, 
    strings= ["E3", "A3", "D4", "G4", "B4", "E5"],
    clef=Clef.TREBLE,
    )
Bass = FrettedInstrument(
    name = "Bass",
    number_of_frets=20, 
    strings= ["E2", "A2", "D3", "G3"],
    clef=Clef.BASS,
    )

