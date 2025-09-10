from dataclasses import dataclass
from typing import Dict, Generator, List, Self

from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.position.string.string import String, StringFrozenList
from fretted_instrument.position.fret.fret import Fret
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class Strings(DataClassWithDefaultArgument):
    """Represents a set of string of the fretted_instrument."""
    instrument: FrettedInstrument
    strings: StringFrozenList
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_strings(strings):
            if isinstance(strings, StringFrozenList):
                return strings
            l = []
            for string in strings:
                if isinstance(string, String):
                    l.append(string)
                else:
                    assert_typing(string, int)
                    l.append(String(instrument, string))
            return StringFrozenList(l)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        instrument = kwargs["instrument"]
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "strings", clean_strings)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self):
        assert_typing(self.instrument, FrettedInstrument)
        assert_typing(self.strings, StringFrozenList)
        if self.strings:
            first_string = self.strings[0]
            for string in self.strings:
                assert string.instrument == first_string.instrument
        assert_iterable_typing(self.strings, String)

    def __iter__(self):
        yield from self.strings

    def __lt__(self, other: Self):
        return set(self.strings) < set(other.strings)
    
    def __le__(self, other: Self):
        return set(self.strings) <= set(other.strings)
    
    def __eq__(self, other: Self):
        assert_typing(other, Strings)
        return self.strings == other.strings
    
    def svg(self, lowest_fret: Fret, show_open_fret: bool) ->List[str]:
        """
        The svg to display the strings.
        If `show_open_fret`, a margin at the top represents the top of the board.
        Otherwise the fret goes over the entire height.
        The fret ends below `lowest_fret` so that it also cover the margin at the bottom.
        """
        return [string.svg(lowest_fret, show_open_fret) for string in self]

    def pop(self):
        """Returns the first string, the set of strings without this element. Or None if the set is empty."""
        if not self.strings:
            return None
        string = self.strings[0]
        strings = Strings.make(self.instrument, self.strings[1:])
        return (string, strings)