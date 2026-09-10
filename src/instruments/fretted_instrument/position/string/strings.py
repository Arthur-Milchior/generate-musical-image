from dataclasses import dataclass
from typing import Dict, Generator, Iterable, List, Optional, Self, Tuple

from instruments.fretted_instrument.position.fretted_position_maker.colored_position_maker.constants import DEFAULT_COLOR, SELECTED_STRING_COLOR
from instruments.fretted_instrument.position.string.string import String, StringFrozenList
from instruments.fretted_instrument.position.fret.fret import Fret
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.svg.svg_generator import SvgLines
from utils.util import assert_iterable_typing, assert_typing

@dataclass(frozen=True)
class Strings(DataClassWithDefaultArgument, SvgLines):
    """Represents a set of string of the fretted_instrument."""
    strings: StringFrozenList
    """The strings in this set."""

    @classmethod
    def make_interval(cls, instrument: "FrettedInstrument", lower: String, higher: String) -> Self:
        """All strings on `instrument` between `lower` and `higher` (inclusive)."""
        assert lower <= higher
        return super().make(instrument.string(string) for string in range(lower.value, higher.value+1) )

    def __iter__(self) -> Generator[String]:
        """Iterate over the strings in this set."""
        yield from self.strings

    def __lt__(self, other: Self) -> bool:
        """Strict subset comparison, by the underlying set of strings."""
        return set(self.strings) < set(other.strings)

    def __le__(self, other: Self) -> bool:
        """Subset-or-equal comparison, by the underlying set of strings."""
        return set(self.strings) <= set(other.strings)

    def __eq__(self, other: Self) -> bool:
        """Equal iff the same strings (order-sensitive, since `strings` is a `StringFrozenList`)."""
        assert_typing(other, Strings)
        return self.strings == other.strings

    def pop(self) -> Optional[Tuple[String, "Strings"]]:
        """Returns the first string, the set of strings without this element. Or None if the set is empty."""
        if not self.strings:
            return None
        string = self.strings[0]
        strings = Strings.make(self.strings[1:])
        return (string, strings)

    #pragma mark - SvgLines

    def svg_lines(self,
            lowest_fret: Fret,
            show_open_fret: bool,
            colored_strings: List[String] = list(),
            ) ->Iterable[str]:
        """
        The svg to display the strings.
        If `show_open_fret`, a margin at the top represents the top of the board.
        Otherwise the fret goes over the entire height.
        The fret ends below `lowest_fret` so that it also cover the margin at the bottom.
        """
        assert_typing(lowest_fret, Fret)
        for string in self:
            color = SELECTED_STRING_COLOR if string in colored_strings else None
            yield string.svg_line(lowest_fret, show_open_fret, color)
    
    #pragma mark - DataClassWithDefaultArgument

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Normalize constructor arguments: `strings` becomes a keyword argument, coerced to a `StringFrozenList`."""
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "strings", StringFrozenList)
        return super()._clean_arguments_for_constructor(args, kwargs)

    def __post_init__(self) -> None:
        """Validate that `strings` is a `StringFrozenList` of `String`."""
        assert_typing(self.strings, StringFrozenList)
        assert_iterable_typing(self.strings, String)