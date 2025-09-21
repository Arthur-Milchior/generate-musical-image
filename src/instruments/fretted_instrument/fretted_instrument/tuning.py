
import copy
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional, Tuple

from instruments.fretted_instrument.position.fret.fret_deltas import FretDelta
from solfege.value.note.chromatic_note import ChromaticNoteFrozenList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_optional_typing, assert_typing


@dataclass(frozen=True)
class Tuning(DataClassWithDefaultArgument):
    open_string_chromatic_note: ChromaticNoteFrozenList
    _name: Optional[str] = None
    
    def string(self, index):
        from instruments.fretted_instrument.position.string.string import String
        assert_typing(index, int)
        # String 1 is at position 0 in the array, and so on. So removing 1 to index.
        return String(index, self.open_string_chromatic_note[index-1])
    
    def strings(self):
        from instruments.fretted_instrument.position.string.string import StringFrozenList
        from instruments.fretted_instrument.position.string.strings import Strings
        return Strings.make((self.string(index) for index in range(1, len(self.open_string_chromatic_note)+1)))
    
    def number_of_strings(self):
        return len(self.open_string_chromatic_note)
    
    def last_string(self):
        return self.string(self.number_of_strings())
    
    def pair_of_string_with_distinct_intervals(self) -> Generator[Tuple[int, int]]:
        intervals = set()
        for lower_index, lower_note in enumerate(self.open_string_chromatic_note):
            lowest_string = self.string(lower_index+1)
            for higher_index, higher_note in enumerate(self.open_string_chromatic_note):
                higher_string = self.string(higher_index+1)
                if lower_index >= higher_index:
                    continue
                interval = higher_note - lower_note
                if interval in intervals:
                    continue
                intervals.add(interval)
                yield lowest_string, higher_string

    # pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "open_string_chromatic_note", ChromaticNoteFrozenList)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_name", type=str)
        return super()._clean_arguments_for_constructor(args, kwargs)
    
    def __post_init__(self):
        assert_optional_typing(self._name, str)
        assert_typing(self.open_string_chromatic_note, ChromaticNoteFrozenList)
        super().__post_init__()