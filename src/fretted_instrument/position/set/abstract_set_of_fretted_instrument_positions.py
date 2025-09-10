from __future__ import annotations
from dataclasses import dataclass

import dataclasses
import itertools
from pickle import EMPTY_SET
from typing import Callable, ClassVar, Dict, FrozenSet, Generator, Generic, Iterable, List, Iterator, Optional, Self, Tuple, Type, Union

from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from fretted_instrument.fretted_instrument.fretted_instruments import Gui_tar
from fretted_instrument.position.fretted_instrument_position import  PositionOnFrettedInstrumentType
from fretted_instrument.position.fret.fret import Fret
from fretted_instrument.position.consts import *
from fretted_instrument.position.string.strings import Strings
from solfege.value.interval.chromatic_interval import ChromaticInterval, ChromaticIntervalFrozenList
from solfege.value.interval.set.interval_list import ChromaticIntervalList, IntervalList
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList
from solfege.value.note.set.note_list import NoteList
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.frozenlist import FrozenList, MakeableWithSingleArgument
from utils.util import T, assert_dict_typing, assert_increasing, assert_iterable_typing, assert_optional_typing, assert_typing, optional_max, optional_min, sorted_unique
from fretted_instrument.position.string.string import String

COLOR_TONIC = "red"
COLOR_SECOND = "yellow"
COLOR_THIRD = "blue"
COLOR_FOURTH = "orange"
COLOR_FIFTH = "grey"
COLOR_QUALITY = "green"
COLOR_OTHER = "purple"
COLOR_UNINTERESTING = "black"

open_fret = Gui_tar.fret( value=0)

@dataclass(frozen=True)
class Colors:
    def get_color_from_note(self, chromatic_note: ChromaticNote) -> str:
        return NotImplemented

@dataclass(frozen=True)
class ColorsWithTonic(Colors):
    tonic: ChromaticNote

    def __post_init__(self):
        assert_typing(self.tonic, ChromaticNote)

    def get_color_from_interval(self, chromatic_interval: ChromaticInterval) -> str:
        return NotImplemented
    
    def get_color_from_note(self, chromatic_note: ChromaticNote):
        assert_typing(chromatic_note, ChromaticNote)
        return self.get_color_from_interval(chromatic_note - self.tonic)


