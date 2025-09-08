from __future__ import annotations
from dataclasses import dataclass

import itertools
from pickle import EMPTY_SET
from typing import Dict, FrozenSet, Generator, Iterable, List, Iterator, Optional, Self, Tuple, Union

from guitar.position.guitar_position import GuitarPosition, GuitarPositionMakeSingleArgumentType
from guitar.position.fret.fret import NOT_PLAYED, OPEN_FRET, Fret
from guitar.position.consts import *
from guitar.position.string.strings import ALL_STRINGS
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from solfege.value.note.set.note_list import NoteList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_dict_typing, assert_increasing, assert_iterable_typing, assert_optional_typing, assert_typing, optional_max, optional_min, sorted_unique
from guitar.position.string.string import String, strings

COLOR_TONIC = "red"
COLOR_THIRD = "blue"
COLOR_FIFTH = "grey"
COLOR_QUALITY = "green"
COLOR_OTHER = "purple"

@dataclass(frozen=True)
class SetOfGuitarPositions(DataClassWithDefaultArgument):
    """
    A set of positions on the guitar.

    There may be 0, 1 or many note by strings.
    Iterated in GuitarPosition order.
    """

    """The set of positions"""
    positions: frozenset[GuitarPosition] = frozenset()

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_positions(positions: Iterable[GuitarPositionMakeSingleArgumentType]):
             return frozenset(GuitarPosition.make_single_argument(position) for position in positions)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "positions", clean_positions)
        return super()._clean_arguments_for_constructor(args, kwargs)
 
    def played_positions(self):
        return frozenset(pos for pos in self.positions if pos.fret.is_played())
    
    def closed_positions(self):
        return frozenset(pos for pos in self.positions if pos.fret.is_closed())

    def __post_init__(self):
        assert_typing(self.positions, frozenset)
        for position in self.positions:
            assert_typing(position, GuitarPosition)

    def get_most_grave_note(self) -> Optional[GuitarPosition]:
        """The guitar position of the lowest note"""
        return optional_min(self.positions)

    def add(self, position: GuitarPositionMakeSingleArgumentType):
        """A set similar to `self`, with `position`"""
        position = GuitarPosition.make_single_argument(position)
        return self.__class__(self.positions | frozenset({position}))

    def __iter__(self) -> Iterator[GuitarPosition]:
        return iter(sorted(self.positions))

    def __eq__(self, other: SetOfGuitarPositions):
        assert_typing(other, SetOfGuitarPositions)
        return set(self.positions) == set(other.positions)
    
    def __lt__(self, other: SetOfGuitarPositions):
        return set(self.positions) < set(other.positions)
    
    def __le__(self, other: SetOfGuitarPositions):
        return set(self.positions) <= set(other.positions)

    def _max_fret(self) -> Optional[Fret] :
        """The greatest fret used."""
        played_positions = self.played_positions()
        return optional_max(position.fret for position in played_positions)
     
    def _min_fret(self, include_open: bool) -> Optional[Fret]:
        """The lowest fret used."""
        if include_open:
            return optional_min(position.fret for position in self.played_positions())
        return optional_min(position.fret for position in self.closed_positions())
    
    def last_shown_fret(self) -> Optional[Fret]:
        return self._max_fret()

    def strings_at_fret(self, fret: Fret):
        return [pos.string for pos in self.positions if pos.fret == fret]
    
    def open_strings(self):
        return self.strings_at_fret(OPEN_FRET)

    def strings_at_min_fret(self, include_open: bool):
        return self.strings_at_fret(self._min_fret(include_open=include_open))
    
    def height(self):
        assert self.positions
        return self.last_shown_fret().y_fret() + MARGIN
    
    def svg_content(self, absolute: bool, tonic: Optional[ChromaticNote], nbFretMin: Fret =OPEN_FRET, add_empty_fret: bool = True):
        assert_optional_typing(tonic, ChromaticNote)
        """If tonic, add some colors depending on the role of the note compared to the tonic"""
        max_fret = max(self.last_shown_fret(add_empty_fret ), nbFretMin).below()
        l = ["""<rect width="100%" height="100%" fill="white" />"""]
        l += ALL_STRINGS.svg(lowest_fret=max_fret, show_open_fret=absolute)
        l += max_fret.all_frets_up_to_here(include_open=absolute).svg(absolute)
        color_and_poss: List[Tuple[str, List[GuitarPosition]]] = [
            (COLOR_TONIC, self.get_tonics(tonic)),
            (COLOR_THIRD, self.get_thirds(tonic)),
            (COLOR_FIFTH, self.get_fifths(tonic)),
            (COLOR_QUALITY, self.get_quality(tonic)),
            (COLOR_OTHER, self.get_other(tonic)),
            ("black", self.get_not_played_positions()),
            ] if tonic else [("black", self.positions)]
        for (color, poss) in color_and_poss:
            l += [pos.svg(absolute, color) for pos in poss]
        return l

    def chromatic_notes(self) -> ChromaticNoteList:
        """return the set of note (i.e. no repetition)"""
        chromatic_notes = [pos.get_chromatic() for pos in self]
        chromatic_notes = [note for note in chromatic_notes if note is not None]
        assert_iterable_typing(chromatic_notes, ChromaticNote)
        return ChromaticNoteList.make(sorted_unique(chromatic_notes))

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

    def svg(self, absolute:bool, tonic: Optional[ChromaticNote]=None, nbFretMin: Fret=OPEN_FRET) -> str:
        new_line = "\n"
        return f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="{int(WIDTH)}" height="{int(self.height())}" version="1.1">
{new_line.join(("  "+ content) for content in self.svg_content(absolute=absolute, tonic=tonic, nbFretMin=nbFretMin, add_empty_fret=True))}
</svg>"""
    
    def number_of_distinct_notes(self):
        return len(self.chromatic_notes())
    
    def get_specific_role(self, tonic: ChromaticNote, roles: Iterable[Union[ChromaticInterval, int]], assert_unique: bool = True):
        """Get the notes whose interval with tonic belongs in `roles`. If `assert_unique` a single of those role should be present at most.
        E.g. not having both third minor and major."""
        assert_typing(tonic, ChromaticNote)
        roles = [ChromaticInterval.make_single_argument(role) for role in roles]
        positions: List[GuitarPosition] = []
        found_role = None
        played_positions = [pos for pos in self if pos.fret.is_played()]
        for role in roles:
            positions_at_role = [pos for pos in played_positions if (pos.get_chromatic() - tonic).in_base_octave() == role]
            if positions_at_role:
                if assert_unique:
                    assert found_role is None, f"{self} has {role} and {found_role}"
                positions += positions_at_role
                found_role = role
        return positions
    
    def get_not_played_positions(self):
        return [pos for pos in self if pos.fret.is_not_played()]

    def get_tonics(self, tonic: ChromaticNote):
        assert_typing(tonic, ChromaticNote)
        return self.get_specific_role(tonic, [0])
    
    def get_thirds(self, tonic: ChromaticNote):
        assert_typing(tonic, ChromaticNote)
        return self.get_specific_role(tonic, [3, 4])
    
    def get_fifths(self, tonic: ChromaticNote):
        assert_typing(tonic, ChromaticNote)
        return self.get_specific_role(tonic, [6, 7, 8])
    
    def get_quality(self, tonic: ChromaticNote):
        assert_typing(tonic, ChromaticNote)
        return self.get_specific_role(tonic, [9, 10, 11])
    
    def get_other(self, tonic: ChromaticNote):
        assert_typing(tonic, ChromaticNote)
        return self.get_specific_role(tonic, [1, 2, 5], assert_unique=False)
    
    def transpose_same_fret(self, transpose: int, transpose_open: bool, transpose_not_played: bool):
        return self.__class__(frozenset(position.transpose_same_fret(transpose, transpose_open, transpose_not_played) for position in self.positions))

    def notes_from_note_list(self, note_list: NoteList):
        """Returns the list of note played, where the diatonic is chosen in order to ensures that the note is octaves apart from an element of note_list"""
        chromatic_notes = self.chromatic_notes()
        return note_list.change_octave_to_be_enharmonic(chromatic_notes)
        
    def notes_from_interval_list(self, interval_list: IntervalList, lowest_note: Optional[Note] = None):
        """Returns the list of note played, where the diatonic is chosen in order to ensures that the note difference between each note and its lowest note belongs (up to octave) in interval_list, and lowest note is `lowest_note`."""
        assert_typing(interval_list, IntervalList)
        if lowest_note is None:
            lowest_note: Note = self.get_most_grave_note().get_chromatic().get_note()
        notes_to_imitate: NoteList = interval_list.from_note(lowest_note)
        return self.notes_from_note_list(notes_to_imitate)