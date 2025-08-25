from __future__ import annotations
from dataclasses import dataclass

from pickle import EMPTY_SET
from typing import List, Iterator, Optional

from guitar.position.guitar_position import GuitarPosition
from guitar.position.fret import NOT_PLAYED, OPEN_FRET, Fret
from guitar.position.consts import *
from guitar.position.strings import ALL_STRINGS
from utils.util import assert_typing
from guitar.position.string import strings


# def fret_svg(last_fret: Fret) -> List[str]:
#     """The svg for the guitar, with `nb_frets` frets"""
#     svg_lines = []
#     for string in range(1, 7):
#         # columns
#         x = string_distance * (string - .5)
#         y1 = fret_distance / 2
#         y2 = fret_distance * (last_fret.value + .5)
#         svg_lines.append(f"""<line x1="{int(x)}" y1="{int(y1)}" x2="{int(x)}" y2="{int(y2)}" stroke-width="4" stroke="black" />""")
#     for fret in range(1, last_fret.value + 2):
#         # lines
#         x1 = string_distance / 2
#         x2 = string_distance * 5.5
#         y = fret_distance * (fret - .5)
#         svg_lines.append(f"""<line x1="{int(x1)}" y1="{int(y)}" x2="{int(x2)}" y2="{int(y)}" stroke-width="4" stroke="black" />""")
#     return svg_lines


@dataclass(frozen=True)
class SetOfGuitarPositions:
    """
    A set of positions on the guitar.

    There may be 0, 1 or many note by strings.
    Iterated in GuitarPosition order.
    """

    """The set of positions"""
    positions: frozenset[GuitarPosition] = frozenset()


    def __post_init__(self):
        assert_typing(self.positions, frozenset)
        for position in self.positions:
            assert_typing(position, GuitarPosition)

    def get_lowest_note(self) -> Optional[GuitarPosition]:
        """The guitar position of the lowest note"""
        return min(self.positions) if self.positions else None

    def add(self, position: GuitarPosition):
        """A set similar to `self`, with `position`"""
        return SetOfGuitarPositions(self.positions | frozenset({position}))

    def __iter__(self) -> Iterator[GuitarPosition]:
        return iter(sorted(self.positions))

    def __eq__(self, other: SetOfGuitarPositions):
        assert_typing(other, SetOfGuitarPositions)
        return set(self.positions) == set(other.positions)

    def _max_fret(self) -> Fret :
        """The greatest fret used."""
        return max(position.fret for position in self.positions) if self.positions else NOT_PLAYED
    
    def last_shown_fret(self, add_one: bool = True):
        mf = self._max_fret()
        if add_one:
            return mf.below()
        return mf
    
    def height(self, add_one: bool = True):
        assert self.positions
        return self.last_shown_fret(add_one).y_fret() + MARGIN
    
    def svg_content(self, absolute: bool, nbFretMin: Fret =OPEN_FRET, add_empty_fret: bool = True):
        max_fret = max(self.last_shown_fret(add_empty_fret ), nbFretMin).below()
        yield """<rect width="100%" height="100%" fill="white" />"""
        yield from ALL_STRINGS.svg(lowest_fret=max_fret, show_open_fret=absolute)
        yield from max_fret.all_frets_up_to_here(include_open=absolute).svg(absolute)
        for pos in self:
            yield pos.svg()
    

    def svg(self, absolute:bool, nbFretMin: Fret=OPEN_FRET) -> str:
        new_line = "\n"
        return f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="{int(WIDTH)}" height="{int(self.height(add_one=True))}" version="1.1">
{new_line.join(("  "+ content) for content in self.svg_content(absolute, nbFretMin, add_empty_fret=True))}
</svg>"""
    
    def __lt__(self, other: SetOfGuitarPositions):
        return set(self.positions) < set(other.positions)