@dataclass(frozen=True, eq=False, unsafe_hash=True)
class AbstractSetOfFrettedPositions(MakeableWithSingleArgument, DataClassWithDefaultArgument, Generic[PositionOnFrettedInstrumentType]):
    """
    A set of positions on instrument.

    There may be 0, 1 or many note by strings.
    Iterated in PositionOnFrettedInstrument order.
    """

    """The set of positions"""
    instrument: FrettedInstrument
    positions: FrozenList[PositionOnFrettedInstrumentType]
    type: ClassVar[Type[PositionOnFrettedInstrumentType]]
    _frozen_list_type: ClassVar[Type[FrozenList[PositionOnFrettedInstrumentType]]]

    @classmethod
    def _make_single_argument(cls, arg: List) -> Self:
        instrument, poss = arg
        return cls.make(instrument, (cls.type.make_single_argument(pos) for pos in poss))

    def repr_single_argument(self) -> str:
        return f"""[{", ".join(position.repr_single_argument() for position in self.positions )}]"""

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        def clean_positions(positions: Iterable):
            instrument = kwargs["instrument"]
            l =[]
            for position in positions:
                if isinstance(position, tuple) and len(position) == 2:
                    string, fret = position
                    position = (instrument, string, fret)
                l.append(cls.type.make_single_argument(position))    
            positions = sorted_unique(l)
            return cls._frozen_list_type(positions)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "instrument")
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "positions", clean_positions)
        return super()._clean_arguments_for_constructor(args, kwargs)
 
    def played_positions(self):
        return self._frozen_list_type(pos for pos in self.positions if pos.fret.is_played())
    
    def closed_positions(self):
        return self._frozen_list_type(pos for pos in self.positions if pos.fret.is_closed())

    def __post_init__(self):
        assert_typing(self.positions, self._frozen_list_type)
        assert_iterable_typing(self.positions, self.type)

    def get_most_grave_note(self) -> Optional[PositionOnFrettedInstrumentType]:
        """The fretted_instrument position of the lowest note"""
        return optional_min(self.positions)

    def add(self, new_position: Union[PositionOnFrettedInstrumentType, Tuple[Union[String, int], Union[Fret, Optional[int]]]]) -> Self:
        """A set similar to `self`, with `position`"""
        if not isinstance(new_position, self.type):
            string, fret = new_position
            if isinstance(string, int):
                string = self.instrument.string(string)
            assert_typing(string, String)
            if isinstance(fret, int):
                fret = self.instrument.fret(fret)
            assert_typing(string, String)
            new_position = self.type(self.instrument, string, fret)
        new_positions = sorted(self.positions.append(new_position))
        return dataclasses.replace(self, positions =self._frozen_list_type(new_positions))

    def __iter__(self) -> Iterator[PositionOnFrettedInstrumentType]:
        return iter(sorted(self.positions))

    def __eq__(self, other: Self):
        assert_typing(other, self.__class__)
        return set(self.positions) == set(other.positions)
    
    def __lt__(self, other: Self):
        assert_typing(other, self.__class__)
        return set(self.played_positions()) < set(other.played_positions())
    
    def __le__(self, other: Self):
        assert_typing(other, self.__class__)
        return set(self.played_positions()) <= set(other.played_positions())

    def _max_fret(self) -> Optional[Fret] :
        """The greatest fret used."""
        played_positions = self.played_positions()
        return optional_max(position.fret for position in played_positions)
     
    def _min_fret(self, include_open: bool) -> Optional[Fret]:
        """The lowest fret used."""
        if include_open:
            return optional_min(position.fret for position in self.played_positions())
        return optional_min(position.fret for position in self.closed_positions())
    
    def number_of_frets(self, include_open: bool) -> int:
        """Returns the number of fret between the highest and the lowest fret."""
        m = self._min_fret(include_open)
        if m is None:
            return 0
        M = self._max_fret()
        assert M is not None
        return M.value - m.value
    
    def last_shown_fret(self) -> Optional[Fret]:
        return self._max_fret()

    def strings_at_fret(self, fret: Fret):
        return [pos.string for pos in self.positions if pos.fret == fret]
    
    def open_strings(self):
        return self.strings_at_fret(open_fret)

    def strings_at_min_fret(self, include_open: bool):
        return self.strings_at_fret(self._min_fret(include_open=include_open))
    
    def height(self, absolute: bool):
        return self.last_shown_fret().y_fret() + MARGIN
    
    def execute_on_maybe_transposed(self, absolute: bool, f: Callable[[AbstractSetOfFrettedPositions], T]) -> T:
        """Execute `f` on `self` if `absolute` otherwise on self transposed to first fret."""
        if not absolute:
            transposed, transpose_interval = self.transpose_to_fret_one()
        else:
            transposed = self
        return f(transposed)
    
    def svg_content(self, absolute: bool, colors: Optional[Colors] = None, nbFretMin: Fret =open_fret) -> List[str]:
        assert_optional_typing(colors, Colors)
        """If tonic, add some colors depending on the role of the note compared to the tonic"""
        max_fret = max(self.last_shown_fret(), nbFretMin).below()
        l = ["""<rect width="100%" height="100%" fill="white" />"""]
        l += self.instrument.strings().svg(lowest_fret=max_fret, show_open_fret=absolute)
        l += max_fret.all_frets_up_to_here(include_open=absolute).svg(absolute)
        for pos in self:
            chromatic = pos.get_chromatic()
            color = colors.get_color_from_note(chromatic_note = chromatic) if colors and chromatic else None
            assert_optional_typing(color, str)
            svg = pos.svg(absolute, color)
            #print(f"      {svg=}")
            l.append(svg)
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
        chromatic_intervals = ChromaticIntervalFrozenList(chromatic_note - lowest_note for chromatic_note in chromatic_notes)
        assert_iterable_typing(chromatic_intervals, ChromaticInterval)
        return ChromaticIntervalList.make_absolute(sorted_unique(chromatic_intervals))

    def intervals_frow_lowest_note_in_base_octave(self):
        intervals = self.intervals_frow_lowest_note()
        if intervals is None:
            return None
        absolute_chromatic_intervals = intervals.absolute_intervals()
        assert_iterable_typing(absolute_chromatic_intervals, ChromaticInterval)
        return ChromaticIntervalList.make_absolute(sorted_unique(interval.in_base_octave() for interval in absolute_chromatic_intervals))

    def _svg(self, absolute:bool, colors: Optional[Colors]= None,  nbFretMin: Fret=open_fret):
        assert_optional_typing(colors, Colors)
        new_line = "\n"
        return f"""\
    <svg xmlns="http://www.w3.org/2000/svg" width="{int(WIDTH)}" height="{int(self.height(absolute))}" version="1.1">
    {new_line.join(("  "+ content) for content in self.svg_content(absolute=absolute, colors=colors, nbFretMin=nbFretMin))}
    </svg>"""

    def svg(self, absolute:bool, colors: Optional[Colors]= None, nbFretMin: Fret=open_fret) -> str:
        assert_optional_typing(colors, Colors)
        return self.execute_on_maybe_transposed(absolute, lambda poss: (poss._svg(absolute, colors, nbFretMin)))
    
    def number_of_distinct_notes(self):
        return len(self.chromatic_notes())
    
    def get_specific_role(self, tonic: ChromaticNote, roles: Iterable[Union[ChromaticInterval, int]], assert_unique: bool = True):
        """Get the notes whose interval with tonic belongs in `roles`. If `assert_unique` a single of those role should be present at most.
        E.g. not having both third minor and major."""
        assert_typing(tonic, ChromaticNote)
        roles = [ChromaticInterval.make_single_argument(role) for role in roles]
        positions: List[PositionOnFrettedInstrumentType] = []
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
    
    def transpose_same_string(self, transpose: int, transpose_open: bool, transpose_not_played: bool):
        return dataclasses.replace(self, positions =self._frozen_list_type(position.transpose_same_string(transpose, transpose_open, transpose_not_played) for position in self.positions))
    
    def transpose_to_fret_one(self):
        assert not self.open_strings()
        transpose = ChromaticInterval(-(self._min_fret(include_open=False).value-1))
        return self.transpose_same_string(transpose=transpose, transpose_open=False, transpose_not_played=True), transpose

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