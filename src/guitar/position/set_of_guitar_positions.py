from __future__ import annotations
from dataclasses import dataclass

import itertools
from pickle import EMPTY_SET
from typing import FrozenSet, Generator, Iterable, List, Iterator, Optional, Tuple, Union

from guitar.position.guitar_position import GuitarPosition
from guitar.position.fret import NOT_PLAYED, OPEN_FRET, Fret
from guitar.position.consts import *
from guitar.position.strings import ALL_STRINGS
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.list import ChromaticIntervalList, IntervalList
from solfege.value.note.chromatic_note import ChromaticNote
from utils.util import assert_dict_typing, assert_increasing, assert_iterable_typing, assert_optional_typing, assert_typing, sorted_unique
from guitar.position.string import strings

COLOR_TONIC = "red"
COLOR_THIRD = "blue"
COLOR_FIFTH = "grey"
COLOR_QUALITY = "green"
COLOR_OTHER = "purple"

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

    def get_most_grave_note(self) -> Optional[GuitarPosition]:
        """The guitar position of the lowest note"""
        return min(self.positions) if self.positions else None

    def add(self, position: GuitarPosition):
        """A set similar to `self`, with `position`"""
        return self.__class__(self.positions | frozenset({position}))

    def __iter__(self) -> Iterator[GuitarPosition]:
        return iter(sorted(self.positions))

    def __eq__(self, other: SetOfGuitarPositions):
        assert_typing(other, SetOfGuitarPositions)
        return set(self.positions) == set(other.positions)

    def _max_fret(self) -> Fret :
        """The greatest fret used."""
        return max(position.fret for position in self.positions) if self.positions else NOT_PLAYED
    
    def _min_fret(self) -> Fret :
        """The lowest fret used."""
        return min(position.fret for position in self.positions) if self.positions else NOT_PLAYED
    
    def _min_non_empty_fret(self) -> Fret :
        """The lowest fret used."""
        frets = [position.fret for position in self.positions]
        closed_strings = [fret for fret in frets if fret not in (NOT_PLAYED, OPEN_FRET)]
        return min(closed_strings) if closed_strings else NOT_PLAYED
    
    def last_shown_fret(self, add_one: bool = True):
        mf = self._max_fret()
        if add_one:
            return mf.below()
        return mf
    
    def height(self, add_one: bool = True):
        assert self.positions
        return self.last_shown_fret(add_one).y_fret() + MARGIN
    
    def svg_content(self, absolute: bool, colors: bool, nbFretMin: Fret =OPEN_FRET, add_empty_fret: bool = True):
        max_fret = max(self.last_shown_fret(add_empty_fret ), nbFretMin).below()
        l = ["""<rect width="100%" height="100%" fill="white" />"""]
        l += ALL_STRINGS.svg(lowest_fret=max_fret, show_open_fret=absolute)
        l += max_fret.all_frets_up_to_here(include_open=absolute).svg(absolute)
        color_and_poss: List[Tuple[str, List[GuitarPosition]]] = [
            (COLOR_TONIC, self.get_tonics()),
            (COLOR_THIRD, self.get_thirds()),
            (COLOR_FIFTH, self.get_fifths()),
            (COLOR_QUALITY, self.get_quality()),
            (COLOR_OTHER, self.get_other()),
            ]
        for (color, poss) in color_and_poss:
            l += [pos.svg(color if colors else "black") for pos in poss]
        return l

    def chromatic_notes(self) -> FrozenSet[ChromaticNote]:
        """return the set of note (i.e. no repetition)"""
        chromatic_notes = [pos.get_chromatic() for pos in self]
        chromatic_notes = [note for note in chromatic_notes if note is not None]
        assert_iterable_typing(chromatic_notes, ChromaticNote)
        return sorted_unique(chromatic_notes)

    def intervals_frow_lowest_note(self) -> Optional[IntervalList]:
        """Return None if there are no note played."""
        lowest_position = self.get_most_grave_note()
        lowest_note = lowest_position.get_chromatic()
        chromatic_notes = self.chromatic_notes()
        if lowest_note is None:
            return None
        for chromatic_note in chromatic_notes:
            assert lowest_note <= chromatic_note
        assert_iterable_typing(chromatic_notes, ChromaticNote)
        assert_optional_typing(lowest_note, ChromaticNote)
        chromatic_intervals = frozenset(chromatic_note - lowest_note for chromatic_note in chromatic_notes)
        assert_iterable_typing(chromatic_intervals, ChromaticInterval)
        return ChromaticIntervalList.make_absolute(sorted_unique(chromatic_intervals))

    def intervals_frow_lowest_note_in_base_octave(self):
        intervals = self.intervals_frow_lowest_note()
        if intervals is None:
            return None
        absolute_chromatic_intervals = intervals.absolute_intervals()
        assert_iterable_typing(absolute_chromatic_intervals, ChromaticInterval)
        return ChromaticIntervalList.make_absolute(sorted_unique(interval.in_base_octave() for interval in absolute_chromatic_intervals))

    def svg(self, absolute:bool, stroke_colored: bool, nbFretMin: Fret=OPEN_FRET) -> str:
        new_line = "\n"
        return f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="{int(WIDTH)}" height="{int(self.height(add_one=True))}" version="1.1">
{new_line.join(("  "+ content) for content in self.svg_content(absolute, stroke_colored, nbFretMin, add_empty_fret=True))}
</svg>"""
    
    def __lt__(self, other: SetOfGuitarPositions):
        return set(self.positions) < set(other.positions)
    
    def number_of_distinct_notes(self):
        return len(self.chromatic_notes())
    
    def get_specific_role(self, tonic: ChromaticNote, roles: Iterable[Union[ChromaticInterval, int]], assert_unique: bool = True):
        """Get the notes whose interval with tonic belongs in `roles`. If `assert_unique` a single of those role should be present at most.
        E.g. not having both third minor and major."""
        roles = [ChromaticInterval.make_single_argument(role) for role in roles]
        positions: List[GuitarPosition] = []
        found_role = None
        for role in roles:
            positions_at_role = [pos for pos in self if (pos.get_chromatic() - tonic).in_base_octave() in roles]
            if positions_at_role:
                if assert_unique:
                    assert found_role is None, f"{self} has {role} and {found_role}"
                positions += positions_at_role
                found_role = role
        return positions

    def get_tonics(self, tonic: ChromaticNote):
        return self.get_specific_role(tonic, [0])
    
    def get_thirds(self, tonic: ChromaticNote):
        return self.get_specific_role(tonic, [3, 4])
    
    def get_fifths(self, tonic: ChromaticNote):
        return self.get_specific_role(tonic, [6, 7, 8])
    
    def get_quality(self, tonic: ChromaticNote):
        return self.get_specific_role(tonic, [9, 10, 11])
    
    def get_other(self, tonic: ChromaticNote):
        return self.get_specific_role(tonic, [1, 2, 5], assert_unique=False)