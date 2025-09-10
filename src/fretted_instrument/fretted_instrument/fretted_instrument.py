
import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from solfege.value.note.chromatic_note import ChromaticNoteFrozenList
from solfege.value.note.clef import Clef
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_optional_typing, assert_typing
from consts import generate_root_folder


@dataclass(frozen=True, unsafe_hash=True)
class FrettedInstrument(DataClassWithDefaultArgument):
    name: str
    number_of_frets: int
    open_string_chromatic_note: ChromaticNoteFrozenList
    clef: Clef
    finger_to_fret_delta: Dict[int, Dict[int, "FretDelta"]]=field(compare=False)

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_open_strings(open_strings):
            return ChromaticNoteFrozenList(open_strings)

        args, kwargs = cls.arg_to_kwargs(args, kwargs, "name")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "number_of_frets")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "open_string_chromatic_note", clean_open_strings)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "clef")
        #Copying to ensure we don't modify the input dic
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "finger_to_fret_delta", copy.deepcopy)
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        assert_typing(self.name, str)
        assert_typing(self.number_of_frets, int)
        assert_typing(self.name, str)
        assert_typing(self.clef, Clef)
        from fretted_instrument.position.fret.fret_deltas import FretDelta
        #Change is done here because creating the delta require the instrument.
        for lower in range(4):
            for higher in range (lower+1, 5):
                delta_above, delta_below = self.finger_to_fret_delta[lower][higher]
                self.finger_to_fret_delta[lower][higher] = FretDelta(self, delta_above, delta_below)
                self.finger_to_fret_delta[higher][lower] = -self.finger_to_fret_delta[lower][higher]

        super().__post_init__()

    def string(self, index):
        from fretted_instrument.position.string.string import String
        # String 1 is at position 0 in the array, and so on. So removing 1 to index.
        return String(self, index, self.open_string_chromatic_note[index-1])
    
    def strings(self):
        from fretted_instrument.position.string.string import StringFrozenList
        from fretted_instrument.position.string.strings import Strings
        return Strings.make(self, (self.string(index) for index in range(1, len(self.open_string_chromatic_note)+1)))

    def fret(self, value: Optional[Union[int, "Fret"]]):
        from fretted_instrument.position.fret.fret import Fret
        if isinstance(value, Fret):
            assert value.instrument == self
            return value
        assert_optional_typing(value, int)
        return Fret(value, self)
    
    def number_of_strings(self):
        return len(self.open_string_chromatic_note)

    def last_fret(self):
        return self.fret(self.number_of_frets)
    
    def last_string(self):
        return self.string(self.number_of_strings())

    def lowest_note(self):
        return min(self.open_string_chromatic_note)
    
    def highest_note(self):
        return max(self.open_string_chromatic_note) + self.number_of_frets
    
    def generated_folder_name(self):
        return f"{generate_root_folder}/{self.name}"